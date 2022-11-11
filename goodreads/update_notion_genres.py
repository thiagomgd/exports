import requests
import json
import re
from pprint import pprint
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
import notion

GOODREADS_URL = "https://www.goodreads.com/book/show/"

SERIES_ENGLISH = {
    "イジらないで、長瀞さん / Ijiranaide, Nagatoro-san": "Nagatoro-san",
    "ぼくたちは勉強ができない / We Never Learn": "We Never Learn",
    "ドラゴンクエストダイの大冒険 / Dragon Quest Dai no Daibouken": "Dragon Quest: The Adventure Of Dai",
    "見える子ちゃん": "Mieruko-Chan"
}

DEBUG = False

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
            print(series, n_in_series, txt)
            # input('pause')


    genres = []
    
    genre_links = soup.select('a.bookPageGenreLink')
    if len(genre_links):
        genres = [a.text for a in genre_links] 

    type = 'book'

    if 'Manga' in genres:
        type = 'manga'
    elif 'Comics' in genres or 'Graphic Novel' in genres:
        type = 'comic'
    elif 'Light Novel' in genres:
        type = 'light novel'


    # print(series, type, genres, n_in_series)
    return series, genres, type, n_in_series

def get_info(id):
    url = GOODREADS_URL + str(id)
    
    log('processing', url)
    url_open = urlopen(url)
    soup = BeautifulSoup(url_open, 'html.parser')

    if (soup.find("h1", {"id": "bookTitle"})):
        log("OLD", url)
        return get_info_old(soup)

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

        print(series, n_in_series, txt)

    genres = []
    
    genre_links = soup.select('span.BookPageMetadataSection__genre > a')
    if len(genre_links):
        genres = [a.text for a in genre_links] 

    type = 'book'

    if 'Manga' in genres: # first this, because sometimes manga have both manga and comics as genre on GR
        type = 'manga'
    elif 'Comics' in genres or 'Graphic Novel' in genres:
        type = 'comic'
    elif 'Light Novel' in genres:
        type = 'light novel'


    # print(series, type, genres, n_in_series)
    return series, genres, type, n_in_series

p = {
    "filter": {
        "property": "Type",
        "select": {
            "is_empty": True
        }
    }
}


books = notion.get_notion_data('BOOKS', p=p)
for b in books:
    book = notion.get_props_data(b)
    try:
        # DEBUG = book['Title'].find('One Piece') >= 0

        series, genres, type, n_in_series = get_info(book['Book Id'])
        to_update = {}

        if series != None and series != '' and book["Series"] != series: #!= None and  book["Series"] != '':
            to_update["Series"] = series.replace(',',';')
        
        if n_in_series != None and n_in_series != '' and book["Number In Series"] != n_in_series: #None and book["Number In Series"] != '':
            to_update["Number In Series"] = n_in_series

        if genres:
            to_update["Genres"] = genres

        if type != None and type != '' and book["Type"] != type: #!= None and book["Type"] != '':
            to_update["Type"] = type
            
        if to_update != {}:
            log("Updating", book['Title'], to_update)
            notion.update_notion(b.get('id'), to_update)
    except Exception as e:
        print('!!!!!!!!!!', book['Title'], book['Book Id'])
        print(e)


# url = GOODREADS_URL + str(id)

#     print(url)

#     url_open = urlopen(url)
#     soup = BeautifulSoup(url_open, 'html.parser')

