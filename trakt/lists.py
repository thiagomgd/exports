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

TRAKT_SHOWS = "https://trakt.tv/shows/{}"
TRAKT_MOIES = "https://trakt.tv/movies/{}"

# def get_imdb_img(id):
#     url = IMDB + str(id)
#     page_data = requests.get(url)
#     page = BeautifulSoup(page_data.content, 'html.parser')

#     result = page.select_one('div.poster a')

#     if (result and result['href']):
#         gallery_data = requests.get(IMDB_DOMAIN + result['href'])
#         gallery_page = BeautifulSoup(gallery_data.content, 'html.parser')

#         img_id = result['href'].split('/')[-1].split('?')[0] + '-curr'
        
#         img = gallery_page.find(attrs={'data-image-id':img_id})
#         return img['src'].replace('"', '') if img else ''

#     result = page.select_one('div.poster a img')
#     return result['src'].replace('"', '') if result else ''

def get_trakt_banner(item):
    if (isinstance(item, TVShow)):
        url = TRAKT_SHOWS.format(item.trakt)
    else:
        url = TRAKT_MOIES.format(item.trakt)

    page_data = requests.get(url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    result = page.select_one('#summary-wrapper')

    if (result and result['data-fanart']):
        return result['data-fanart']

    return ''

def get_network(item):
    if (isinstance(item, TVShow) and item.network == 'Netflix') or (item.homepage and 'netflix' in item.homepage):
        return 'Netflix'
    elif (isinstance(item, TVShow) and item.network == 'Amazon') or (item.homepage and ('primevideo' in item.homepage or 'amazon' in item.homepage)):
        return 'Amazon'
    elif (isinstance(item, TVShow) and item.network == 'Apple TV+') or (item.homepage and 'tv.apple.com' in item.homepage):
        return 'Apple TV+'
    elif (isinstance(item, TVShow) and item.network == 'Disney+') or (item.homepage and 'disneyplus' in item.homepage):
        return 'Disney+'
    return ''

LIST_TO_STATUS = {
    'secondary-watchlist': 'Maybe',
    'watching-now': 'Watching',
    'abandoned': 'Abandoned',
    'paused': 'Paused',
    'on-hold': 'On Hold',
    'finished': 'Watched',
    'actual-watchlist': 'Not started'
}

TRAKT_DOMAIN = 'https://trakt.tv/'
TRAKT_LINK = 'https://trakt.tv/{media_type}/{slug}'
IMDB = 'https://www.imdb.com/title/'
IMDB_DOMAIN = 'https://www.imdb.com'

def get_all_trakt():
    trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        trakt.core.CLIENT_ID = config["CLIENT_ID"]
        trakt.core.CLIENT_SECRET = config["CLIENT_SECRET"]
        trakt.core.OAUTH_TOKEN = config["OAUTH_TOKEN"]
        trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
        username = config["USERNAME"]

    me = User(username)
    # print(me.lists)

    things = []

    for l in LIST_TO_STATUS.keys():
        # print('-'*5, l.ljust(12), '-'*5)
        list = me.get_list(l) 
        for item in list._items:

        # for watched_shows and watched_movies
        # some attributes are not present (bug on PyTrakt?), so have to comment them below
        # list = me.watched_shows
        # for item in list:

            # pprint.pprint(item)
            thing = {}

            if isinstance(item, Movie):
                thing['Type'] = 'Movie'
                thing['Premiered'] = item.released

            elif isinstance(item, TVShow):
                thing['Type'] = 'TV'
                thing['Premiered'] = item.first_aired.strftime('%Y-%m-%d') if item.first_aired else None
                thing['Show Status'] = item.status

            else:
                print('SKIPPED:', item.title)
                continue

            thing['Trakt Id'] = item.trakt

            thing['Name'] = item.title
            thing['Status'] = LIST_TO_STATUS[l]
            # pprint.pprint(item)
            thing['Country'] =  item.country
            thing['Language'] = item.language
            
            genres = getattr(item, 'genres', [])
            if genres:
                thing['Genres'] = ','.join(genres)
                
            thing['Summary'] = item.overview
            thing['Runtime'] = item.runtime
            thing['Certification'] = item.certification
            # pprint.pprint(vars(item))
            # pprint.pprint(item.ext)
            thing['Link'] = TRAKT_DOMAIN + item.ext #TRAKT_LINK.format(**item.__dict__)
            thing['Homepage'] = item.homepage
            thing['Year'] = item.year
            
            thing['Where'] = get_network(item)
            

            # thing['Cover'] = get_trakt_banner(item)
            # print(thing['Cover'])
            
            things.append(thing)

    return things

# with open('lists.json', "w") as f:
#         json.dump(things, f, indent=4)
        


# used for watched_shows and watched_movies. 
# Export to html, so I can fix them into 'finished' or other status
# watched_shows returns shows I've watched at least one episode, not completed shows.
# def trakt_url(name, url):
#     return '<a href="%s">%s</a><br>' % (url, name)

# with open('{}.html'.format(LIST), mode='w') as htmlfile:
#     for thing in things:
#         htmlfile.write(trakt_url(thing['Name'], thing['Link']) + os.linesep)    