from trakt import init
import trakt.core
from trakt.users import User, UserList
from trakt.movies import Movie
from trakt.tv import TVShow
from pprint import pprint
import csv
import requests
import json
from bs4 import BeautifulSoup
import os
import datetime
import time
from tqdm import tqdm 
import utils 

TRAKT_SHOWS = "https://trakt.tv/shows/{}"
TRAKT_MOVIES = "https://trakt.tv/movies/{}"
TRAKT_DOMAIN = 'https://trakt.tv/'
TRAKT_PERSON = 'https://trakt.tv/people/{}'
TMDB_HEADSHOT = 'https://www.themoviedb.org/person/'
IMDB = 'https://www.imdb.com/name/'
IMDB_DOMAIN = 'https://www.imdb.com'
TWITTER = 'https://twitter.com/'
INSTAGRAM = 'https://www.instagram.com/'

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

def get_trakt_headshot(id):
    url = TRAKT_PERSON.format(id)

    page_data = requests.get(url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    result = page.select_one('div.poster > img.real')

    if (result and result['data-original']):
        return result['data-original']

    return ''

def get_trakt_banner(item):
    if (isinstance(item, TVShow)):
        url = TRAKT_SHOWS.format(item.trakt)
    else:
        url = TRAKT_MOVIES.format(item.trakt)

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
    # # 'secondary-watchlist': 'maybe',
    # # 'actual-watchlist': 'watchil'
    # 'watching-now': 'watching',
    # 'abandoned': 'abandoned',
    # 'on-hold': 'onHold',
    # 'actual-watchlist': 'notStarted',
    # # 'finished-previous': 'watched',
    # 'finished': 'watched'


    'old-stuff': 'old-stuff',
    'brazilian': 'brazilian',
    'memories': 'memories',
    'on-hold': 'on-hold',
    'abandoned': 'abandoned',
    'rewatch': 'rewatch',
    'b-trashy': 'b-trashy',
    'finished': 'finished',
    'r': 'r'
    # 'recommendations-copy': 'favorites'
}

TRAKT_DOMAIN = 'https://trakt.tv/'
TRAKT_LINK = 'https://trakt.tv/{media_type}/{slug}'
IMDB = 'https://www.imdb.com/title/'
IMDB_DOMAIN = 'https://www.imdb.com'

def get_all_trakt():
    print('version', trakt.__version__)
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

    things = {}

    for l in LIST_TO_STATUS.keys():
        print('-'*5, l.ljust(12), '-'*5)
        list = me.get_list(l) 
        # print("ITEMS: ", len(list._items))
        # pprint(list._items[0])
        for item in tqdm(list._items):

        # for watched_shows and watched_movies
        # some attributes are not present (bug on PyTrakt?), so have to comment them below
        # list = me.watched_shows
        # for item in list:

            # pprint.pprint(item)
            thing = {}
            # print(item.slug)

            # for some reason, 1899 is being loaded as this show
            # if 'strangers-with-candy' in item.slug:
            #     continue

            if isinstance(item, Movie):
                thing['type'] = 'Movie'
                thing['premiered'] = item.released

            elif isinstance(item, TVShow):
                thing['type'] = 'TV'
                thing['premiered'] = item.first_aired.strftime('%Y-%m-%d') if item.first_aired else None
                thing['showStatus'] = item.status
                # if l == 'watching-now':
                

            else:
                print('SKIPPED:', item)
                # pprint(item)
                continue

            thing['traktId'] = item.trakt
            thing['tmdbId'] = item.tmdb
            

            thing['name'] = item.title
            thing['status'] = LIST_TO_STATUS[l]
            # pprint.pprint(item)
            thing['country'] =  utils.country_code_to_name(item.country)
            thing['language'] = item.language
            
            thing['genres'] = getattr(item, 'genres', [])
            # if genres:
            #     thing['genres'] = ','.join(genres)
                
            thing['summary'] = item.overview
            thing['runtime'] = item.runtime
            thing['certification'] = item.certification
            # pprint.pprint(vars(item))
            # pprint.pprint(item.ext)
            thing['link'] = TRAKT_DOMAIN + item.ext #TRAKT_LINK.format(**item.__dict__)
            # if 'strangers-with-candy' in thing['Link']:
            #     thing['Link'].replace('strangers-with-candy','1899')
            thing['homepage'] = item.homepage
            thing['year'] = item.year
            thing['where'] = get_network(item)
            

            # thing['Cover'] = get_trakt_banner(item)
            # print(thing['Cover'])
            
            things[str(item.trakt)] = thing

    return things

def get_trakt_actors():
    print('version', trakt.__version__)
    trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        trakt.core.CLIENT_ID = config["CLIENT_ID"]
        trakt.core.CLIENT_SECRET = config["CLIENT_SECRET"]
        trakt.core.OAUTH_TOKEN = config["OAUTH_TOKEN"]
        trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
        username = config["USERNAME"]

    me = User(username)

    people = {}

    actresses_list = me.get_list('actresses') 
    for actor in tqdm(actresses_list._items):
        # print(actor.name)
        person = {}
        
        person['name'] = actor.name
        person['birthday'] = actor.birthday 
        person['country'] = utils.fix_actress_country(actor.birthplace)
        person['profession'] = ['actor']
        person['traktId'] = actor.trakt
        person['tmdbId'] = actor.tmdb
        person['link'] = TRAKT_DOMAIN + actor.ext
        if actor.social_ids:
            person['instagram'] = INSTAGRAM + actor.social_ids['instagram'] if actor.social_ids['instagram'] else ''
            person['twitter'] = TWITTER + actor.social_ids['twitter'] if actor.social_ids['twitter'] else ''
        
        person['photo'] = get_trakt_headshot(actor.trakt)

        people[str(actor.trakt)] = person

    return people
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