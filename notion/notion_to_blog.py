import requests, json
from pprint import pprint
from datetime import datetime
from time import sleep

def title(prop):
  return prop["title"][0]["plain_text"]

def number(prop):
  return prop["number"]

def date(prop):
  text = prop["date"]["start"]
  date = datetime.strptime(text, "%Y-%m-%d")
  return date

def files(prop):
  files = prop["files"]

  if len(files) == 0:
    return None

  return files[0]["name"]

def select(prop):
  return prop["select"]["name"]

def get_data(props, name):
  prop = props.get(name, None)

  if prop == None:
    return None

  return {
    "number": number,
    "date": date,
    "files": files,
    "select": select,
    "title": title
  }.get(prop["type"])(prop)

def get_book_data(book):
  b = {}

  props = book["properties"]

  b["author"] = get_data(props, "Author")
  b["cover"] = get_data(props, "Cover")
  b["date_read"] = get_data(props, "Date Read")
  b["rating"] = get_data(props, "My Rating") # or 0
  b["pages"] = get_data(props, "Number of Pages")
  b["original_year"] = get_data(props, "Original Publication Year")
  # status
  b["title"] = get_data(props, "Title")
  b["year_published"] = get_data(props, "Year Published")

  return b
  
def format_item(book):
  f = """ {{{{< card img="{cover}" {badge}>}}}}
#### {title}

{{{{< /card >}}}}


"""
  b["badge"] = ""
  if book["rating"]:
    b["badge"] = 'rating="{}"'.format(book["rating"])

  return f.format(**book)


def get_notion_data(cursor=None):
  with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    url = config["BOOKS_URL"]
    token = config["TOKEN"]

  p = {
    "filter": {
      "property": "Status",
      "select": {
        "equals": "read"
      }
    }
  }

  if cursor:
    p["start_cursor"] = cursor

  payload = json.dumps(p)
  headers = {
    'Authorization': 'Bearer {}'.format(token),
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  resp = json.loads(response.text)
  books = resp["results"]

  print(len(books), resp["next_cursor"])
  if resp["has_more"] and resp["next_cursor"]:
    
    sleep(1)
    books.extend(get_notion_data(resp["next_cursor"]))

  return books

# pprint(books[0])

# pprint(resp["has_more"])
# pprint(resp["next_cursor"])

organized = {}

books = get_notion_data()
print("TOTAL", len(books))

for book in books:
  b = get_book_data(book)
  year = b["date_read"].year if b["date_read"] else 0

  if year not in organized:
    organized[year] = []

  organized[year].append(b)

years = sorted(organized.keys(), reverse=True)

# pprint(years)


text = ""

for year in years:
  year_books = organized[year]
  # pprint(year_books[0])
  l = sorted(year_books, key = lambda i: (i['rating'], i['date_read']), reverse=True)
  text += """### {} 
  
  <div class="cards">
  """.format(year)

  for b in l:
    text += format_item(b)

  text += """
  </div>

  """

with open('books.md', mode='w') as mdfile:
    mdfile.write(text)    