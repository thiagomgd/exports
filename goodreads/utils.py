import requests
import re
import json
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ff_options= Options()
ff_options.add_argument("--headless")
driver = webdriver.Firefox(options=ff_options)

DEBUG = False

GOODREADS_URL = "https://www.goodreads.com/book/show/"

SERIES_ENGLISH = {
    "イジらないで、長瀞さん / Ijiranaide, Nagatoro-san": "Nagatoro-san",
    "ぼくたちは勉強ができない / We Never Learn": "We Never Learn",
    "ドラゴンクエストダイの大冒険 / Dragon Quest Dai no Daibouken": "Dragon Quest: The Adventure Of Dai",
    "ドラゴンクエスト〜ダイの大冒険〜 [Dragon Quest: Dai no Daibōken]": "Dragon Quest: The Adventure Of Dai",
    "見える子ちゃん": "Mieruko-Chan",
    "ブラッククローバー [Black Clover]": "Black Clover"
}

def load_json():
    with open('books.json', 'r') as json_file:
        books = json.load(json_file)

        return books
    
def log(text, text2="", text3=""):
    if DEBUG:
        print('>>', text, text2, text3)

def get_number(val):
    try:
        num = int(val)
        return num
    except ValueError:
        try:
            num = float(val)
            return num
        except ValueError:
            return None

def get_cover(soup):
    try:
        tag = soup.find("img", {"class": "ResponsiveImage"})
        cover_url = tag['src']
        return cover_url
    except:
        # print("Book:", url, "found with no cover, try changing edition.", )
        return 'https://d15be2nos83ntc.cloudfront.net/images/no-cover.png'

# def get_info_old(soup):
#     # total_info_old += 1
#     series_h2 = soup.find("h2", {"id": "bookSeries"})

#     series = ''
#     n_in_series = None

#     log('series_h2', series_h2)

#     if series_h2:
#         series_a = series_h2.find("a" , recursive=False)
#         # series_text = re.search('\(([^)]+)', series_a.text).group(1) if series_a else ''

#         log('series a', series_a)
#         if series_a:
#             txt = series_a.text
#             if (txt.find('(')):
#                 txt = txt[txt.find('(')+1:txt.rfind(')')]
            
#             series = txt[:txt.find('#')].strip() if txt else ''
#             n_in_series_txt = txt[txt.find('#')+1:].strip() if txt else ''
#             n_in_series = get_number(n_in_series_txt)
#             log(series, n_in_series, "'{}'".format(txt))
#             # input('pause')


#     genres = []
    
#     genre_links = soup.select('a.bookPageGenreLink')
#     if len(genre_links):
#         genres = [] 
#         [genres.append(a.text) for a in genre_links if a.text not in genres] 

#     type = 'book'

#     if 'Manga' in genres:
#         type = 'manga'
#     elif 'Comics' in genres or 'Graphic Novel' in genres:
#         type = 'comic'
#     elif 'Light Novel' in genres:
#         type = 'light novel'


#     # print(series, type, genres, n_in_series)
#     return series, genres, type, n_in_series, get_setting(soup)

def get_setting(page):
#     {
#   "props": {
#     "pageProps": {
#       "apolloState": {
#         "Work:kca://work/amzn1.gr.work.v3.6lorV48xYuB-kwuJ": {
#           "details": {
#             "places": [
#               {
#                 "__typename": "Places",
#                 "name": "Penang",
#                 "countryName": "Malaysia",
#                 "webUrl": "https://www.goodreads.com/places/507922-penang",
#                 "year": null
#               }
#             ],

    item=page.select_one('script[id="__NEXT_DATA__"]').text

    jsondata=json.loads(item)['props']['pageProps']
  
    apolloState = jsondata['apolloState']

    placeData = None
    for key in apolloState.keys():
        if key.startswith('Work:kca://work'):
            placeData = apolloState[key]['details'].get('places', None)
            continue

    return placeData

def get_info(id):
    try:
        url = GOODREADS_URL + str(id)
        
        log('processing', url)
        driver.get(url)
        # element = driver.find_element(By.CSS_SELECTOR, "div.LoadingCard")
        # print("!!", element)


        try:
            WebDriverWait(driver, 25).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'img.ResponsiveImage'))
                    # EC.presence_of_element_located(('input[autocomplete=email]'))
                )
        except:
            driver.refresh()
            WebDriverWait(driver, 25).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'img.ResponsiveImage'))
                    # EC.presence_of_element_located(('input[autocomplete=email]'))
                )
        
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        # url_open = urlopen(url)
        # soup = BeautifulSoup(url_open, 'html.parser')
        # log('got soup')
        # if (soup.find("h1", {"id": "bookTitle"})):
        #     log("OLD", url)
        #     return get_info_old(soup)

        # total_info_new = total_info_new + 1
        log("NEW", url)
        title_div = soup.select_one("div.BookPageTitleSection__title") # > h3 > a") # > h3 > a")  # soup.find("h2", {"id": "bookSeries"})



        # item=soup.select_one('script[id="__NEXT_DATA__"]').text
        # jsondata=json.loads(item)['props']['pageProps']
        # apolloState = jsondata['apolloState']
        # pprint(jsondata)
        # pprint(soup)

        series_h3a = title_div.select_one("h3 > a")

        series = ''
        n_in_series = None

        if series_h3a:
            txt = series_h3a.text
            if (txt.find('#')):
                txt = txt[:txt.find('#')].strip()
                n_in_series_txt = txt[txt.find('#')+1:].strip() if txt else ''
                n_in_series = get_number(n_in_series_txt)

            series = txt

            # print(series, n_in_series, '-', txt)

        genres = []
        
        genre_links = soup.select('span.BookPageMetadataSection__genre > a')
        if len(genre_links):
            genres = [] 
            [genres.append(a.text) for a in genre_links if a.text not in genres] 
            # genres = [a.text for a in genre_links] 

        type = 'book'

        if 'Manga' in genres: # first this, because sometimes manga have both manga and comics as genre on GR
            type = 'manga'
        elif 'Comics' in genres or 'Graphic Novel' in genres:
            type = 'comic'
        elif 'Light Novel' in genres:
            type = 'lightNovel'

        # print(soup.find("div.BookDetails"))
        setting = get_setting(soup)
        # print('setting', setting)

        cover = get_cover(soup)
        # print(soup)
        # print(series, type, genres, n_in_series)
        return cover, series, genres, type, n_in_series, setting
    except Exception as e:
        # print('!!!!!!!!!!', book['title'], book['goodreadsId'])
        print(e)
        pass
        

    return None, None, None, None, None, None

def updateInfo(book):
    cover, series, genres, type, n_in_series, setting = get_info(book['goodreadsId'])

    if book.get('cover', None) == None or book['cover'].endswith('images/no-cover.png') and cover != None:
        book['cover'] = cover

    if series != None and series != '' and book.get("series","") == "": #!= None and  book["Series"] != '':
        book["series"] = series.replace(',',';') # why this? don't remember
    elif book.get("series","") == "" and "Perry Rhodan" in book['title']:
        book["series"] = "Perry Rhodan"
    
    if n_in_series != None and n_in_series != '' and book.get("numberInSeries",0) != n_in_series: #None and book["Number In Series"] != '':
        book["numberInSeries"] = n_in_series

    if genres:
        book["genres"] = genres

    if type != None and type != '' and book.get('type', "book") == "book": #!= None and book["Type"] != '':
        book["type"] = type

    if setting != None:
        book["setting"] = setting

    return book