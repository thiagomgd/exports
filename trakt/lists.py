from trakt import init
import trakt.core
from trakt.users import User, UserList
from trakt.movies import Movie
from trakt.tv import TVShow
import pprint
import csv
import requests
import json
from bs4 import BeautifulSoup
import os
import datetime

def get_imdb_img(id):
    url = IMDB + str(id)
    page_data = requests.get(url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    result = page.select_one('div.poster a')

    if (result and result['href']):
        gallery_data = requests.get(IMDB_DOMAIN + result['href'])
        gallery_page = BeautifulSoup(gallery_data.content, 'html.parser')

        img_id = result['href'].split('/')[-1].split('?')[0] + '-curr'
        
        img = gallery_page.find(attrs={'data-image-id':img_id})
        return img['src'].replace('"', '') if img else ''

    result = page.select_one('div.poster a img')
    return result['src'].replace('"', '') if result else ''



# LIST = 'watched_shows'
# LIST = 'on-hold'
# STATUS = 'Paused'

# LIST = 'watching-now'
# STATUS = 'Watching'

# LIST = 'abandoned'
# STATUS = 'Abandoned'

LIST = 'finished'
STATUS = 'Finished'

TRAKT_DOMAIN = 'https://trakt.tv/'
TRAKT_LINK = 'https://trakt.tv/{media_type}/{slug}'
IMDB = 'https://www.imdb.com/title/'
IMDB_DOMAIN = 'https://www.imdb.com'

trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    trakt.core.CLIENT_ID = config["CLIENT_ID"]
    trakt.core.CLIENT_SECRET = config["OAUTH_TOKEN"]
    trakt.core.OAUTH_TOKEN = config["OAUTH_TOKEN"]
    username = config["USERNAME"]

me = User(username)

things = []

list = me.get_list(LIST) 
for item in list._items:

# for watched_shows and watched_movies
# some attributes are not present (bug on PyTrakt?), so have to comment them below
# list = me.watched_shows
# for item in list:

    pprint.pprint(item)
    thing = {}

    if isinstance(item, Movie):
        thing['Type'] = 'Movie'
        thing['Premiered'] = item.released

    elif isinstance(item, TVShow):
        thing['Type'] = 'TV'
        thing['Premiered'] = item.first_aired.strftime('%Y-%m-%d')
        thing['Show Status'] = item.status

    else:
        print('SKIPPED:', item.title)
        continue

    thing['Trakt Id'] = item.trakt

    thing['Name'] = item.title
    thing['Status'] = STATUS
    thing['Country'] =  item.country
    thing['Language'] = item.language
    
    genres = getattr(item, 'genres', [])
    if genres:
        thing['Tags'] = ','.join(genres)
        
    thing['Summary'] = item.overview
    thing['Runtime'] = item.runtime
    thing['Certification'] = item.certification
    thing['Link'] = TRAKT_LINK.format(**item.__dict__)
    thing['Homepage'] = item.homepage
    thing['Year'] = item.year
    
    if (isinstance(item, TVShow) and item.network == 'Netflix') or (item.homepage and 'netflix' in item.homepage):
        thing['Where'] = 'Netflix'
    elif (isinstance(item, TVShow) and item.network == 'Amazon') or (item.homepage and ('primevideo' in item.homepage or 'amazon' in item.homepage)):
        thing['Where'] = 'Amazon'
    else:
        thing['Where'] = ''

    thing['Cover'] = get_imdb_img(item.imdb)
    
    things.append(thing)

csv_columns = ['Name', 'Type', 'Country', 'Language', 'Status', 'Runtime', 'Link', 'Homepage', 'Cover', 'Show Status', 'Tags', 'Premiered', 'Year', 'Certification', 'Where', 'Summary', "Trakt Id"]

time_stamp =  datetime.datetime.now().strftime("%b-%d-%y--%H-%M-%S")

with open('export/{}_{}.csv'.format(LIST, time_stamp), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in things:
        writer.writerow(data)


# used for watched_shows and watched_movies. 
# Export to html, so I can fix them into 'finished' or other status
# watched_shows returns shows I've watched at least one episode, not completed shows.
# def trakt_url(name, url):
#     return '<a href="%s">%s</a><br>' % (url, name)

# with open('{}.html'.format(LIST), mode='w') as htmlfile:
#     for thing in things:
#         htmlfile.write(trakt_url(thing['Name'], thing['Link']) + os.linesep)    