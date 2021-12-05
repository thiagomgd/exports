import requests, json
from pprint import pprint
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
import csv 
import notion
import lists

TRAKT_SHOWS = "https://trakt.tv/shows/{}"
TRAKT_MOVIES = "https://trakt.tv/movies/{}"
TYPE = 'MEDIA'

def get_trakt_banner(item):
    if item['Type'] == 'TV':
        url = TRAKT_SHOWS.format(item['Trakt Id'])
    else:
        url = TRAKT_MOVIES.format(item['Trakt Id'])

    page_data = requests.get(url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    result = page.select_one('#summary-wrapper')

    if (result and result['data-fanart']):
        return result['data-fanart']

    return ''

def compare_data(notion_data, trakt_data):
    TO_COMPARE = ['Status', 'Rating']

    stored = notion.get_props_data(notion_data)
    to_update = {}
    
    for key in TO_COMPARE:
        notion_val = stored.get(key)
        trakt_val = trakt_data.get(key)
        if notion_val != trakt_val:
            if key == 'Status' and trakt_val in ['Watching','Maybe', 'Not started'] and notion_val in ['Waiting', 'Next', 'Paused']:
                continue

            # print(key, notion_val, trakt_val)
            # pprint(notion)
            # input('a')
            to_update[key] = trakt_val

    return to_update

# def get_trakt_data():
#     with open('lists.json', "r") as f:
#         return json.load(f)

def format_notion_data(notion_data):
    items = {}
    for act in notion_data:
        trakt_id = act['properties']['Trakt Id']['number']
        items[trakt_id] = act

    return items

def update_record(notion_data, trakt_data):
    diff = compare_data(notion_data, trakt_data)
    
    if len(diff) > 0:
        notion.update_notion(notion_data.get('id'), diff)
        
notion_data = notion.get_notion_data(TYPE)

act_notion = format_notion_data(notion_data)

act_trakt = lists.get_all_trakt()

for trakt in act_trakt:
    if trakt['Trakt Id'] in act_notion:
        update_record(act_notion[trakt['Trakt Id']], trakt)
    else:
        trakt['Cover'] = get_trakt_banner(trakt)
        notion.insert_notion(TYPE, trakt)
        
