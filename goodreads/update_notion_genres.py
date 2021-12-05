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


def get_info(id):
    url = GOODREADS_URL + str(id)
    url_open = urlopen(url)
    soup = BeautifulSoup(url_open, 'html.parser')

    series_h2 = soup.find("h2", {"id": "bookSeries"})

    series = ''
    n_in_series = None

    if series_h2:
        series_a = series_h2.find("a" , recursive=False)
        # series_text = re.search('\(([^)]+)', series_a.text).group(1) if series_a else ''
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

    if 'Comics' in genres or 'Graphic Novel' in genres:
        type = 'comic'
    elif 'Manga' in genres:
        type = 'manga'
    elif 'Light Novel' in genres:
        type = 'light novel'


    # print(series, type, genres, n_in_series)
    return series, genres, type, n_in_series

    
# print(get_info(91478))

books = notion.get_notion_data('BOOKS')
for b in books:
    book = notion.get_props_data(b)
    series, genres, type, n_in_series = get_info(book['Book Id'])
    if series != None and series != '':
        notion.update_notion(b.get('id'), {'Series': series, 'Genres': genres, 'Type': type, 'Number In Series': n_in_series})
