import json
from pprint import pprint
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm
import ruamel.yaml
import re
import os 
import frontmatter
import copy 
import utils 

yaml = ruamel.yaml.YAML()

ACTORS_FILE = 'actors.json'
MEDIA_FILE = 'media.json'
MEDIA_MAIN_DIR = '/Users/thiago/git/things/movies_tv'
ACTORS_MAIN_DIR = '/Users/thiago/git/things/people'

# MAIN_DIR = 'mds'
# IGNORE_LIST = ['/.DS_Store'] # '{}/Inbox/'.format(MAIN_DIR), 

# CHANGED_STATUS = []

def load_jsons():
    act = {}
    media = {}

    with open(ACTORS_FILE, 'r') as json_file:
        act = json.load(json_file)

    with open(MEDIA_FILE, 'r') as json_file:
        media = json.load(json_file)

    return media, act

def load_md():
    media_data = {}
    media_files = {}
    actor_data = {}
    actor_files = {}

    for root, dirs, files in os.walk(MEDIA_MAIN_DIR, topdown=False):
        for name in files:
            try:
                file_path = os.path.join(root, name)
                if file_path.endswith('.DS_Store'):
                    continue

                data = frontmatter.load(file_path)

                media_data[str(data.metadata['traktId'])] = data
                media_files[str(data.metadata['traktId'])] = file_path

            except:
                print("EXCEPT: ", file_path)
                raise Exception("stop")

    for root, dirs, files in os.walk(MEDIA_MAIN_DIR, topdown=False):
        for name in files:
            try:
                file_path = os.path.join(root, name)
                if file_path.endswith('.DS_Store'):
                    continue

                data = frontmatter.load(file_path)

                actor_data[str(data.metadata['traktId'])] = data
                actor_files[str(data.metadata['traktId'])] = file_path

            except:
                print("EXCEPT: ", file_path)
                raise Exception("stop")
            
    return media_data, media_files, actor_data, actor_files

# def containsAny(str, set):
#     """ Check whether sequence str contains ANY of the items in set. """
#     return 1 in [c in str for c in set]

def set_actor_frontmatter(actor):
    frontmatter = {}

    # cleanTitle = actor['name'].translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip() # re.sub(r'\(.+\)', ' ', book['title']) # Not removing series to avoid collisions
    # aliases = [cleanTitle]
    # frontmatter['aliases'] = aliases

    frontmatter["name"] = actor.get("name")
    frontmatter["birthday"] = actor.get("birthday")
    frontmatter["country"] = actor.get("country")
    frontmatter["profession"] = actor.get("profession")
    frontmatter["traktId"] = actor.get("traktId")
    frontmatter["link"] = actor.get("link")
    frontmatter["instagram"] = actor.get("instagram")
    frontmatter["twitter"] = actor.get("twitter")
    frontmatter["photo"] = actor.get("photo")
    frontmatter["cast"] = actor.get("cast")
    frontmatter["castIds"] = actor.get("castIds")
        
    tags = []
    for profession in frontmatter["profession"]:
        tags.append('people/'+profession)
    
    if frontmatter["country"] and frontmatter["country"] != "":
        tags.append('people/country/'+frontmatter["country"].replace(' ', ''))

    frontmatter['tags'] = tags

    # pprint(frontmatter)
    return frontmatter

def set_media_frontmatter(media):
    frontmatter = {}

    # cleanTitle = actor['name'].translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip() # re.sub(r'\(.+\)', ' ', book['title']) # Not removing series to avoid collisions
    # aliases = [cleanTitle]
    # frontmatter['aliases'] = aliases
    
    frontmatter["type"] = media.get("type")
    frontmatter["premiered"] = media.get("premiered")
    frontmatter["traktId"] = media.get("traktId")
    frontmatter["name"] = media.get("name")
    frontmatter["status"] = media.get("status")
    frontmatter["country"] = media.get("country")
    frontmatter["language"] = media.get("language")
    frontmatter["genres"] = media.get("genres")
    frontmatter["summary"] = media.get("summary")
    frontmatter["runtime"] = media.get("runtime")
    frontmatter["certification"] = media.get("certification")
    frontmatter["link"] = media.get("link")
    frontmatter["homepage"] = media.get("homepage")
    frontmatter["year"] = media.get("year")
    frontmatter["where"] = media.get("where")
    frontmatter["showStatus"] = media.get("showStatus")
    
    tags = ["media/"+frontmatter["type"], "media/status/"+frontmatter["status"]]
    
    if frontmatter["country"] and frontmatter["country"] != None and frontmatter["country"] != "":
        tags.append('media/country/'+frontmatter["country"].replace(' ', ''))

    if frontmatter["year"] and frontmatter["year"] != "":
        tags.append('media/year/'+str(frontmatter["year"]))

    for genre in frontmatter["genres"]:
        tags.append('media/genre/'+genre)

    frontmatter['tags'] = tags

    # pprint(frontmatter)
    return frontmatter

# def get_new_data(json_data, file_data):
#     updated = False

#     new_data = copy.deepcopy(file_data)

#     attributes = ['rating', 'binding', 'bookshelves', 'series', 'numberInSeries', 'genres'] # add type, setting

#     for attribute in attributes:
#         if file_data.get(attribute) != json_data.get(attribute):
#             updated = True
#             new_data[attribute] = json_data.get(attribute)

#     status = 'status/' + json_data['status']

#     if status not in file_data['tags']:
#         # replace status tag
#         CHANGED_STATUS.append(new_data['title'])
#         new_tags = []
#         for tag in file_data['tags']:
#             print('tag:', tag)
#             if tag.startswith('status/'):
#                 print('STARTSWITH', status)
#                 new_tags.append(status)
#             else:
#                 new_tags.append(tag)

#         new_data['tags'] = new_tags

#         updated = True
        
#     # JUST ONCE
#     # print(json_data['title'])
#     # new_data['aliases'] = [json_data['title'].translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip()]
#     # updated = True

#     return new_data, updated

def get_media_extra(media):
    text = """from:: [[{country}]]

***

"""

    return text.format(**media)

def get_actor_extra(actor):
    castLinks = ["[[{}]]".format(thing) for thing in actor['cast'] ]

    text = """from:: [[{}]]
castIn:: {}

![cover|150]({})
***

"""

    return text.format(actor['country'], ", ".join(castLinks), actor['photo'])

# def get_media_folder(media):
#     folder = {
#         'finished': 'finished/',
#         'tbr/owned': 'tbr/',
#         'tbr/notOwned': 'tbr/',
#         'tbr/next': 'next/',
#         # 'maybe': '', #it's not saved
#         'paused': 'paused/',
#         'interested': 'interested/',
#         'dnf': 'dnf/',
#         'inProgress': ''
#     }

#     return folder[media['status']]


json_media, json_actors = load_jsons()

media_data, media_files, actor_data, actor_files = load_md()
# print( len(md_books), len(md_files))

# updated_files = []

print('Exporting actors')
for actorId in json_actors:
    # print(actorId)
    actor = json_actors[actorId]

    # if actorId in actor_data:
    #     print('exists')
    # else:
    frontmatter = set_actor_frontmatter(actor)
    filename = actor["name"] # get_filename(actor['name'])
    folder = "" # get_folder(book)

    with open("{}/{}{}.md".format(ACTORS_MAIN_DIR, folder, filename), 'w') as fh:
        fh.write('---\n')
        yaml.dump(frontmatter, fh)
        fh.write('---\n')
        extra_data = get_actor_extra(actor)
        fh.write(extra_data)

print('Exporting media')
for mediaId in json_media:
    # print(actorId)
    media = json_media[mediaId]

    # if mediaId in media_data:
    #     # print('exists')
    #     pass
    # else:
    frontmatter = set_media_frontmatter(media)
    filename = utils.format_media_title(media)
    folder = media['status'] # get_media_folder(book)

    with open("{}/{}/{}.md".format(MEDIA_MAIN_DIR, folder, filename), 'w') as fh:
        fh.write('---\n')
        yaml.dump(frontmatter, fh)
        fh.write('---\n')
        extra_data = get_media_extra(media)
        fh.write(extra_data)

# print("updated files:", len(updated_files))
# print("Changed status:", CHANGED_STATUS)
# print("Unvisited files:", len(md_files), md_files)

