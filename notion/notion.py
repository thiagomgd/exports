import requests
import json
import re
from pprint import pprint
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen

import os
fname = 'config.json'
this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
wanted_file = os.path.join(this_dir, fname)

with open(wanted_file, 'r') as config_file:
    config = json.load(config_file)

    TOKEN = config["TOKEN"]

    NOTION_URL = "https://api.notion.com/v1/pages/"

    HEADERS = {
        'Authorization': 'Bearer {}'.format(TOKEN),
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'  # '2021-05-13'
    }

    # DATABASES = {}
    # DATABASES['LISTS'] = config["TRAKT_DB_ID"]
    # DATABASES['ACTRESSES'] = config["ACTRESSES_DB_ID"]
    # URLS = {}
    # URLS['ACTRESSES'] = "https://api.notion.com/v1/databases/{}/query".format(DATABASES['ACTRESSES'])
    # URLS['LISTS'] = "https://api.notion.com/v1/databases/{}/query".format(DATABASES['LISTS'])

def get_notion_data(type, cursor=None, p={}):
    # print(type, cursor, p)
    if cursor:
        p["start_cursor"] = cursor

    payload = json.dumps(p)

    response = requests.request(
        "POST", 
        "https://api.notion.com/v1/databases/{}/query".format(config[type]), 
        headers=HEADERS, 
        data=payload
        )

    resp = json.loads(response.text)

    items = resp.get("results")

    if not items:
        print('NO ITEMS')
        pprint(resp)
        return []

    print(len(items), resp.get("next_cursor"))

    if resp["has_more"] and resp["next_cursor"]:
        sleep(1)
        items.extend(get_notion_data(type, resp["next_cursor"], p))

    return items

def insert_notion(type, notion_data):
    payload = json.dumps({
        "parent": {
            "database_id": config[type]
        },
        'properties': dict_to_notion(notion_data)
    })

    response = requests.request(
        "POST", NOTION_URL, headers=HEADERS, data=payload)

    name = notion_data.get('Title') or notion_data.get('Name') or 'Not Found'
    print('insert', name, response.status_code)

    if response.status_code == 400:
        print(response.text)
        pprint(notion_data)
        input('ERROR')
    
    sleep(0.2)

def update_notion(notion_id, notion_data):
    notion_format = dict_to_notion(notion_data)

    # pprint(notion_data)
    # pprint(notion_format)
    # input('------------------------')
    payload = json.dumps({'properties': notion_format})
    req_url = NOTION_URL+notion_id

    response = requests.request(
        "PATCH", req_url, headers=HEADERS, data=payload)

    
    print('update', notion_id, response.status_code)
    if response.status_code == 400:
        print(response.text)
        input('ERROR')

    sleep(0.2)


def dict_to_notion(thing):
    props = {}
    for key, value in thing.items():
        if value != None:
            prop = _map_to_notion(key, value)
            if prop != None:
                props[key] = prop

    return props

def get_props_data(item):
    props = item["properties"]

    list = {key: _get_data(props, key) for key in props.keys()}

    return list

def _to_multi(value):
    if type(value) is str:
        if value == '':
            return None

        values = value.split(',')
    elif type(value) is list:
        if len(value) == 0:
            return None

        values = list(dict.fromkeys(value))

    selected = [{'name': x.strip()} for x in values]

    return {
        "multi_select": selected
    }


def _to_select(value):
    if value == '':
        return None

    return {
        "select": {'name': value}
    }

def _to_status(value):
    if value == '':
        return None

    return {
        "status": {'name': value}
    }

def _to_title(value):
    if value == '':
        return None

    return {"title": [
        {
            "text": {
                "content": value
            }
        }
    ]
    }


def _to_rich_text(value):
    if value == '':
        return None

    return {"rich_text": [
        {
            "text": {
                "content": value
            }
        }
    ]
    }


def _to_date(value):
    if value == '':
        return None

    if type(value) is datetime:
        start = value.strftime("%Y-%m-%d")
    else:
        start = value.replace('/', '-')

    return {"date": {
        "start": start
    }}


def _to_number(value):
    if value == '' or value == None:
        return None
    return {'number': value}


def _to_file_link(value):
    if value == '':
        return None

    return {
        'type': 'files',
                'files': [
                    {
                        "type": "external",
                        "name": 'link',
                        "external": {"url": value}
                    }

                ]}


def _to_url(value):
    if value == '':
        return None

    return {
        'url': value
    }

def _to_relation(ids):
    if ids == '' or ids == []:
        return None

    return {
        'relation': [{'id': id} for id in ids]
    }


def _to_none(value):
    return None


def _title(prop):
    return prop["title"][0]["plain_text"]


def _rich_text(prop):
    return prop["rich_text"][0]["plain_text"] if len(prop["rich_text"]) > 0 else None


def _number(prop):
    return prop["number"]

def _url(prop):
    return prop["url"]

def _checkbox(prop):
    return prop["checkbox"]

def _date(prop):
    dt = prop["date"]

    if dt == None:
        return None 

    text = dt["start"]

    if text == None or text == '':
        return None

    date = datetime.strptime(text[:10], "%Y-%m-%d")
    return date


def _files(prop):
    files = prop["files"]

    if len(files) == 0:
        return None

    file = files[0]
    if 'external' in file:
        return file["external"]['url']
    
    return file['file']['url']


def _select(prop):
    val = prop['select']
    if val == None:
        return None 

    return val["name"]

def _status(prop):
    val = prop['status']
    
    if val == None:
        return None 

    return val["name"]


def _multi_select(prop):
    return [x['name'] for x in prop["multi_select"]]

def _relation(prop):
    return [x['id'] for x in prop["relation"]]

def _created_time(prop):
    return prop["created_time"]

def _last_edited_time(prop):
    return prop["last_edited_time"]

def _formula(prop):
    # TODO: implement
    return None

def _get_data(props, name):
    prop = props.get(name, None)

    if prop == None:
        return None

    # print(name, prop["type"])
    return {
        "number": _number,
        "date": _date,
        "files": _files,
        "select": _select,
        "status": _status,
        "title": _title,
        "rich_text": _rich_text,
        'multi_select': _multi_select,
        'url': _url,
        'checkbox': _checkbox,
        'relation': _relation,
        'created_time': _created_time,
        'formula': _formula,
        'last_edited_time': _last_edited_time
    }.get(prop["type"])(prop)

def _map_to_notion(key, value):
    # print(key, value)

    return {
        # goodreads
        "Title": _to_title,
        "Author": _to_select,
        "Series": _to_select,
        "Type": _to_select,
        "Genres": _to_multi,
        "Additional Authors": _to_multi,
        "ISBN": _to_none,
        "ISBN13": _to_none,
        "My Rating": _to_number,
        "Average Rating": _to_number,
        "Publisher": _to_select,
        "Binding": _to_select,
        "Number of Pages": _to_number,
        "Year Published": _to_number,
        "Original Publication Year": _to_number,
        "Date Read": _to_date,
        "Date Added": _to_date,
        "Bookshelves": _to_multi,
        "Status": _to_status,
        "Cover": _to_file_link,
        "Book Id": _to_number,
        "Number In Series": _to_number,
        "Link": _to_url,
        # trakt - media
        'Name': _to_title,
        'Type': _to_select,
        'Country': _to_select,
        'Status': _to_select,
        'Homepage': _to_url,
        'Genres': _to_multi,
        'Certification': _to_select,
        'Language': _to_select,
        'Runtime': _to_number,
        'Show Status': _to_select,
        'Summary': _to_rich_text,
        'Premiered': _to_date,
        'Year': _to_number,
        'Where': _to_multi,
        'Cover': _to_file_link,
        'Wait Until': _to_date,
        'Rating': _to_number,
        'Trakt Id': _to_number,
        'Roles': _to_relation,
        # trakt - actress
        'Name': _to_title,
        "Birthday": _to_date,
        'Instagram': _to_url,
        'Twitter': _to_url,
        'Profession': _to_multi,
        'Photo': _to_file_link,
        # freeones
        'Ethnicity': _to_select,
        'Eyes': _to_select,
        'Aliases': _to_rich_text,
        'Height': _to_number,
        'Weight': _to_number,
        'Boobs': _to_select, 
        'Bust': _to_number, 
        'Cup': _to_select, 
        'Bra': _to_select,
        'Hair': _to_select,
        'Waist': _to_number,
        'Hip': _to_number,
        'Butt': _to_select,
        'Tattoos': _to_select, 
        'Tattoo Locations': _to_rich_text,
        'Piercings': _to_select,
        'Piercing Locations': _to_rich_text,
        'Started': _to_number,
        'Until': _to_number
    }.get(key)(value)