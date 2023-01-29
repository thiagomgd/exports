import requests
import json
import re
from pprint import pprint
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm

GOODREADS_URL = "https://www.goodreads.com/book/show/"

SERIES_ENGLISH = {
    "イジらないで、長瀞さん / Ijiranaide, Nagatoro-san": "Nagatoro-san",
    "ぼくたちは勉強ができない / We Never Learn": "We Never Learn",
    "ドラゴンクエストダイの大冒険 / Dragon Quest Dai no Daibouken": "Dragon Quest: The Adventure Of Dai",
    "ドラゴンクエスト〜ダイの大冒険〜 [Dragon Quest: Dai no Daibōken]": "Dragon Quest: The Adventure Of Dai",
    "見える子ちゃん": "Mieruko-Chan",
    "ブラッククローバー [Black Clover]": "Black Clover"
}

DEBUG = True

total_info_old = 0
total_info_new = 0

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


def get_info_old(soup):
    # total_info_old += 1
    series_h2 = soup.find("h2", {"id": "bookSeries"})

    series = ''
    n_in_series = None

    log('series_h2', series_h2)

    if series_h2:
        series_a = series_h2.find("a" , recursive=False)
        # series_text = re.search('\(([^)]+)', series_a.text).group(1) if series_a else ''

        log('series a', series_a)
        if series_a:
            txt = series_a.text
            if (txt.find('(')):
                txt = txt[txt.find('(')+1:txt.rfind(')')]
            
            series = txt[:txt.find('#')].strip() if txt else ''
            n_in_series_txt = txt[txt.find('#')+1:].strip() if txt else ''
            n_in_series = get_number(n_in_series_txt)
            log(series, n_in_series, "'{}'".format(txt))
            # input('pause')


    genres = []
    
    genre_links = soup.select('a.bookPageGenreLink')
    if len(genre_links):
        genres = [] 
        [genres.append(a.text) for a in genre_links if a.text not in genres] 

    type = 'book'

    if 'Manga' in genres:
        type = 'manga'
    elif 'Comics' in genres or 'Graphic Novel' in genres:
        type = 'comic'
    elif 'Light Novel' in genres:
        type = 'light novel'


    # print(series, type, genres, n_in_series)
    return series, genres, type, n_in_series

def get_setting(page):
    setting = None 
    
    descItem = page.select("div.WorkDetails") # div.DescListItem")

    print(descItem)
    for itm in descItem:
        if itm.select_one("dt").text == "Setting":
            setting = itm.select_one("dd").text

    return setting

def get_info(id):
    try:
        url = GOODREADS_URL + str(id)
        
        log('processing', url)
        url_open = urlopen(url)
        soup = BeautifulSoup(url_open, 'html.parser')
        log('got soup')
        if (soup.find("h1", {"id": "bookTitle"})):
            log("OLD", url)
            return get_info_old(soup)

        # total_info_new = total_info_new + 1
        log("NEW", url)
        title_div = soup.select_one("div.BookPageTitleSection__title") # > h3 > a") # > h3 > a")  # soup.find("h2", {"id": "bookSeries"})

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

            print(series, n_in_series, '-', txt)

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
        # setting = get_setting(soup)
        # print(setting)

        # print(soup)
        # print(series, type, genres, n_in_series)
        return series, genres, type, n_in_series #, setting
    except Exception as e:
        # print('!!!!!!!!!!', book['title'], book['goodreadsId'])
        # print(e)
        pass
        

    return None, None, None, None

p = {
    "filter": {
        "property": "Type",
        "select": {
            "is_empty": True
        }
    }
}


# books = notion.get_notion_data('BOOKS', p=p)
# books = load_json()
books = {'55119872': {'goodreadsId': 55119872}}

new_books = {}

processed = 0

for b in books:
# for b in tqdm(books):
    book = books[b]
   
    if book.get('type', "") == "":
        series, genres, type, n_in_series = get_info(book['goodreadsId'])

        if series != None and series != '' and book.get("series","") != series: #!= None and  book["Series"] != '':
            book["series"] = series.replace(',',';') # why this? don't remember
        elif book.get("series","") == "" and "Perry Rhodan" in book['title']:
            book["series"] = "Perry Rhodan"
        
        if n_in_series != None and n_in_series != '' and book.get("numberInSeries",0) != n_in_series: #None and book["Number In Series"] != '':
            book["numberInSeries"] = n_in_series

        if genres:
            book["genres"] = genres

        if type != None and type != '' and book.get("type","") != type: #!= None and book["Type"] != '':
            book["type"] = type
            
        # if to_update != {}:
        #     log("Updating", book['title'], to_update)
            # notion.update_notion(b.get('id'), to_update)
        processed += 1

    new_books[b] = book


# url = GOODREADS_URL + str(id)

#     print(url)

#     url_open = urlopen(url)
#     soup = BeautifulSoup(url_open, 'html.parser')

print(len(new_books), len(books), processed)
print('info old:', total_info_old, 'info new:', total_info_new)

with open('books.json', "w") as f:
    json.dump(new_books, f, indent=4)