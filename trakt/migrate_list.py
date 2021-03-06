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
import os

# LIST = 'watched_shows'
LIST = 'watchlistprev'

trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    trakt.core.CLIENT_ID = config["CLIENT_ID"]
    trakt.core.CLIENT_SECRET = config["OAUTH_TOKEN"]
    trakt.core.OAUTH_TOKEN = config["OAUTH_TOKEN"]
    username = config["USERNAME"]

me = User(username)


# for watched_shows and watched_movies
watchlist = me.watchlist_movies

print(len(watchlist))
# for item in watchlist:
    # print(item.title)
    # pprint.pprint(item)
    # list.add_items([item])
list = me.get_list(LIST) 

list.add_items(*watchlist)

for item in list._items:
    pprint.pprint(item)
