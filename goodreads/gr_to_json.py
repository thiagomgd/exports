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
import utils 

GOODREADS_URL = "https://www.goodreads.com/book/show/"

def load_json():
    with open('books.json', 'r') as json_file:
        books = json.load(json_file)

        return books



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

def getBookType(book):
    # if (book.get('type', None)) != None:
    #     return book['type']
    
    if ('manga' in book['Bookshelves']):
        return 'manga'

    if ('light-novel' in book['Bookshelves']):
        return 'light novel'
    
    if ('comics' in book['Bookshelves'] or 'graphic-novels' in book['Bookshelves']):
        return 'comic'

    # if ('non-fiction' in book['Bookshelves']):
    #     return 'book'

    if (book.get('type', None)) != None:
        return book['type']
    
    return None
        

def convert_book(book):
    
    # if book['Book Id'] == "36568445":
    #     print("!!!", getBookType(book), '-', book['Bookshelves'])

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
        "cover": book.get('cover', None),
        "goodreadsId": int(book['Book Id']),
        "goodreadsLink": "https://www.goodreads.com/book/show/{}".format(book['Book Id']),
        "type": getBookType(book)
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
    new_data['bookshelves'] = gr_data['bookshelves']

    if (gr_data.get('dateRead', None) != None):
        new_data['dateRead'] = gr_data['dateRead']
        new_data['yearRead'] = int(gr_data['dateRead'][:4])
    elif (new_data.get('yearRead', None) == None and new_data.get('dateRead', None) != None):
        new_data['yearRead'] = int(new_data['dateRead'][:4])

    if (gr_data['type'] != None):
        new_data['type'] = gr_data['type']

    # print('cover', new_data['cover'], new_data['cover'].endswith('images/no-cover.png'))
    # new books will have no cover anyway, no need to check for other tags
    if new_data.get('cover', None) == None or new_data['cover'].endswith('images/no-cover.png'):
        new_data = utils.updateInfo(new_data)

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

# for book_id in books_gr:
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

MAIN_DIR = '/Users/thiago/git/geekosaurblog/src/_cache/'
with open(MAIN_DIR+'goodreads.json', "w") as f:
    json.dump(new_dict, f, indent=4)