import requests
from pprint import pprint

headers = {
    'User-Agent': 'FooBarApp/3.0',
}

info = requests.get('https://api.discogs.com/releases/249504', headers)
pprint(info.json())
