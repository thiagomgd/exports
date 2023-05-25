from os import stat
from bs4 import BeautifulSoup
import requests
import json, datetime, csv
from pprint import pprint

fname = 'watchlater2'
FOLDER = 'Watch Later'

# def selectonetext(page, label):
#     itm = page.select_one(label)
#     return itm.text if itm else None

def getTags(item):
    tags = ["Youtube", "Video"]

    channel = item.select("ytd-channel-name #tooltip")[0]
    # pprint(item)
    # print('----------------------------')
    # pprint(channel)

    tags.append('YT: ' + channel.text.strip())
    return ", ".join(tags)

def getUrl(item):
    fullurl = item.find(id='video-title')['href']
    # https://www.youtube.com/watch?v=rJVYb2Ib8DU&list=WL&index=11
    parts = fullurl.split('?')
    params = parts[1].split('&')
    videoId = ''
    for param in params:
        if param.startswith('v='):
            videoId=param
            break

    return parts[0] + '?' + videoId

with open("{}.html".format(fname)) as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    # print(soup)

saved = soup.select('ytd-playlist-video-renderer div[id="meta"]')

print(len(saved))

articles = []

for itm in saved:
    url = getUrl(itm)
    tags = getTags(itm)
    articles.append({'folder': FOLDER,'url': url, 'tags':tags})

csv_columns = ['url','folder','tags']
# time_stamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")

# with open('{}_{}.csv'.format(fname, time_stamp), mode='w') as csvfile:
with open('{}.csv'.format(fname), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in articles:
        writer.writerow(data)