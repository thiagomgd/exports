import requests
import json
import re
from pprint import pprint
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    URLS = {}
    URLS['ANIME'] = config["ANIME_URL"]
    URLS['MANGA'] = config["MANGA_URL"]

    TOKEN = config["NOTION_TOKEN"]

    DATABASES = {}
    DATABASES['ANIME'] = config["ANIME_DB_ID"]
    DATABASES['MANGA'] = config["MANGA_DB_ID"]
    NOTION_URL = "https://api.notion.com/v1/pages/"
    HEADERS = {
        'Authorization': 'Bearer {}'.format(TOKEN),
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'  # '2021-05-13'
    }


def get_notion_data(type, cursor=None, p={}):
    if cursor:
        p["start_cursor"] = cursor

    payload = json.dumps(p)
    headers = {
        'Authorization': 'Bearer {}'.format(TOKEN),
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", URLS[type], headers=headers, data=payload)

    resp = json.loads(response.text)
    # pprint(resp)
    items = resp["results"]

    print(len(items), resp["next_cursor"])

    if resp["has_more"] and resp["next_cursor"]:

        sleep(1)
        items.extend(get_notion_data(type, resp["next_cursor"], p))

    return items


def to_multi(value):
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


def to_select(value):
    if value == '':
        return None

    return {
        "select": {'name': value}
    }


def to_title(value):
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


def to_rich_text(value):
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


def to_date(value):
    if value == '':
        return None

    return {"date": {
        "start": value.replace('/', '-')
    }}


def to_number(value):
    if value == '':
        return None
    return {'number': value}


def to_file_link(value):
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


def to_url(value):
    if value == '':
        return None

    return {
        'url': value
    }

def to_checkbox(value):
    if value == '':
        return None

    return {
        'checkbox': value
    }


def to_none(value):
    return None


def anime_map_to_notion(key, value):
    return {
        'Name': to_title,
        'Cover': to_file_link,
        'Status': to_select,
        'Link': to_url,
        'Genres': to_multi,
        'Tags': to_multi,
        'Format': to_select,
        'Episodes': to_number,
        'Year': to_number,
        'Season': to_select,
        'Anilist Id': to_number,
        'Is Adult': to_checkbox,
        'MAL Link': to_url
    }.get(key)(value)


def manga_map_to_notion(key, value):
    return {
        'Name': to_title,
        'Cover': to_file_link,
        'Status': to_select,
        'Link': to_url,
        'Genres': to_multi,
        'Tags': to_multi,
        'Format': to_select,
        'Volumes': to_number,
        'Chapters': to_number,
        'Year': to_number,
        'Season': to_select,
        'Anilist Id': to_number,
        'Is Adult': to_checkbox,
        'MAL Link': to_url,
        'My Score': to_number,
        'Avg. Score': to_number
    }.get(key)(value)


def dict_to_notion(thing, map_func):
    props = {}
    for key, value in thing.items():
        if value != None:
            prop = map_func(key, value)
            if prop != None:
                props[key] = prop

    return props


def title(prop):
    return prop["title"][0]["plain_text"]


def rich_text(prop):
    return prop["rich_text"][0]["plain_text"] if len(prop["rich_text"]) > 0 else None


def number(prop):
    return prop["number"]

def url(prop):
    return prop["url"]

def checkbox(prop):
    return prop["checkbox"]

def date(prop):
    text = prop["date"]["start"]
    date = datetime.strptime(text, "%Y-%m-%d")
    return date


def files(prop):
    files = prop["files"]

    if len(files) == 0:
        return None

    return files[0]["external"]['url']


def select(prop):
    return prop["select"]["name"]


def multi_select(prop):
    return [x['name'] for x in prop["multi_select"]]

def relation(prop):
    return [x['id'] for x in prop["relation"]]

def get_data(props, name):
    prop = props.get(name, None)

    if prop == None:
        return None

    return {
        "number": number,
        "date": date,
        "files": files,
        "select": select,
        "title": title,
        "rich_text": rich_text,
        'multi_select': multi_select,
        'url': url,
        'checkbox': checkbox,
        'relation': relation
    }.get(prop["type"])(prop)


def get_props_data(item):
    props = item["properties"]

    list = {key: get_data(props, key) for key in props.keys()}

    return list

def insert_notion(db_type, notion_data):
    payload = json.dumps({
        "parent": {
            "database_id": DATABASES[db_type]
        },
        'properties': notion_data
    })

    headers = {
        'Authorization': 'Bearer {}'.format(TOKEN),
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'  # '2021-05-13'
    }

    response = requests.request(
        "POST", NOTION_URL, headers=headers, data=payload)

    # print('insert', notion_data.get('Name'), response.status_code)
    if response.status_code == 400:
        print(response.text)
        pprint(notion_data)
        input('ERROR')
    
    sleep(0.2)

def update_notion(notion_id, notion_data):
    payload = json.dumps({'properties': notion_data})
    req_url = NOTION_URL+notion_id

    response = requests.request(
        "PATCH", req_url, headers=HEADERS, data=payload)

    
    # print('update', notion_data.get('Name'), response.status_code)
    if response.status_code == 400:
        print(response.text)
        input('ERROR')

    sleep(0.2)
