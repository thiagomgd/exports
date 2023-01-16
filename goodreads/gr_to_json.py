import requests
import json
import re
from pprint import pprint
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv 
import copy 
from tqdm import tqdm

GOODREADS_URL = "https://www.goodreads.com/book/show/"
TYPE = 'BOOKS'

def load_json():
    with open('books.json', 'r') as json_file:
        books = json.load(json_file)

        return books

# def get_series(title):
#     # Song of the Forever Rains (Mousai, #1)
#     # Ember Falls (The Green Ember #2)
#     # 文豪ストレイドッグス 8 [Bungō Stray Dogs 8]
#     # ぼくたちは勉強ができない 7 [Bokutachi wa Benkyou ga Dekinai 7] (We Never Learn, #7)
#     # Ranma 1/2 (2-in-1 Edition), Vol. 5: Includes Volumes 9  10
#     # Bottom-Tier Character Tomozaki, Vol. 3 (light novel)
#     # Occultic;Nine: Volume 2
#     # Amagi Brilliant Park: Volume 1
#     # House of Secrets: Clash of the Worlds (House of Secrets Series)


#     # print(title)
#     match = re.search('\(([^)]+)', title) #.group(1)
    
#     if match != None: # has something inside ()
#         between_par = match.group(1)
#         # print(between_par)
        
#         comma_pos = between_par.find(',')
        
#         if comma_pos > 0: # title, #number
#             return between_par.split(',')[0]

#     return None

def get_cover(id):
    url = GOODREADS_URL + str(id)
    try:
        url_open = urlopen(url)
        soup = BeautifulSoup(url_open, 'html.parser')
        tag = soup.find("img", {"id": "coverImage"})
        cover_url = tag['src']
        return cover_url
    except:
        # print("Book:", url, "found with no cover, try changing edition.")
        return 'https://d15be2nos83ntc.cloudfront.net/images/no-cover.png'


def gr_date(val):
    if val == '' or val == None:
        return None

    return datetime.strptime(val, "%Y/%m/%d")

def get_isbn(param):
    if param == None or param == "":
        return None 
    
    num = re.findall(r'\d+', param) 

    if (len(num) == 0):
        return None

    return num[0]

def get_status(status):
    statuses = {
        'read': 'finished',
        'tbr-owned': 'tbr/owned',
        'owned-maybe': 'maybe',
        'on-hold': 'paused',
        'dnf': 'dnf',
        'currently-reading': 'inProgress',
        'tbr-not-owned': 'tbr/notOwned',
        'owned-prob-not': 'owned-prob-not',
        'next': 'tbr/next',
        'to-read': 'grInterested',
        'interested': 'interested'
    }

    # print("get status", status, statuses[status])
    return statuses[status]

def convert_book(book):

    return {
        "title": book['Title'],
        "author": [book['Author']],
        # TODO: fix?
        # "Additional Authors": book['Additional Authors'],
        "insb10": get_isbn(book['ISBN']),
        "isbn13": get_isbn(book['ISBN13']),
        "rating": float(book['My Rating']) if book['My Rating'].isnumeric() else None,
        "averageRating": float(book['Average Rating']) if book['Average Rating'].isnumeric() else None,
        "publisher": book['Publisher'].replace(',',';'),
        "binding": book['Binding'],
        "pages": int(book['Number of Pages']) if book['Number of Pages'].isnumeric() else None,
        "yearPublished": int(book['Year Published']) if book['Year Published'].isnumeric() else None,
        "originalPublicationYear": int(book['Original Publication Year']) if book['Original Publication Year'].isnumeric() else None,
        "dateRead": gr_date(book['Date Read']).isoformat()[:10] if gr_date(book['Date Read']) else None,
        "dateAddedGR": gr_date(book['Date Added']).isoformat()[:10] if gr_date(book['Date Added']) else None,
        "bookshelves": book['Bookshelves'],
        "status": get_status(book['Exclusive Shelf']),
        "cover": book.get('cover',None),
        "goodreadsId": int(book['Book Id']),
        "goodreadsLink": "https://www.goodreads.com/book/show/{}".format(book['Book Id'])
    }

# dateAdded: {{date}}
# dateAddedGR:
# dateRead: 
# owned: 
# status: interested
# tags:
# - media/book
# - status/interested
# aliases:
# - "{{title}}"
# title: "{{title}}"
# author: [{{author}}]
# category: {{category}}
# pages: {{totalPage}}
# publishDate: {{publishDate}} 
# publisher: {{publisher}}
# isbn10: {{isbn10}}
# isbn13: {{isbn13}}
# summary: "{{description}}"

def update_record(json_data, gr_data):
    new_data = copy.deepcopy(json_data)

    new_data['status'] = gr_data['status']
    new_data['rating'] = gr_data['rating']
    new_data['dateRead'] = gr_data['dateRead']

    if new_data.get('cover', None) == None or new_data['cover'] == 'https://d15be2nos83ntc.cloudfront.net/images/no-cover.png':
        new_data['cover'] = get_cover(new_data['goodreadsId'])

    return new_data

organized = {}

books_gr = {}


with open('goodreads_library_export.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        # print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
        line_count += 1
        book = convert_book(row)
        # pprint(book)
        if book["status"] != 'to-read' and book["status"] != 'grInterested':
            books_gr[str(book['goodreadsId'])] = book

    print(f'Processed {line_count} lines.')

books_json = load_json()


print("TOTAL", len(books_json), 'Total GR', len(books_gr))
# pprint(books_notion)

# TODO: keep track of visited, check which ones on JSON are not on GR, print to terminal so I can delete

new = 0
updated = 0
new_dict = {}

for book_id in tqdm(books_gr):
    b_gr = books_gr[book_id]
    # print(book_id)
    if book_id in books_json:
        b_json = books_json[book_id]
        
        new_data = update_record(b_json, b_gr)
        # print('@@@', new_data['status'])
        # print('update?')
        new_dict[book_id] = new_data
        del books_json[book_id]
        updated += 1
        # print("!!!!", new_dict[book_id]['status'])
    else:
        # insert_record(b_gr)
        new_dict[book_id] = b_gr
        new += 1

    

print(len(new_dict), len(books_json), len(books_gr), new, updated)

with open('books.json', "w") as f:
    json.dump(new_dict, f, indent=4)
