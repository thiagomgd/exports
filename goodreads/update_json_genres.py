import json
from tqdm import tqdm
from pprint import pprint
import utils

GOODREADS_URL = "https://www.goodreads.com/book/show/"

total_info_old = 0
total_info_new = 0




# books = notion.get_notion_data('BOOKS', p=p)
books = utils.load_json()
# books = {'55119872': {'goodreadsId': 55119872}}

new_books = {}

processed = 0

# for b in books:
for b in tqdm(books):
    book = books[b]
   
    if book.get('type', "") == "" or book.get('series', "") == "" or len(book.get('genres',[])) == 0:
        book = utils.updateInfo(book)
            
        # if to_update != {}:
        #     log("Updating", book['title'], to_update)
            # notion.update_notion(b.get('id'), to_update)
        processed += 1

    new_books[b] = book



print(len(new_books), len(books), processed)

with open('books.json', "w") as f:
    json.dump(new_books, f, indent=4)

MAIN_DIR = '/Users/thiago/git/geekosaurblog/src/_cache/'
with open(MAIN_DIR+'goodreads.json', "w") as f:
    json.dump(books, f, indent=4)