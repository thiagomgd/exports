from os import stat
from bs4 import BeautifulSoup
import requests
import json, datetime, csv, tqdm
from pprint import pprint

def selectonetext(page, label):
    itm = page.select_one(label)
    return itm.text if itm else None


with open("stars.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    # print(soup)

bios = soup.select('a[href*="/bio"]')

print(len(bios))

stars = []

for bio in bios:
    url = bio['href']
    print(url)
# with open("emilywillis.html") as fp:
    page_data = requests.get(url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    star = {}
    img = page.select_one("body > div.flex-footer-wrapper > div > div.right-container.flex-m-column.d-m-flex.flex-1 > main > div.px-2.px-md-3 > section > header > div.dashboard-image-container > a > img")
    star["Name"] = img["title"] if img else 'NO-NAME'
    star["Photo"] = img["src"] if img else None
    pi = page.select_one('div[data-test="section-personal-information"]')
    # pprint(pi)

    dob = pi.select_one('a[href*="/babes?f%5BdateOfBirth%5D"]')
    star["Birthday"] = dob["href"].split("=")[1] if dob else None
    country = pi.select_one('a[href*="/babes?f%5BcountryCode%5D"]')
    star["Country"] = country["title"] if country else None
    ethnicity = page.select_one('span[data-test="link_span_ethnicity"]')
    star["Ethnicity"] = ethnicity.text
    aliases = page.select_one('p[data-test="p_aliases"]')
    star["Aliases"] = aliases.text.replace('\n','').strip() if aliases else None

    # official website
    # links

    #appearance
    appearance = page.select_one('ul.profile-meta-list')
    # pprint(appearance)
    star["Eyes"] = selectonetext(appearance, 'span[data-test="link_span_eye_color"]')
    star["Hair"] = selectonetext(appearance, 'span[data-test="link_span_hair_color"]')
    star["Height"] = (selectonetext(appearance, 'span[data-test="link_span_height"]') or '').split(" - ")[0]
    star["Weight"] = (selectonetext(appearance, 'span[data-test="link_span_weight"]') or '').split(" - ")[0]

    measurements = appearance.select('span[data-test="p-measurements"] span')

    if len(measurements) > 0:
        star["Bra"] = measurements[0].text
        star["Waist"] = measurements[1].text
        star["Hip"] = measurements[2].text


    star["Boobs"] = selectonetext(appearance, 'span[data-test="link_span_boobs"]')
    star["Shoes"] = selectonetext(appearance, 'span[data-test="link_span_shoe_size"]')
    star["Tattoos"] = selectonetext(appearance, 'span[data-test="p_has_tattoos"] span')
    star["Piercings"] = selectonetext(appearance, 'span[data-test="p_has_piercings"] span')

    status = page.select_one('a[href*="/babes?f%5BcareerStatus%5D="]')
    star["Status"] = status["href"].split("=")[1]

    
    started = page.select_one("body > div.flex-footer-wrapper > div > div.right-container.flex-m-column.d-m-flex.flex-1 > main > div.d-lg-flex.flex-1.flex-1--ie11.flex-lg-row > div.d-block.d-lg-flex.flex-lg-column.w-lg-30.pr-2.pr-lg-3.sidebar-right.sidebar-right-wide > div > div.flex-1.mb-4.mb-md-0 > div.timeline-horizontal.mb-3 > div.d-flex.justify-content-between.font-size-md.align-items-center.mb-2 > p:nth-child(1)")
    star['Started'] = started.text if started else None

    until = page.select_one("body > div.flex-footer-wrapper > div > div.right-container.flex-m-column.d-m-flex.flex-1 > main > div.d-lg-flex.flex-1.flex-1--ie11.flex-lg-row > div.d-block.d-lg-flex.flex-lg-column.w-lg-30.pr-2.pr-lg-3.sidebar-right.sidebar-right-wide > div > div.flex-1.mb-4.mb-md-0 > div.timeline-horizontal.mb-3 > div.d-flex.justify-content-between.font-size-md.align-items-center.mb-2 > p:nth-child(3)")
    star['Until'] = until.text if (until and until.text != 'Now') else None


    social_urls = page.select('div.social-meta a')

    # pprint(social_urls)

    star["Social"] = [a['href'] for a in social_urls]
    star["Freeones"] = url

    pprint(star)
    stars.append(star)

csv_columns = ['Name','Photo','Birthday','Country','Ethnicity','Aliases','Eyes','Hair','Height','Weight','Bra','Waist','Hip','Boobs','Shoes','Tattoos','Piercings','Status','Started','Until','Social','Freeones']
time_stamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")

with open('stars_{}.csv'.format(time_stamp), mode='w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in stars:
        writer.writerow(data)