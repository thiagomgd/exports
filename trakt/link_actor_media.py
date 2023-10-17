from re import I
from typing import Counter
from trakt import init
import trakt.core
from trakt.users import User, UserList
from trakt.movies import Movie
from trakt.tv import TVShow
from pprint import pprint
import requests
import json
from time import sleep
from tqdm import tqdm
import utils

CAST = {
    'movies': 'https://api.trakt.tv/people/{}/movies',
    'shows': 'https://api.trakt.tv/people/{}/shows'
}

TRAKT_DOMAIN = 'https://trakt.tv/'
ACTORS_FILE = 'actors.json'
MEDIA_FILE = 'media.json'

def load_jsons():
    act = {}
    media = {}

    with open(ACTORS_FILE, 'r') as json_file:
        act = json.load(json_file)

    with open(MEDIA_FILE, 'r') as json_file:
        media = json.load(json_file)

    return media, act

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
        ids = [str(cast['movie']['ids']['trakt']) for cast in resp['cast']]
    else:
        ids = [str(cast['show']['ids']['trakt']) for cast in resp['cast']]

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

def get_notion_ids_for_creds(notion, cast_creds):
    ids = []

    for cred in cast_creds:
        if notion.get(cred):
            ids.append(notion[cred]['notion_id'])

    return ids

media, actors = load_jsons()
delta_creds = 0

for actor_id in tqdm(actors.keys()):
    creds = get_cast_creds(actor_id)
    filteredCreds = []
    cast = []

    for credId in creds:
        if credId in media:
            filteredCreds.append(credId)
            cast.append(utils.format_media_title(media[credId]))

    delta_creds += len(filteredCreds) - len(actors[actor_id].get('castIds',[]))

    actors[actor_id]['cast'] = cast
    actors[actor_id]['castIds'] = filteredCreds

print('delta creds', delta_creds)

with open(ACTORS_FILE, "w") as f:
    json.dump(actors, f, indent=4)
