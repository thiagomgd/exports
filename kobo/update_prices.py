import requests
import json
import re
from pprint import pprint
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
from tqdm import tqdm

WISHLIST = [
    "https://www.kobo.com/ca/en/ebook/stellarlune-1",
    "https://www.kobo.com/ca/en/ebook/ghostly-echoes-5",
    "https://www.kobo.com/ca/en/ebook/catfish-rolling-2",
    "https://www.kobo.com/ca/en/ebook/on-the-edge-of-gone",
    "https://www.kobo.com/ca/en/ebook/earthlings-3",
    "https://www.kobo.com/ca/en/ebook/convenience-store-woman-6",
    "https://www.kobo.com/ca/en/ebook/mieruko-chan-vol-7",
    "https://www.kobo.com/ca/en/ebook/dandadan-vol-2",
    "https://www.kobo.com/ca/en/ebook/she-is-a-haunting-1",
    "https://www.kobo.com/ca/en/ebook/fractal-noise",
    "https://www.kobo.com/ca/en/ebook/an-accident-of-stars",
    "https://www.kobo.com/ca/en/ebook/monstrous-heart-the-deepwater-trilogy-book-1-1",
    "https://www.kobo.com/ca/en/ebook/wild-and-wicked-things-1",
    "https://www.kobo.com/ca/en/ebook/unseelie-2",
    "https://www.kobo.com/ca/en/ebook/delicious-in-dungeon-vol-11",
    "https://www.kobo.com/ca/en/ebook/black-tide-27",
    "https://www.kobo.com/ca/en/ebook/house-of-suns-2",
    "https://www.kobo.com/ca/en/ebook/home-before-dark-22",
    "https://www.kobo.com/ca/en/ebook/children-of-time-3",
    "https://www.kobo.com/ca/en/ebook/dead-silence-27",
    "https://www.kobo.com/ca/en/ebook/ghost-girl-17",
    "https://www.kobo.com/ca/en/ebook/ghostlight-6",
    "https://www.kobo.com/ca/en/ebook/monster-club-1-1"
]


books = []

for url in WISHLIST:
    print("url", url)
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    url_open = urllib.request.urlopen(req)
    # url_open = urlopen(url)
    soup = BeautifulSoup(url_open, 'html.parser')

    title = soup.select_one("h1.title").text
    price = soup.select_one("div.active-price").text
    cover = soup.select_one("img.cover-image").href

    print(title, price, cover)
    # h1.title
    # div.active-price
    # img.cover-image
