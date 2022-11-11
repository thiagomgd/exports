import requests
import json
import anotion
from bs4 import BeautifulSoup

s = requests.Session()
# data = {"login":"my_login", "password":"my_password"}
req_data = {'auth': {"id":32518,"name":"FalconSensei","avatar":{"large":"https://s4.anilist.co/file/anilistcdn/user/avatar/large/n32518-XtxGstWrHtWD.png"},"bannerImage":"https://s4.anilist.co/file/anilistcdn/user/banner/n32518-b2KAVV6QhqV8.jpg","unreadNotificationCount":5,"donatorTier":0,"donatorBadge":"Donator","options":{"titleLanguage":"ENGLISH","staffNameLanguage":"ROMAJI_WESTERN","displayAdultContent":True,"profileColor":"purple","notificationOptions":[{"type":"ACTIVITY_MESSAGE","enabled":True},{"type":"ACTIVITY_REPLY","enabled":True},{"type":"FOLLOWING","enabled":True},{"type":"ACTIVITY_MENTION","enabled":True},{"type":"THREAD_COMMENT_MENTION","enabled":True},{"type":"THREAD_SUBSCRIBED","enabled":True},{"type":"THREAD_COMMENT_REPLY","enabled":True},{"type":"AIRING","enabled":True},{"type":"ACTIVITY_LIKE","enabled":True},{"type":"ACTIVITY_REPLY_LIKE","enabled":True},{"type":"THREAD_LIKE","enabled":True},{"type":"THREAD_COMMENT_LIKE","enabled":True},{"type":"ACTIVITY_REPLY_SUBSCRIBED","enabled":True},{"type":"RELATED_MEDIA_ADDITION","enabled":True},{"type":"MEDIA_DATA_CHANGE","enabled":True},{"type":"MEDIA_MERGE","enabled":True},{"type":"MEDIA_DELETION","enabled":True}]},"mediaListOptions":{"scoreFormat":"POINT_10","rowOrder":"updatedAt","animeList":{"customLists":[],"sectionOrder":["Watching","Rewatching","Completed","Completed TV","Completed Movie","Completed OVA","Completed ONA","Completed TV Short","Completed Special","Completed Music","Paused","Dropped","Planning"],"splitCompletedSectionByFormat":True,"advancedScoring":["Story","Characters","Visuals","Audio","Enjoyment"],"advancedScoringEnabled":False},"mangaList":{"customLists":["To Read"],"sectionOrder":["Reading","Rereading","Completed","Completed Manga","Completed Novel","Completed One Shot","Paused","Dropped","Planning"],"splitCompletedSectionByFormat":False,"advancedScoring":["Story","Characters","Visuals","Audio","Enjoyment"],"advancedScoringEnabled":False}},"nameId":"falconsensei"}}

url = "http://example.net/login"

endpoint = 'https://graphql.anilist.co'
headers = {}

query = """query {
   MediaListCollection(userName: "falconsensei", type: MANGA) {
    lists {
      entries {
        # id
        status
        score(format: POINT_10)
        progress
        notes
        repeat
        media {
        	 id
          idMal
          title {
            romaji
            english
            native
            userPreferred
          }
          startDate {
            year
            month
            day
          }
          endDate {
            year
            month
            day
          }
          season
          seasonYear
          type
          format
          status
          episodes
          duration
          chapters
          volumes
          isAdult
          genres
          tags {
            name
            # description
          }
          averageScore
          popularity
          source
        }
      }
      # name
      # isCustomList
      # isSplitCompletedList
      # status
    }
    
  }
}
"""

def get_poster(url, mal_url):
    page_data = requests.get(url, data=req_data)
    page = BeautifulSoup(page_data.content, 'html.parser')

    result = page.select_one('img.cover')

    if result:
        return result['src']

    page_data = requests.get(mal_url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    result = page.select_one('img[itemprop=image]')
    
    if result:
        return result['data-src']

    print('No cover', url)
    return None

def get_from_notion():
    notion_data = anotion.get_notion_data('MANGA')
    items = {}
    for itm in notion_data:
        an_id = itm['properties']['Anilist Id']['number']
        items[an_id] = itm

    return items

def to_anilist_dict(an):
    media = an['media']

    data = {
        'Name':  an['media']['title']['english'] if an['media']['title']['english'] else an['media']['title']['romaji'],
        'Cover': None,
        'Status': an['status'].title(),
        'Link': f"https://anilist.co/{media['type']}/{media['id']}".lower(),
        'MAL Link': f"https://myanimelist.net/{media['type']}/{media['idMal']}".lower(),
        'Genres': media['genres'],
        'Tags': [tag['name'] for tag in media['tags']],
        'Format': media['format'],
        'Volumes': media['volumes'],
        'Chapters': media['chapters'],
        'Year': media['seasonYear'],
        'Season': media['season'],
        'Anilist Id': media['id'],
        'Is Adult': media['isAdult'],
        'My Score': an['score'],
        'Avg. Score': media['averageScore']
    }


    return data

def to_anilist_list(an_data):
    an_list = []
    data = an_data['data']['MediaListCollection']['lists']
    for l in data:
        for entry in l['entries']:
            an_list.append(to_anilist_dict(entry))

    return an_list

def compare_data(notion, an):
    TO_COMPARE = ['Status', 'Avg. Score', 'My Score', 'Volumes', 'Chapters']

    stored = anotion.get_props_data(notion)
    to_update = {}
    
    for key in TO_COMPARE:
        notion_val = stored.get(key)
        an_val = an.get(key)
        if notion_val != an_val:
            if key == 'Status' and an_val == 'Planning' and notion_val in ['Planning', 'Next', 'Maybe']:
                continue

            # print(key, notion_val, trakt_val)
            # pprint(notion)
            # input('a')
            to_update[key] = an_val

    return to_update

def update_record(notion, an):
    diff = compare_data(notion, an)
    
    if len(diff) > 0:
        print('Update:', an['Name'], diff)
        notion_format = anotion.dict_to_notion(diff, anotion.manga_map_to_notion)
        anotion.update_notion(notion.get('id'), notion_format)

r = requests.post(endpoint, json={"query": query}, headers=headers)
if r.status_code != 200:
    print(r.text)
    raise Exception(f"Query failed to run with a {r.status_code}.")

# animes_an__ = json.loads(r.json())
animes_an = to_anilist_list(r.json())
# animes_an = to_anilist_dict(animes_an_)
animes_notion = get_from_notion()


for an in animes_an:
    if an['Anilist Id'] in animes_notion:
        update_record(animes_notion[an['Anilist Id']], an)
    else:
        print('Insert:', an['Name'])
        an['Cover'] = get_poster(an['Link'], an['MAL Link'])
        notion_format = anotion.dict_to_notion(an, anotion.manga_map_to_notion)
        anotion.insert_notion('MANGA', notion_format)
