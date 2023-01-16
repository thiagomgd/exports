import json
from pprint import pprint
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm
import ruamel.yaml
import re
import os 
import frontmatter
import copy 

yaml = ruamel.yaml.YAML()

MAIN_DIR = '/Users/thiago/git/Main/Books'
# MAIN_DIR = 'mds'
# IGNORE_LIST = ['{}/Inbox/'.format(MAIN_DIR), '/.DS_Store']

CHANGED_STATUS = []

def load_json():
    with open('books.json', 'r') as json_file:
        books = json.load(json_file)

        return books

def load_md():
    book_data = {}
    book_files = {}

    for root, dirs, files in os.walk(MAIN_DIR, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            if file_path.endswith('.DS_Store') or file_path.startswith('{}/Inbox/'.format(MAIN_DIR)):
                continue

            # print(file_path)
            data = frontmatter.load(file_path)
            # print('\n\n\n------\n')
            # pprint(data.metadata)
            # pprint(data.content)

            book_data[str(data.metadata['goodreadsId'])] = data
            book_files[str(data.metadata['goodreadsId'])] = file_path
            # break
            # with open(file_path, 'r') as f:
            #     data = yaml.load_all(f)
            #     for itm in data:
            #         pprint(itm)
            #     break
            # stuff
        # for name in dirs:
        #     print(os.path.join(root, name))
            # stuff

    return book_data, book_files

def containsAny(str, set):
    """ Check whether sequence str contains ANY of the items in set. """
    return 1 in [c in str for c in set]

def set_file_frontmatter(book):
    frontmatter = {}

    # aliases =  [] #['"'+book['title'].translate({ord(i): None for i in '\/:#[]|'}).replace('  ', ' ')+'"']

    # if containsAny(book['title'],'\:#[]|""/'):
        # title = book['title'] # re.sub(r'\(.+\)', ' ', book['title']) # Not removing series to avoid collisions
    #     aliases.append(title.translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip()) 
    # else:
    #     aliases.append(book['title'])

    cleanTitle = book['title'].translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip() # re.sub(r'\(.+\)', ' ', book['title']) # Not removing series to avoid collisions
    aliases = [cleanTitle]

    # q = {}
    # q['a'] = "'{}'".format(book['title'].translate({ord(i): None for i in '\/:#[]|'}).replace('  ', ' '))
    # q['b'] = book['title'].translate({ord(i): None for i in '\/:#[]|'}).replace('  ', ' ')
    # q['c'] = '"'+book['title'].translate({ord(i): None for i in '\/:#[]|'}).replace('  ', ' ')+'"'
    # pprint(q)
    # aliases[0] = 
    

    # frontmatter['owned']: book[''] 
    # TODO: fiction/nonfiction
    # frontmatter['category']: book[''] {{category}} 
    # frontmatter['publishDate']: book[''] {{publishDate}} 
    # frontmatter['summary']: book['']

    frontmatter['dateAddedGR'] = book.get('dateAddedGR') 
    frontmatter['dateRead'] = book.get('dateRead') 
    frontmatter['title'] = book.get('title') 
    frontmatter['author'] = book.get('author')
    frontmatter['pages'] = book.get('pages')
    frontmatter['publisher'] = book.get('publisher')
    frontmatter['isbn10'] = book.get('isbn10')
    frontmatter['isbn13'] = book.get('isbn13')
    frontmatter['link'] = book.get('goodreadsLink')

    frontmatter["rating"] = book.get('rating')
    frontmatter["averageRating"] = book.get('averageRating')
    frontmatter["binding"] = book.get('binding') 
    frontmatter["pages"] = book.get('pages')
    frontmatter["yearPublished"] = book.get('yearPublished')
    frontmatter["originalPublicationYear"] = book.get('originalPublicationYear')
    frontmatter["bookshelves"] = book.get('bookshelves')
    frontmatter["cover"] = book.get('cover')
    frontmatter["goodreadsId"] = book.get('goodreadsId')
    frontmatter["series"] = book.get('series')
    frontmatter["numberInSeries"] = book.get('numberInSeries')
    frontmatter["genres"] = book.get('genres')

    frontmatter['aliases'] = aliases
        
    tags = ['media/book']
    tags.append('status/'+book['status'])

    frontmatter['tags'] = tags

    # pprint(frontmatter)
    return frontmatter

def get_new_data(json_data, file_data):
    updated = False

    new_data = copy.deepcopy(file_data)

    attributes = ['rating', 'binding', 'bookshelves', 'series', 'numberInSeries', 'genres'] # add type, setting

    for attribute in attributes:
        if file_data.get(attribute) != json_data.get(attribute):
            updated = True
            new_data[attribute] = json_data.get(attribute)

    status = 'status/' + json_data['status']

    if status not in file_data['tags']:
        # replace status tag
        CHANGED_STATUS.append(new_data['title'])
        new_tags = []
        for tag in file_data['tags']:
            print('tag:', tag)
            if tag.startswith('status/'):
                print('STARTSWITH', status)
                new_tags.append(status)
            else:
                new_tags.append(tag)

        new_data['tags'] = new_tags

        updated = True
        
    # JUST ONCE
    # print(json_data['title'])
    # new_data['aliases'] = [json_data['title'].translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip()]
    # updated = True

    return new_data, updated

def get_extra(book):
    text = """from:: 
related:: 

![cover|150]({cover})
***

"""

    return text.format(**book)

def should_skip(book):
    if book.get('type','') == '':
        # print('No type', book['title'], book['status'])
        return True

    if book.get('type', '') not in ['book', 'lightNovel']:
        # print("Type: ", book['type'])
        return True

    # 'read': 'finished',
    # 'tbr-owned': 'tbr/owned',
    # 'owned-maybe': 'maybe',
    # 'on-hold': 'paused',
    # 'abandoned': 'abandoned',
    # 'currently-reading': 'inProgress',
    # 'tbr-not-owned': 'tbr/notOwned'

    desired_status = [
        'finished',
        'tbr/owned',
        # 'owned-maybe': 'maybe',
        'paused',
        'dnf',
        'inProgress',
        'tbr/notOwned',
        # 'to-read': 'grInterested'
        'tbr/next',
        'interested'
    ]

    if book['status'] not in desired_status:
        # print("Skip: ", book['status'])
        return True

    if "Perry Rhodan" in book.get('series','') and "Perry Rhodan NEO" not in book.get('series',''):
        return True

    return False

def get_filename(book):
    fn = book['title']
    if len(book['author']) > 0:
        fn = '{} - {}'.format(book['title'], book['author'][0])

    return fn.translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip()

def get_folder(book):
    folder = {
        'finished': 'finished/',
        'tbr/owned': 'tbr/',
        'tbr/notOwned': 'tbr/',
        'tbr/next': 'next/',
        # 'maybe': '', #it's not saved
        'paused': 'paused/',
        'interested': 'interested/',
        'dnf': 'dnf/',
        'inProgress': ''
    }

    return folder[book['status']]


json_books = load_json()

md_books, md_files = load_md()
print( len(md_books), len(md_files))
for bookId in json_books:
    # print(bookId)
    book = json_books[bookId]
    

    if should_skip(book):
        continue

    # pprint(book)

    if bookId in md_books:
        # print("EXISTS")
        new_data, updated = get_new_data(book, md_books[bookId].metadata)
        if updated:
            # print('should update')
            # print('File:', md_files[bookId])
            with open(md_files[bookId], 'w') as fh:
                fh.write('---\n')
                yaml.dump(new_data, fh)
                fh.write('---\n')
                fh.write(md_books[bookId].content)
    else:
        # TODO: Check if it's changed edition 
        #     if there's a file already, it's same book
        # print('new')
        # pass
        frontmatter = set_file_frontmatter(book)
        filename = get_filename(book)
        folder = get_folder(book)

        # print("Saving: ", folder, filename)
        with open("mds/{}{}.md".format(folder, filename), 'w') as fh:
            fh.write('---\n')
            yaml.dump(frontmatter, fh)
            fh.write('---\n')
            extra_data = get_extra(book)
            fh.write(extra_data)

#     # break

print("Changed status:", CHANGED_STATUS)
print("Unvisited files:", md_files)

