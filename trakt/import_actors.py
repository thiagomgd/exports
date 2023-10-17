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
import lists
import time 

ACTORS_FILE = 'actors.json'
TMDB_ACTORS_FILE = 'tmdb_actors.json'

def load_json():
    with open(ACTORS_FILE, 'r') as json_file:
        act = json.load(json_file)

        return act

# def get_status(status):
#     statuses = {
#         'read': 'finished',
#         'tbr-owned': 'tbr/owned',
#         'owned-maybe': 'maybe',
#         'on-hold': 'paused',
#         'dnf': 'dnf',
#         'currently-reading': 'inProgress',
#         'tbr-not-owned': 'tbr/notOwned',
#         'owned-prob-not': 'owned-prob-not',
#         'next': 'tbr/next',
#         'to-read': 'grInterested',
#         'interested': 'interested'
#     }

#     # print("get status", status, statuses[status])
#     return statuses[status]


        

# def convert_book(book):
    
#     # if book['Book Id'] == "36568445":
#     #     print("!!!", getBookType(book), '-', book['Bookshelves'])

#     return {
#         "title": book['Title'],
#         "author": [book['Author']],
#         # TODO: fix?
#         # "Additional Authors": book['Additional Authors'],
#         "insb10": get_isbn(book['ISBN']),
#         "isbn13": get_isbn(book['ISBN13']),
#         "rating": float(book['My Rating']) if book['My Rating'].isnumeric() else None,
#         "averageRating": float(book['Average Rating']) if book['Average Rating'].isnumeric() else None,
#         "publisher": book['Publisher'].replace(',',';'),
#         "binding": book['Binding'],
#         "pages": int(book['Number of Pages']) if book['Number of Pages'].isnumeric() else None,
#         "yearPublished": int(book['Year Published']) if book['Year Published'].isnumeric() else None,
#         "originalPublicationYear": int(book['Original Publication Year']) if book['Original Publication Year'].isnumeric() else None,
#         "dateRead": gr_date(book['Date Read']).isoformat()[:10] if gr_date(book['Date Read']) else None,
#         "dateAddedGR": gr_date(book['Date Added']).isoformat()[:10] if gr_date(book['Date Added']) else None,
#         "bookshelves": book['Bookshelves'],
#         "status": get_status(book['Exclusive Shelf']),
#         "cover": book.get('cover', None),
#         "goodreadsId": int(book['Book Id']),
#         "goodreadsLink": "https://www.goodreads.com/book/show/{}".format(book['Book Id']),
#         "type": getBookType(book)
#     }


def update_record(json_data, trakt_data):
    new_data = copy.deepcopy(json_data)

    # for now, justoverwrite all trakt data (this will skip any custom fields I decide to add)
    new_data['name'] = trakt_data.get('name')
    new_data['traktId'] = trakt_data.get('traktId')
    new_data['tmdbId'] = trakt_data.get('tmdbId')
    new_data['birthday'] = trakt_data.get('birthday')
    new_data['country'] = trakt_data.get('country')
    # profession can be overwritten by me
    # new_data['profession'] = trakt_data.get('profession')
    new_data['link'] = trakt_data.get('link')
    new_data['instagram'] = trakt_data.get('instagram')
    new_data['twitter'] = trakt_data.get('twitter')
    new_data['photo'] = trakt_data.get('photo')
    new_data['syncedDate'] = time.time()*1000

    return new_data

actors_trakt = lists.get_trakt_actors()

actors_json = load_json()


print("TOTAL json", len(actors_json), 'Total Trakt', len(actors_trakt))

# # TODO: keep track of visited, check which ones on JSON are not on trakt, print to terminal so I can delete

new = 0
updated = 0
new_dict = {}

# # for book_id in books_gr:
for id in tqdm(actors_trakt):
    actor_trakt = actors_trakt[id]
    # id = str(thing_trakt['traktId'])

    if id in actors_json:
        # print('EXISTS')
        actor_json = actors_json[id]
        # print(book_id)

        
        new_data = update_record(actor_json, actor_trakt)
        # print('@@@', new_data['status'])
        # print('update?')
        new_dict[id] = new_data
        # del media_json[id]
        updated += 1
            # print("!!!!", new_dict[book_id]['status'])
    else:
        # print(id, media_json.get(id), media_json.get(int(id)))
        new_dict[id] = actor_trakt
        new += 1
    

print(
    "new:", len(new_dict),
    "json", len(actors_json),
    "trakt", len(actors_trakt),
    "new", new,
    "updated", updated
    )

with open(ACTORS_FILE, "w") as f:
    json.dump(new_dict, f, indent=4)

tmdb_dict = {v['tmdbId']:v for (k,v) in new_dict.items()}

with open(ACTORS_FILE, "w") as f:
    json.dump(tmdb_dict, f, indent=4)

# MAIN_DIR = '/Users/thiago/git/geekosaurblog/src/_cache/'
# with open(MAIN_DIR+'goodreads.json', "w") as f:
#     json.dump(new_dict, f, indent=4)