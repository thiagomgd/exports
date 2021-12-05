from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, datetime, csv, tqdm

GOODREADS_URL = "https://www.goodreads.com/book/show/"

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
        "Date Read": book['Date Read'],
        "Date Added": book['Date Added'],
        "Bookshelves": book['Bookshelves'],
        "Status": book['Exclusive Shelf'],
        "Cover": None,
        "Book Id": book['Book Id'],
    }

with open('goodreads.json') as f:
  books_ = json.load(f)

books = []


for book_ in books_:
    book = convert_book(book_)
    if book["Status"] != 'to-read':
        books.append(book)

# for book in tqdm.tqdm(books):
#     url = GOODREADS_URL + str(book['Book Id'])
#     url_open = urlopen(url)
#     soup = BeautifulSoup(url_open, 'html.parser')
#     tag = soup.find("img", {"id": "coverImage"})
#     try:
#         book['Cover'] = tag['src']
#     except:
#         print("Book:", url, "found with no cover, try changing edition.")

# csv_columns = ["Title"
# , "Author"
# , "Additional Authors"
# , "ISBN"
# , "ISBN13"
# , "My Rating"
# , "Average Rating"
# , "Publisher"
# , "Binding"
# , "Number of Pages"
# , "Year Published"
# , "Original Publication Year"
# , "Date Read"
# , "Date Added"
# , "Bookshelves"
# , "Status"
# , "Cover",
# "Book Id"]

time_stamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")

with open('with_covers_{}.json'.format(time_stamp), mode='w') as jsonfile:
    json.dump(books, jsonfile)
    # writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    # writer.writeheader()
    # for data in books:
    #     writer.writerow(data)