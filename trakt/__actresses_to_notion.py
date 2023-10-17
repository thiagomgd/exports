import requests, json
from pprint import pprint
from datetime import datetime
from time import sleep
import notion
from trakt import init
import trakt.core
from trakt.users import User, UserList
import requests
import json
from bs4 import BeautifulSoup

TRAKT_DOMAIN = 'https://trakt.tv/'
TRAKT_PERSON = 'https://trakt.tv/people/{}'
TMDB_HEADSHOT = 'https://www.themoviedb.org/person/'
IMDB = 'https://www.imdb.com/name/'
IMDB_DOMAIN = 'https://www.imdb.com'
TWITTER = 'https://twitter.com/'
INSTAGRAM = 'https://www.instagram.com/'

def get_imdb_headshot(id):
    url = IMDB + str(id)
    page_data = requests.get(url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    result = page.select_one('div.poster-hero-container > div.image > a')

    if (result and result['href']):
        gallery_data = requests.get(IMDB_DOMAIN + result['href'])
        gallery_page = BeautifulSoup(gallery_data.content, 'html.parser')

        img_id = result['href'].split('/')[-1].split('?')[0] + '-curr'
        
        img = gallery_page.find(attrs={'data-image-id':img_id})
        return img['src'].replace('"', '') if img else ''

    result = page.find(id='name-poster')
    return result['src'].replace('"', '') if result else ''

def get_trakt_headshot_imgur(id):
    url = TRAKT_PERSON.format(id)

    page_data = requests.get(url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    result = page.select_one('div.poster > img.real')

    if (result and result['data-original']):
        return result['data-original']

    return ''


with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    trakt.core.CLIENT_ID = config["CLIENT_ID"]
    trakt.core.CLIENT_SECRET = config["CLIENT_SECRET"]
    trakt.core.OAUTH_TOKEN = config["OAUTH_TOKEN"]
    username = config["USERNAME"]

def compare_data(notion_data, trakt_data):
    TO_COMPARE = ['Twitter', 'Instagram', 'Photo']
    stored = notion.get_props_data(notion_data)
    # print('Comparing', stored.keys())
    to_update = {}

    for key in TO_COMPARE:
        notion_val = stored.get(key)
        trakt_val = trakt_data.get(key)
        if notion_val != trakt_val:
            if key == 'Photo':
                if notion_val != None and 'trakt.tv' not in notion_val:
                    continue
        
            to_update[key] = trakt_val


    return to_update
        

def get_trakt_data():
    trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 
    # print(init(username, client_id=config["CLIENT_ID"], client_secret=config["CLIENT_SECRET"]))
    # print('a', trakt.core.OAUTH_TOKEN)
    me = User(username)

    people = []

    actresses_list = me.get_list('actresses') 
    for actor in actresses_list._items:
        # print(actor.name)
        person = {}
        
        person['Name'] = actor.name
        person['Birthday'] = actor.birthday 
        person['Country'] = actor.birthplace.split(',')[-1].strip() if actor.birthplace else "?"
        person['Profession'] = 'actor'
        person['Trakt Id'] = actor.trakt
        person['Link'] = TRAKT_DOMAIN + actor.ext
        if actor.social_ids:
            person['Instagram'] = INSTAGRAM + actor.social_ids['instagram'] if actor.social_ids['instagram'] else ''
            person['Twitter'] = TWITTER + actor.social_ids['twitter'] if actor.social_ids['twitter'] else ''
        
        person['Photo'] = get_trakt_headshot_imgur(actor.trakt)

        people.append(person)

    return people


def format_notion_data(notion_data):
    actresses = {}
    for act in notion_data:
        trakt_id = act['properties']['Trakt Id']['number']
    
        actresses[trakt_id] = act

    return actresses

def update_record(notion_data, trakt_data):
    diff = compare_data(notion_data, trakt_data)
    
    if len(diff) > 0:
        pprint(diff)
        notion.update_notion(notion_data.get('id'), diff)
        
notion_data = notion.get_notion_data('ACTRESSES')
act_notion = format_notion_data(notion_data)
act_trakt = get_trakt_data()

for trakt in act_trakt:
    trakt_id = trakt['Trakt Id']

    if trakt_id in act_notion:
        update_record(act_notion[trakt_id], trakt)
 
    else:
        notion.insert_notion('ACTRESSES', trakt)
        