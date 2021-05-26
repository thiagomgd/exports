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
USERNAME = ''

trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 
trakt.core.CLIENT_ID = ''
trakt.core.CLIENT_SECRET = ''
trakt.core.OAUTH_TOKEN = ''

me = User(USERNAME)


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
