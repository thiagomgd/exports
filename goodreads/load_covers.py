from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, datetime, csv, tqdm

GOODREADS_URL = "https://www.goodreads.com/book/show/"

with open('goodreads.json') as f:
  books = json.load(f)

for book in tqdm.tqdm(books):
    url = GOODREADS_URL + str(book['Book Id'])
    url_open = urlopen(url)
    soup = BeautifulSoup(url_open, 'html.parser')
    tag = soup.find("img", {"id": "coverImage"})
    try:
        book['Cover'] = tag['src']
    except:
        print("Book:", url, "found with no cover, try changing edition.")

csv_columns = ["Title"
, "Author"
, "Additional Authors"
, "ISBN"
, "ISBN13"
, "My Rating"
, "Average Rating"
, "Publisher"
, "Binding"
, "Number of Pages"
, "Year Published"
, "Original Publication Year"
, "Date Read"
, "Date Added"
, "Bookshelves"
, "Status"
, "Cover",
"Book Id"]

time_stamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")



with open('with_covers_{}.csv'.format(time_stamp), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in books:
        writer.writerow(data)