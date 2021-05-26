# import trakt
from trakt import init
import trakt.core
# from trakt.people import Person
from trakt.users import User, UserList
from pprint import pprint
import csv
import requests
import json
import datetime
from bs4 import BeautifulSoup

TRAKT_DOMAIN = 'https://trakt.tv/'
TRAKT_PERSON = 'https://trakt.tv/people/{}'
TMDB_HEADSHOT = 'https://www.themoviedb.org/person/'
IMDB = 'https://www.imdb.com/name/'
IMDB_DOMAIN = 'https://www.imdb.com'
TWITTER = 'https://twitter.com/'
INSTAGRAM = 'https://www.instagram.com/'

trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH 
trakt.core.CLIENT_ID = ''
trakt.core.CLIENT_SECRET = ''
trakt.core.OAUTH_TOKEN = ''

# def headshot_img(tag):
#     return tag.name == 'img' and tag.class_ == "profile lazyload lazyloaded"

# def get_tmdb_headshot(id):
#     url = TMDB_HEADSHOT + str(id)
#     print(url)
#     page_data = requests.get(url)
#     # pprint.pprint(page_data)
#     page = BeautifulSoup(page_data.content, 'html.parser')
#     pprint.pprint(page)
#     result = page.find_all('img.profile') # headshot_img)
#     pprint.pprint(result)
#     # pprint.pprint(result.src)

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

me = User('')

people = []

actresses_list = me.get_list('actresses') 

for actor in actresses_list._items:
    print(actor.name)
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

csv_columns = ['Name','Birthday','Country','Profession','Link','Instagram','Twitter', 'Photo', "Trakt Id"]

time_stamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")

with open('export/actresses_{}.csv'.format(time_stamp), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in people:
        writer.writerow(data)
