from re import I
from typing import Counter
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
from time import sleep
import os
import datetime
import tn

CAST = {
    'movies': 'https://api.trakt.tv/people/{}/movies',
    'shows': 'https://api.trakt.tv/people/{}/shows'
}

TRAKT_DOMAIN = 'https://trakt.tv/'

def get_trakt_data(type, id):
    url = CAST[type].format(id)
    headers = {
        'Authorization': 'Bearer {}'.format(trakt.core.OAUTH_TOKEN),
        'Content-Type': 'application/json',
        'trakt-api-version':'2',
        'trakt-api-key':trakt.core.CLIENT_ID
    }

    response = requests.request("GET", url, headers=headers)
    # pprint(response)
    resp = json.loads(response.text)
    # pprint(resp)

    if type == 'movies':
        ids = [cast['movie']['ids']['trakt'] for cast in resp['cast']]
    else:
        ids = [cast['show']['ids']['trakt'] for cast in resp['cast']]

    return ids


def get_cast_creds(id):
    movies = get_trakt_data('movies', id)
    shows = get_trakt_data('shows', id)

    return movies + shows


trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    trakt.core.CLIENT_ID = config["CLIENT_ID"]
    trakt.core.CLIENT_SECRET = config["CLIENT_SECRET"]
    trakt.core.OAUTH_TOKEN = config["OAUTH_TOKEN"]
    trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
    username = config["USERNAME"]

def get_actor_data():
    n_actors_ = tn.get_actresses()
    n_actors = {}
    for item in n_actors_:
        actor = tn.get_props_data(item)
        actor['notion_id'] = item.get('id')
        n_actors[actor['Trakt Id']] = actor

    return n_actors

def get_list_data():
    n_lists_ = tn.get_media()
    n_lists = {}
    for item in n_lists_:
        thing = tn.get_props_data(item)
        thing['notion_id'] = item.get('id')
        n_lists[thing['Trakt Id']] = thing

    return n_lists

def get_notion_ids_for_creds(notion, cast_creds):
    ids = []

    for cred in cast_creds:
        if notion.get(cred):
            ids.append(notion[cred]['notion_id'])

    return ids

n_actors = get_actor_data()
n_lists = get_list_data()

for actor_id in n_actors.keys():
    creds = get_cast_creds(actor_id)
    item_notion_ids = get_notion_ids_for_creds(n_lists, creds)

    if len(item_notion_ids) > 0 and Counter(item_notion_ids) != Counter(n_actors[actor_id]['Roles']):
        to_update = {'Roles': item_notion_ids}
        n_format = tn.dict_to_notion(to_update)
        tn.update_notion(n_actors[actor_id]['notion_id'], n_format)
