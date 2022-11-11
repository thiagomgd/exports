from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
from urllib.parse import urlparse

import csv
import requests
import re

FN = "dragonmaid"
SERIES = "Miss Kobayashi's Dragon Maid"
MEDIA = "Anime & Manga"


def extract_numbers(text):
    # temp = re.findall(r'\d+', text)
    # res = list(map(int, temp))
    # ress = [int(i) for i in text.split() if i.isdigit()]

    temp = re.findall(r'\d+', text)
    res = list(map(int, temp))
    # print(text, res, ress)
    return res[0] if len(res) > 0 else None

def remove_brackets(text):
    return re.sub("[\(\[].*?[\)\]]", "", text)

formats = {
    'Age': extract_numbers
}

info_dict = {
    # all div data-source
    'DEFAULT': {
        'Name': ['name', 'title'],
        'Age': 'age',
        'Gender': 'gender',
        'Hair': 'hair',
        'Eyes': 'eyes',
        'Height': 'height',
        'Seiyu': 'seiyu', # this is a link
        'Birthday': 'birthday',
        'Alias': 'alias'
    },
    'dragonmaid': {
        'Name': 'name',
        'Age': 'age',
        'Gender': 'gender',
        'Hair': 'hair',
        'Eyes': 'eyes',
        'Seiyu': 'seiyu', # this is a link
    },
    'mha': {
        'Name': 'name',
        'Age': 'age',
        'Gender': 'gender', # remove link
        'Hair': 'hair',
        'Eyes': 'eyes',
        'Height': 'height',
        # 'Seiyu': 'seiyu', # different structure # this is a link
        'Birthday': 'birthday',
        'Alias': 'alias'
    }
}

def get_image(aside):
    img = aside.select_one('figure > a')
    full = img['href']
    full_lower = full.lower()
    if full_lower.find('.jpg') > 0:
        pos = full_lower.find('.jpg') + 4
    elif full_lower.find('.png') > 0:
        pos = full_lower.find('.png') + 4
    elif full.find('.jpeg') > 0:
        pos = full_lower.find('.jpeg') + 5

    if pos:
        return full[:pos]
    
    return None

with open('{}.csv'.format(FN)) as f:
    links = [line.strip() for line in f]

chars = []

info = info_dict[FN] if FN in info_dict else info_dict['DEFAULT']

for link in links:
    print(link)

    page_data = requests.get(link)

    page = BeautifulSoup(page_data.content, 'html.parser')

    aside = page.select_one("aside.portable-infobox")

    # pprint(aside)

    char = {}
    if (aside == None):
        print('SKIPPING: ', link)
        break

    for key, source in info.items():
        thing = aside.find(attrs={'data-source':source})

        if thing:
            value = thing.select_one('div') or thing
            if value:
                if key in formats:
                    char[key] = formats[key](value.text)
                else:
                    char[key] = remove_brackets(value.text).strip()

    char['Cover'] = get_image(aside)

    gallery_nav = aside.select_one('nav')
    if gallery_nav:
        gallery = gallery_nav.select_one('a')

        domain = urlparse(link).netloc    
        char['Gallery'] = "https://" + domain + gallery['href'] if gallery else None

    char['Series'] = SERIES

    char['Fandom'] = link

    pprint(char)
    # input('a')
    chars.append(char)
        
    
csv_columns = ['Name','Series','Age','Gender','Hair','Eyes','Seiyu','Fandom','Cover','Gallery', 'Birthday', 'Height', 'Alias']
time_stamp =  datetime.now().strftime("%b-%d-%y-%H:%M:%S")

with open('exported_{}_{}.csv'.format(FN, time_stamp), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in chars:
        writer.writerow(data)
