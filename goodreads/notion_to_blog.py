import requests
import json
import bn
from pprint import pprint
from datetime import datetime
from time import sleep

def format_item(book):
    f = """ {{{{< card img="{Cover}" {Badge}>}}}}
#### {Title} <br/>
{review_link}
{{{{< /card >}}}}


"""
    book["Badge"] = ""
    book["review_link"] = ""

    if book.get("My Rating"):
        book["Badge"] = 'rating="{}"'.format(book["My Rating"])

    if book.get("Review"):
        book["review_link"] = f'<a href="{book["Review"]}">Review</a>'

    return f.format(**book)


organized = {}
p = {
        "filter": {
            "property": "Status",
            "select": {
                "equals": "read"
            }
        }
    }

books = bn.get_notion_data(p=p)
print("TOTAL", len(books))

for book in books:
    b = bn.get_props_data(book)

    if b.get('Type') in ['manga', 'comic']:
        continue

    
    year = b["Date Read"].year if b.get("Date Read") else 0

    if year not in organized:
        organized[year] = []

    organized[year].append(b)

years = sorted(organized.keys(), reverse=True)

# pprint(years)


text = ""

for year in years:
    year_books = organized[year]
    # pprint(year_books[0])
    l = sorted(year_books, key=lambda i: (
        i.get('My Rating'), i.get('Date Read')), reverse=True)
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
