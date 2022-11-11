from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
from urllib.parse import urlparse

import csv
import requests

FN = "mha"
SERIES = "My Hero Academia"
MEDIA = "Anime & Manga"


def extract_numbers(text):
    # temp = re.findall(r'\d+', text)
    # res = list(map(int, temp))
    res = [int(i) for i in text.split() if i.isdigit()]
    return res[0] if len(res) > 0 else None

formats = {
    'Age': extract_numbers
}

info = {
    # all div data-source
    'DEFAULT': {
        'Name': 'name',
        'Age': 'age',
        'Gender': 'gender',
        'Hair': 'hair',
        'Eyes': 'eyes',
        'Seiyu': 'seiyu', # this is a link
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
        'Birthday': 'birthday'
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

    for key, source in info[FN].items():
        thing = aside.find(attrs={'data-source':source})

        if thing:
            value = thing.select_one('div') or thing
            if value:
                if key in formats:
                    char[key] = formats[key](value.text)
                else:
                    char[key] = value.text

    char['Cover'] = get_image(aside)

    gallery_nav = aside.select_one('nav')
    if gallery_nav:
        gallery = gallery_nav.select_one('a')


    domain = urlparse(link).netloc    
    char['Gallery'] = "https://" + domain + gallery['href'] if gallery else None

    char['Series'] = SERIES

    char['Fandom'] = link

    # pprint(char)
    # input('a')
    chars.append(char)
        
    
csv_columns = ['Name','Series','Age','Gender','Hair','Eyes','Seiyu','Fandom','Cover','Gallery', 'Birthday', 'Height']
time_stamp =  datetime.now().strftime("%b-%d-%y-%H:%M:%S")

with open('exported_{}_{}.csv'.format(FN, time_stamp), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in chars:
        writer.writerow(data)
