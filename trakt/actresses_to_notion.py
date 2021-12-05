import requests, json
from pprint import pprint
from datetime import datetime
from time import sleep
import notion

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
    with open('actresses.json', "r") as f:
        return json.load(f)

def format_notion_data(notion_data):
    actresses = {}
    for act in notion_data:
        trakt_id = act['properties']['Trakt Id']['number']
    
        actresses[trakt_id] = act

    return actresses

def update_record(notion_data, trakt_data):
    diff = compare_data(notion_data, trakt_data)
    
    if len(diff) > 0:
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
        