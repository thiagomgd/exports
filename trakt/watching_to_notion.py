from re import I
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
from time import sleep
import os
import datetime
import tn

TRAKT_SHOWS = "https://trakt.tv/shows/{}"
TRAKT_MOIES = "https://trakt.tv/movies/{}"
WATCHED_PROGRESS = 'https://api.trakt.tv/shows/{}/progress/watched?hidden=false&specials=false&count_specials=true'
NEXT_EP = 'https://api.trakt.tv/shows/{}/next_episode?extended=full'


TRAKT_DOMAIN = 'https://trakt.tv/'
TRAKT_LINK = 'https://trakt.tv/{media_type}/{slug}'

def get_watched_progress(id):
    # if trakt_id !=145782:
    #     return 99, None 

    url = WATCHED_PROGRESS.format(id)
    headers = {
        'Authorization': 'Bearer {}'.format(trakt.core.OAUTH_TOKEN),
        'Content-Type': 'application/json',
        'trakt-api-version':'2',
        'trakt-api-key':trakt.core.CLIENT_ID
    }

    response = requests.request("GET", url, headers=headers)

    resp = json.loads(response.text)

    aired = resp.get('aired', 0)
    completed = resp.get('completed', 0)
    # next_episode = resp.get('next_episode')

    remaining = aired - completed

    
    # print(aired, completed, remaining)

    if (remaining > 0):
        return remaining, None
    
    response2 = requests.request("GET", NEXT_EP.format(id), headers=headers)
    # print(response2.status_code, response2.text)
    
    if response2.status_code == 204 or not response2.text:
        return remaining, None

    next_info = json.loads(response2.text)
    
    ep_number = next_info.get('number', 99)
    ep_date = next_info.get('first_aired')


    # print(ep_number, ep_date)

    if (ep_number > 1):
        return remaining, None 

    return remaining, ep_date    


trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    trakt.core.CLIENT_ID = config["CLIENT_ID"]
    trakt.core.CLIENT_SECRET = config["CLIENT_SECRET"]
    trakt.core.OAUTH_TOKEN = config["OAUTH_TOKEN"]
    trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
    username = config["USERNAME"]

me = User(username)

things = []

list = me.get_list('watching-now') 
for item in list._items:
    sleep(0.2)
    thing = {}

    if not isinstance(item, TVShow):
        print('SKIPPED:', item.title)
        continue
    
    trakt_id = item.trakt

    remaining, ep_date = get_watched_progress(trakt_id)

    if remaining == 0:
        if item.status in ['cancelled', 'ended']:
            print(item, item.status)
            continue
    
        if ep_date != None:
            print(item.title, ep_date)

            filter = {
                'filter': {
                    'property': 'Trakt Id',
                    'number': {
                        'equals': trakt_id
                    }
                }
            }
            
            notion = tn.get_media(p=filter)

            if not notion or len(notion) != 1:
                print('ooops')
                continue

            nd = tn.get_props_data(notion[0])

            # pprint.pprint(nd)
            # datetime.datetime(2019, 11, 1, 0, 0)
            n_next_date = nd.get('Wait Until')
            t_next_date = datetime.datetime.strptime(ep_date[:10], '%Y-%m-%d')
            
            if not n_next_date or n_next_date != t_next_date:
                print(n_next_date, t_next_date)

                to_update = {'Wait Until': ep_date}
                n_format = tn.dict_to_notion(to_update)
                tn.update_notion(notion[0].get('id'), n_format)