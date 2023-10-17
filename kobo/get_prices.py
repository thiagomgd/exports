from pathlib import Path
from urllib.request import urlopen
from pprint import pprint
# from tqdm import tqdm
from time import sleep
# from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By

import json

options = FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path="/opt/homebrew/bin/geckodriver", options=options)

MAIN_DIR = '/Users/thiago/git/geekosaurblog/src/_data/'

AVAILABLE_VPL = [
"https://www.kobo.com/ca/en/ebook/ghostlight-6",
"https://www.kobo.com/ca/en/ebook/black-sun-27"
]
    
MANGA_COMICS = [
    "https://www.kobo.com/ca/en/ebook/mieruko-chan-vol-7",
    "https://www.kobo.com/ca/en/ebook/delicious-in-dungeon-vol-11",
    "https://www.kobo.com/ca/en/ebook/pretty-guardian-sailor-moon-eternal-edition-1",
    "https://www.kobo.com/ca/en/ebook/the-woods-vol-6",
    "https://www.kobo.com/ca/en/ebook/call-of-the-night-vol-1",
    "https://www.kobo.com/ca/en/ebook/don-t-toy-with-me-miss-nagatoro-4",
    "https://www.kobo.com/ca/en/ebook/my-monster-secret-vol-1",
    # "https://www.kobo.com/ca/en/ebook/yozakura-quartet-1-1",
    "https://www.kobo.com/ca/en/ebook/air-gear-omnibus-3-1"
]

LIGHT_NOVELS = [
    "https://www.kobo.com/ca/en/ebook/alya-sometimes-hides-her-feelings-in-russian-vol-1",
    "https://www.kobo.com/ca/en/ebook/looks-are-all-you-need-vol-1",
    "https://www.kobo.com/ca/en/ebook/liar-liar-vol-1",
    "https://www.kobo.com/ca/en/ebook/konosuba-god-s-blessing-on-this-wonderful-world-trpg",
    "https://www.kobo.com/ca/en/ebook/re-zero-starting-life-in-another-world-vol-1-light-novel-2",
    "https://www.kobo.com/ca/en/ebook/high-school-dxd-vol-1-1",
    "https://www.kobo.com/ca/en/ebook/konosuba-god-s-blessing-on-this-wonderful-world-fantastic-days",
    "https://www.kobo.com/ca/en/ebook/orc-eroica-vol-1-light-novel",
    "https://www.kobo.com/ca/en/ebook/mushoku-tensei-jobless-reincarnation-light-novel-vol-4",
    "https://www.kobo.com/ca/en/ebook/secrets-of-the-silent-witch-vol-1",
    "https://www.kobo.com/ca/en/ebook/dragon-and-ceremony-vol-1-light-novel",
    "https://www.kobo.com/ca/en/ebook/when-supernatural-battles-became-commonplace-volume-1",
    "https://www.kobo.com/ca/en/ebook/spice-and-wolf-vol-3-light-novel-2",
    "https://www.kobo.com/ca/en/ebook/irina-the-vampire-cosmonaut-light-novel-vol-1",
    "https://www.kobo.com/ca/en/ebook/reign-of-the-seven-spellblades-vol-1-light-novel",
    "https://www.kobo.com/ca/en/ebook/slayers-volume-1",
    "https://www.kobo.com/ca/en/ebook/durarara-vol-2-light-novel-2",
    "https://www.kobo.com/ca/en/ebook/full-clearing-another-world-under-a-goddess-with-zero-believers-manga-volume-1",
    "https://www.kobo.com/ca/en/ebook/bottom-tier-character-tomozaki-vol-4-light-novel",
]

WISHLIST = [
    "https://www.kobo.com/ca/en/ebook/the-stars-undying",
    "https://www.kobo.com/ca/en/ebook/the-mad-women-s-ball-1"
    "https://www.kobo.com/ca/en/ebook/the-rise-and-fall-of-the-dinosaurs",
    "https://www.kobo.com/ca/en/ebook/the-apollo-murders-1",
    "https://www.kobo.com/ca/en/ebook/drinks-and-sinkholes",
    "https://www.kobo.com/ca/en/ebook/emily-wilde-s-encyclopaedia-of-faeries-1",
    "https://www.kobo.com/ca/en/ebook/can-t-spell-treason-without-tea",
    "https://www.kobo.com/ca/en/ebook/the-lost-girl-king",
    "https://www.kobo.com/ca/en/ebook/the-keeper-s-six",
    "https://www.kobo.com/ca/en/ebook/the-mountain-in-the-sea",
    "https://www.kobo.com/ca/en/ebook/extremely-online",
    "https://www.kobo.com/ca/en/ebook/improbable-magic-for-cynical-witches",
    "https://www.kobo.com/ca/en/ebook/life-s-edge",
    "https://www.kobo.com/ca/en/ebook/wild-born-spirit-animals-book-1",
    "https://www.kobo.com/ca/en/ebook/the-storm-keeper-s-island-1",
    "https://www.kobo.com/ca/en/ebook/the-drowned-woods",
    "https://www.kobo.com/ca/en/ebook/front-desk-front-desk-1-scholastic-gold",
    "https://www.kobo.com/ca/en/ebook/charmed-life-the-chrestomanci-series-book-1",
    "https://www.kobo.com/ca/en/ebook/magic-kingdom-for-sale-sold-1",
    "https://www.kobo.com/ca/en/ebook/joust-3",
    "https://www.kobo.com/ca/en/ebook/crystal-singer",
    "https://www.kobo.com/ca/en/ebook/spellsinger-1",
    "https://www.kobo.com/ca/en/ebook/the-lark-and-the-wren",
    "https://www.kobo.com/ca/en/ebook/beyond-104",
    "https://www.kobo.com/ca/en/ebook/dead-country-3",
    "https://www.kobo.com/ca/en/ebook/what-the-river-knows-2",
    "https://www.kobo.com/ca/en/ebook/a-study-in-drowning-1",
    "https://www.kobo.com/ca/en/ebook/vampires-of-el-norte",
    "https://www.kobo.com/ca/en/ebook/contact-37",
    "https://www.kobo.com/ca/en/ebook/the-space-between-us-30",
    "https://www.kobo.com/ca/en/ebook/a-curious-beginning",
    "https://www.kobo.com/ca/en/ebook/the-culture-code-2",
    "https://www.kobo.com/ca/en/ebook/call-me-a-cab",
    "https://www.kobo.com/ca/en/ebook/effortless-8",
    "https://www.kobo.com/ca/en/ebook/silver-in-the-bone",
    "https://www.kobo.com/ca/en/ebook/the-isles-of-the-gods-1",
    "https://www.kobo.com/ca/en/ebook/sister-maiden-monster",
    "https://www.kobo.com/ca/en/ebook/the-enigma-of-room-622-1",
    "https://www.kobo.com/ca/en/ebook/the-merry-dredgers",
    "https://www.kobo.com/ca/en/ebook/itchy-tasty",
    "https://www.kobo.com/ca/en/ebook/these-fleeting-shadows",
    "https://www.kobo.com/ca/en/ebook/perry-rhodan-neo-volume-4-english-edition",
    "https://www.kobo.com/ca/en/ebook/peter-and-the-starcatchers-1",
    "https://www.kobo.com/ca/en/ebook/the-sun-and-the-void-1",
    "https://www.kobo.com/ca/en/ebook/the-winter-sea-dark-water-daughter",
    "https://www.kobo.com/ca/en/ebook/the-helm-of-midnight",
    "https://www.kobo.com/ca/en/ebook/dead-dead-girls",
    "https://www.kobo.com/ca/en/ebook/the-rise-and-reign-of-the-mammals-3",
    "https://www.kobo.com/ca/en/ebook/pod-26",
    "https://www.kobo.com/ca/en/ebook/century-rain-4",
    "https://www.kobo.com/ca/en/ebook/a-magical-match",
    "https://www.kobo.com/ca/en/ebook/the-magician-s-daughter-8",
    "https://www.kobo.com/ca/en/ebook/the-dance-tree-1",
    "https://www.kobo.com/ca/en/ebook/the-bleeding-4",
    "https://www.kobo.com/ca/en/ebook/ghosts-from-the-library-lost-tales-of-terror-and-the-supernatural-a-bodies-from-the-library-special-1",
    "https://www.kobo.com/ca/en/ebook/a-city-on-mars-1",
    "https://www.kobo.com/ca/en/ebook/stranger-things-flight-of-icarus",
    "https://www.kobo.com/ca/en/ebook/bookshops-bonedust",
    "https://www.kobo.com/ca/en/ebook/the-remarkable-retirement-of-edna-fisher",
    "https://www.kobo.com/ca/en/ebook/her-majesty-s-royal-coven",
    "https://www.kobo.com/ca/en/ebook/the-book-that-wouldn-t-burn",
    "https://www.kobo.com/ca/en/ebook/the-storm-keeper-s-island-1",
    "https://www.kobo.com/ca/en/ebook/masters-of-death-3",
    "https://www.kobo.com/ca/en/ebook/the-making-of-another-major-motion-picture-masterpiece-1",
    "https://www.kobo.com/ca/en/ebook/no-place-like-home-108",
    "https://www.kobo.com/ca/en/ebook/the-frugal-wizard-s-handbook-for-surviving-medieval-england",
    "https://www.kobo.com/ca/en/ebook/the-family-fortuna",
    "https://www.kobo.com/ca/en/ebook/that-inevitable-victorian-thing",
    "https://www.kobo.com/ca/en/ebook/spell-booked",
    "https://www.kobo.com/ca/en/ebook/revelle-1",
    "https://www.kobo.com/ca/en/ebook/the-year-of-less-2",
    "https://www.kobo.com/ca/en/ebook/the-adventures-of-amina-al-sirafi-1",
    "https://www.kobo.com/ca/en/ebook/hamra-and-the-jungle-of-memories-1",
    "https://www.kobo.com/ca/en/ebook/vera-wong-s-unsolicited-advice-for-murderers-1",
    "https://www.kobo.com/ca/en/ebook/the-london-seance-society",
    "https://www.kobo.com/ca/en/ebook/hunt-on-dark-waters",
    "https://www.kobo.com/ca/en/ebook/a-midwinter-s-tail",
    "https://www.kobo.com/ca/en/ebook/these-silent-woods",
    "https://www.kobo.com/ca/en/ebook/nocturne-95",
    "https://www.kobo.com/ca/en/ebook/tell-me-pleasant-things-about-immortality",
    "https://www.kobo.com/ca/en/ebook/of-manners-and-murder",
    "https://www.kobo.com/ca/en/ebook/tell-me-i-m-worthless-1",
    "https://www.kobo.com/ca/en/ebook/silver-nitrate-2",
    "https://www.kobo.com/ca/en/ebook/sweep-of-stars",
    "https://www.kobo.com/ca/en/ebook/swan-dive-14",
    "https://www.kobo.com/ca/en/ebook/dying-of-politeness-1",
    "https://www.kobo.com/ca/en/ebook/black-sun-27",
    "https://www.kobo.com/ca/en/ebook/no-time-like-the-future-1",
    "https://www.kobo.com/ca/en/ebook/neurotribes",
    # "https://www.kobo.com/ca/en/ebook/but-you-don-t-look-autistic-at-all",
    "https://www.kobo.com/ca/en/ebook/one-dark-window",
    "https://www.kobo.com/ca/en/ebook/letters-to-a-young-poet-the-norton-centenary-edition",
    "https://www.kobo.com/ca/en/ebook/how-we-learn-3",
    "https://www.kobo.com/ca/en/ebook/spineless-8",
    "https://www.kobo.com/ca/en/ebook/immortal-longings-5",
    "https://www.kobo.com/ca/en/ebook/the-body-keeps-the-score",
    "https://www.kobo.com/ca/en/ebook/flowerheart-1",
    "https://www.kobo.com/ca/en/ebook/the-satanic-verses",
    "https://www.kobo.com/ca/en/ebook/midnight-s-children-1",
    "https://www.kobo.com/ca/en/ebook/gory-details-2",
    "https://www.kobo.com/ca/en/ebook/the-master-and-margarita-9",
    "https://www.kobo.com/ca/en/ebook/the-lake-house-22",
    "https://www.kobo.com/ca/en/ebook/antimatter-blues-1",
    # "https://www.kobo.com/ca/en/ebook/don-t-make-me-think-a-common-sense-approach-to-web-usability-1",
    "https://www.kobo.com/ca/en/ebook/the-design-of-everyday-things-6",
    # "https://www.kobo.com/ca/en/ebook/the-best-interface-is-no-interface",
    "https://www.kobo.com/ca/en/ebook/silverborn-the-mystery-of-morrigan-crow",
    "https://www.kobo.com/ca/en/ebook/catfish-rolling-2",
    "https://www.kobo.com/ca/en/ebook/on-the-edge-of-gone",
    "https://www.kobo.com/ca/en/ebook/earthlings-8",
    "https://www.kobo.com/ca/en/ebook/convenience-store-woman-6",
    "https://www.kobo.com/ca/en/ebook/an-accident-of-stars",
    "https://www.kobo.com/ca/en/ebook/black-tide-27",
    "https://www.kobo.com/ca/en/ebook/house-of-suns-2",
    "https://www.kobo.com/ca/en/ebook/home-before-dark-22",
    "https://www.kobo.com/ca/en/ebook/children-of-time-3",
    "https://www.kobo.com/ca/en/ebook/dead-silence-27",
    "https://www.kobo.com/ca/en/ebook/ghost-girl-17",
    "https://www.kobo.com/ca/en/ebook/ghostlight-6",
    "https://www.kobo.com/ca/en/ebook/monster-club-1-1"
]

def getPrice(text):
    num = ""
    for c in text:
        if c.isdigit() or c == '.':
            num = num + c

    # print(num)
    if num == '':
        print('000000')
        return 0

    return float(num)

def checkExists(browser, element):
    try: 
        browser.find_element(By.CSS_SELECTOR, (element))
        return True
    except:
        return False

def getBookData(url):
    print(url)
    browser.get(url)

    WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.active-price > div.price-wrapper > span.price:not(:empty)"))
                # EC.presence_of_element_located(('input[autocomplete=email]'))
            )

    # pprint(browser.find_element_by_css_selector("div.active-price > div.price-wrapper").get_attribute('outerHTML') )
    title = browser.find_element(By.CSS_SELECTOR, ("h1.title")).get_attribute('textContent').strip()
    priceText = browser.find_element(By.CSS_SELECTOR, ("div.active-price > div.price-wrapper")).get_attribute('textContent')
    cover = browser.find_element(By.CSS_SELECTOR, ("img.cover-image")).get_attribute("src")
    author = browser.find_element(By.CSS_SELECTOR, ("a.contributor-name")).get_attribute("textContent")
    

    preorder = ''

    if checkExists(browser, 'p.preorder-subtitle'):
        preorder = browser.find_element(By.CSS_SELECTOR, "p.preorder-subtitle").get_attribute("textContent")

    isPlus = checkExists(browser, 'h2.subscription-title')
    isSale = checkExists(browser, 'span.saving-callout') or checkExists(browser, "div.original-price")
    dealDescription = browser.find_element(By.CSS_SELECTOR, "div.deal-description").get_attribute("textContent") if checkExists(browser, 'div.deal-description') else ''
    price = getPrice(priceText)

    return {
        'title': title,
        'price': price,
        'cover': cover,
        'url': url,
        'preorder': preorder,
        'isPlus': isPlus,
        'isSale': isSale,
        'author': author,
        'dealDescription': dealDescription
    }

books = []
manga =[]
lns = []

for url in WISHLIST:
# for url in tqdm(WISHLIST):   
    sleep(0.5)
    book = getBookData(url)

    if (book['price'] == 0):
        # input('waiting')
        sleep(2)
        book = getBookData(url)

    if (book['price'] == 0):
        sleep(2)
        book = getBookData(url)

    books.append(book)


for url in MANGA_COMICS:
# for url in tqdm(WISHLIST):   
    sleep(0.5)
    item = getBookData(url)

    if (item['price'] == 0):
        sleep(2)
        item = getBookData(url)

    if (item['price'] == 0):
        sleep(2)
        item = getBookData(url)

    manga.append(item)

for url in LIGHT_NOVELS:
# for url in tqdm(WISHLIST):   

    sleep(0.5)
    item = getBookData(url)

    if (item['price'] == 0):
        sleep(2)
        item = getBookData(url)

    if (item['price'] == 0):
        sleep(2)
        item = getBookData(url)

    lns.append(item)

books.sort(key=lambda x: x['price'], reverse=False)
manga.sort(key=lambda x: x['price'], reverse=False)
lns.sort(key=lambda x: x['price'], reverse=False)

pprint(books)

with open(MAIN_DIR+'wishlist.json', "w") as f:
    json.dump(books, f, indent=4)

with open(MAIN_DIR+'manga_wishlist.json', "w") as f:
    json.dump(manga, f, indent=4)

with open(MAIN_DIR+'lns_wishlist.json', "w") as f:
    json.dump(lns, f, indent=4)

browser.quit()