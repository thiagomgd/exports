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
TYPE = 'BOOKS'

def get_series(title):
    # Song of the Forever Rains (Mousai, #1)
    # Ember Falls (The Green Ember #2)
    # 文豪ストレイドッグス 8 [Bungō Stray Dogs 8]
    # ぼくたちは勉強ができない 7 [Bokutachi wa Benkyou ga Dekinai 7] (We Never Learn, #7)
    # Ranma 1/2 (2-in-1 Edition), Vol. 5: Includes Volumes 9  10
    # Bottom-Tier Character Tomozaki, Vol. 3 (light novel)
    # Occultic;Nine: Volume 2
    # Amagi Brilliant Park: Volume 1
    # House of Secrets: Clash of the Worlds (House of Secrets Series)


    print(title)
    match = re.search('\(([^)]+)', title) #.group(1)
    
    if match != None: # has something inside ()
        between_par = match.group(1)
        # print(between_par)
        
        comma_pos = between_par.find(',')
        
        if comma_pos > 0: # title, #number
            return between_par.split(',')[0]

    return None

def get_cover(id):
    url = GOODREADS_URL + str(id)
    url_open = urlopen(url)
    soup = BeautifulSoup(url_open, 'html.parser')
    tag = soup.find("img", {"id": "coverImage"})
    try:
        cover_url = tag['src']
        return cover_url
    except:
        print("Book:", url, "found with no cover, try changing edition.")
        return 'https://d15be2nos83ntc.cloudfront.net/images/no-cover.png'


def gr_date(val):
    if val == '' or val == None:
        return None

    return datetime.strptime(val, "%Y/%m/%d")

def convert_book(book):
    return {
        "Title": book['Title'],
        "Author": book['Author'],
        "Additional Authors": book['Additional Authors'],
        "ISBN": book['ISBN'],
        "ISBN13": book['ISBN13'],
        "My Rating": book['My Rating'],
        "Average Rating": book['Average Rating'],
        "Publisher": book['Publisher'],
        "Binding": book['Binding'],
        "Number of Pages": book['Number of Pages'],
        "Year Published": book['Year Published'],
        "Original Publication Year": book['Original Publication Year'],
        "Date Read": gr_date(book['Date Read']),
        "Date Added": gr_date(book['Date Added']),
        "Bookshelves": book['Bookshelves'],
        "Status": book['Exclusive Shelf'],
        "Cover": None,
        "Book Id": book['Book Id'],
        "Link": "https://www.goodreads.com/book/show/{}".format(book['Book Id'])
    }


def compare_data(notion_data, gr_data):
    TO_COMPARE = ['Status', 'My Rating', "Date Read"] #, 'Average Rating'] 'Type', 'Series'

    stored = notion.get_props_data(notion_data)
    # stored = notion
    to_update = {}
    
    for key in TO_COMPARE:
        notion_val = stored.get(key)
        gr_val = gr_data.get(key)
        if notion_val != gr_val:
            # if key == 'Status' and an_val == 'Planning' and notion_val in ['Planning', 'Next', 'Maybe']:
            #     continue
            # if (key == 'Date Read'):
            #     print('GR:', an_val, ' , Notion:', notion_val)
            #     input('a')

            if (key == 'Series' and gr_val == None) or (key == 'Type' and gr_val == None):
                continue

            # print(key, notion_val, an_val)

            # pprint(stored)
            # input('a')
            to_update[key] = gr_val

    return to_update  

def update_record(notion_data, gr):
    diff = compare_data(notion_data, gr)
    
    if len(diff) > 0:
        print('Update', gr['Title'])
        notion.update_notion(notion_data.get('id'), diff)


def insert_record(gr):
    print('Inserting: ', gr["Title"])

    gr['Cover'] = get_cover(gr['Book Id'])

    notion.insert_notion(TYPE, gr)

organized = {}

books_notion_ = notion.get_notion_data(TYPE)

books_gr = {}

with open('goodreads.json') as f:
    books_gr_json = json.load(f)
    for book_ in books_gr_json:
        book = convert_book(book_)
        if book["Status"] != 'to-read':
            books_gr[book['Book Id']] = book


books_notion = {x['properties']['Book Id']['number']: x for x in books_notion_}

print("TOTAL", len(books_notion), 'Total GR', len(books_gr))
# pprint(books_notion)
for book_id in books_gr:
    b_gr = books_gr[book_id]
    # print(book_id)
    if book_id in books_notion:
        update_record(books_notion[b_gr['Book Id']], b_gr)
    else:
        insert_record(b_gr)
