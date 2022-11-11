from os import stat
from bs4 import BeautifulSoup
import requests
import json, datetime, csv, tqdm
from pprint import pprint

fname = 'saved_feedly'

def selectonetext(page, label):
    itm = page.select_one(label)
    return itm.text if itm else None


with open("{}.html".format(fname)) as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    # print(soup)

saved = soup.select('div.content > a.entry__title')

print(len(saved))

articles = []

for itm in saved:
    articles.append({'url': itm["href"]})
    

csv_columns = ['url']
time_stamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")

with open('{}_{}.csv'.format(fname, time_stamp), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in articles:
        writer.writerow(data)