from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
from urllib.parse import urlparse

import csv
import requests
import re

FN = "jav"
TAGS = "JAV"


def get_inches(numbers, idx):
    return round(numbers[idx]/2.54) if idx < len(numbers) else None

def extract_numbers(text):
    # temp = re.findall(r'\d+', text)
    # res = list(map(int, temp))
    res = [int(i) for i in text.split() if i.isdigit()]
    return res[0] if len(res) > 0 else None

def extract_bra(text):
    # temp = re.findall(r'\d+', text)
    # res = list(map(int, temp))
    cup = text[text.find("(")+1:text.find(")")].split()[0]

    temp = re.findall(r'\d+', text)
    res = list(map(int, temp))
    print(text, cup, res)
    size = get_inches(res, 0)
    return str(size) + cup if size else None

def extract_waist(text):
    # temp = re.findall(r'\d+', text)
    # res = list(map(int, temp))
    temp = re.findall(r'\d+', text)
    res = list(map(int, temp))
    return get_inches(res, 1)

def extract_hip(text):
    # temp = re.findall(r'\d+', text)
    # res = list(map(int, temp))
    temp = re.findall(r'\d+', text)
    res = list(map(int, temp))
    return get_inches(res, 2)

def extract_started(text):
    # temp = re.findall(r'\d+', text)
    # res = list(map(int, temp))
    temp = re.findall(r'\d+', text)
    res = list(map(int, temp))
    return res[0] if 0 < len(res) else None

def extract_until(text):
    # temp = re.findall(r'\d+', text)
    # res = list(map(int, temp))
    temp = re.findall(r'\d+', text)
    res = list(map(int, temp))
    return res[1] if 1 < len(res) else None

def extract_status(text):
    return 'active' if text.find("present") else 'retired'

formats = {
    'Age': extract_numbers,
    'Bra': extract_bra,
    'Waist': extract_waist,
    'Hip': extract_hip,
    'Started': extract_started,
    'Until': extract_until,
    'Status': extract_status
}

info = {
    # all div data-source
    'DEFAULT': {
        'Name': 'title1',
        'Birthday': 'born',
        'Country': 'birthplace',
        'Height': 'heght',
        'Hair': 'hair',
        'Eyes': 'eyes',
        'Bra': 'b-w-h',
        'Waist': 'b-w-h',
        'Hip': 'b-w-h',
        'Started': 'years_active',
        'Until': 'years_active',
        'Status': 'years_active'
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

def remove_brackets(text):
    return re.sub("[\(\[].*?[\)\]]", "", text)

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

    for key, source in info['DEFAULT'].items():
        thing = aside.find(attrs={'data-source':source})

        if thing:
            value = thing.select_one('div') or thing
            if value:
                if key in formats:
                    char[key] = formats[key](value.text)
                else:
                    char[key] = remove_brackets(value.text).strip()

    char['Photo'] = get_image(aside)

    gallery_nav = aside.select_one('nav')
    if gallery_nav:
        gallery = gallery_nav.select_one('a')


    # domain = urlparse(link).netloc    
    # char['Gallery'] = "https://" + domain + gallery['href'] if gallery else None

    char['Link'] = link

    el_span = page.find(id='External_Links')
    el_h2 = el_span.parent
    ul = el_h2.find_next('ul')
    links = ul.select('li > a')
    char["Social"] = [a['href'].split('?')[0] for a in links] 

    char["Tags"] = [TAGS]
    pprint(char)
    input('a')
    chars.append(char)
        
    
csv_columns = ['Name','Birthday','Country','Age','Hair','Eyes','Bra','Waist','Hip','Started','Until','Status','Photo','Height','Social']
        
time_stamp =  datetime.now().strftime("%b-%d-%y-%H:%M:%S")

with open('exported_{}_{}.csv'.format(FN, time_stamp), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in chars:
        writer.writerow(data)
