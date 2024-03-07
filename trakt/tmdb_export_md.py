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
import time 

yaml = ruamel.yaml.YAML()

ACTORS_FILE = 'actors.json'
MEDIA_FILE = 'media.json'
MOVIES_MAIN_DIR = '/Users/thiago/git/Main/Media/Movies'
TV_MAIN_DIR = '/Users/thiago/git/Main/Media/TV'
ACTORS_MAIN_DIR = '/Users/thiago/git/Main/people/famous'

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


def set_actor_frontmatter(actor):
    frontmatter = {}

    # cleanTitle = actor['name'].translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip() # re.sub(r'\(.+\)', ' ', book['title']) # Not removing series to avoid collisions
    # aliases = [cleanTitle]
    # frontmatter['aliases'] = aliases

    frontmatter["name"] = actor.get("name")
    frontmatter["birthday"] = actor.get("birthday")
    frontmatter["country"] = actor.get("country")
    frontmatter["traktId"] = actor.get("traktId")
    frontmatter["tmdbId"] = actor.get("tmdbId")
    frontmatter["link"] = actor.get("link")
    frontmatter["instagram"] = actor.get("instagram")
    frontmatter["twitter"] = actor.get("twitter")
    frontmatter["photo"] = actor.get("photo")
    frontmatter["syncedDate"] = int(time.time() * 1000)
        
    tags = []
    tags.append('people/actor')
    
    frontmatter['tags'] = tags

    # pprint(frontmatter)
    return frontmatter

def set_media_frontmatter(media):
    frontmatter = {}
    
    # frontmatter["premiered"] = media.get("premiered")
    frontmatter["traktId"] = media.get("traktId")
    frontmatter["tmdbId"] = media.get("tmdbId")
    frontmatter["syncedDate"] = int(time.time() * 1000)
    
    mediaType = 'show' if media["type"] == 'TV' else 'movie'
    tags = ["media/"+mediaType, "media/status/"+media.get("status")]
    
    frontmatter['tags'] = tags

    return frontmatter

def get_media_extra(media):
    text = """
***

"""

    return text.format(**media)

def get_actor_extra(actor):
    text = """![cover|150]({})
***

"""

    return text.format(actor['photo'])

json_media, json_actors = load_jsons()

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

    fname = "{}/{}{}.md".format(ACTORS_MAIN_DIR, folder, filename)
    if os.path.exists(fname):
        continue

    with open(fname, 'w') as fh:
        fh.write('---\n')
        yaml.dump(frontmatter, fh)
        fh.write('---\n')
        extra_data = get_actor_extra(actor)
        fh.write(extra_data)

# print('Exporting media')
# for mediaId in json_media:
#     # print(actorId)
#     media = json_media[mediaId]

#     # if mediaId in media_data:
#     #     # print('exists')
#     #     pass
#     # else:
#     frontmatter = set_media_frontmatter(media)
#     filename = utils.format_media_title(media)
#     folder = MOVIES_MAIN_DIR if media['type'] == "Movie" else TV_MAIN_DIR
#     year = media.get('year')
#     decade = 'noYear' if year == None else str(year)[:-1] + '0s'

#     filePath = "{}/{}".format(folder, decade)
#     if not os.path.exists(filePath):
#         os.makedirs(filePath)

#     print("{}/{}.md".format(filePath, filename))

#     with open("{}/{}.md".format(filePath, filename), 'w') as fh:
#         fh.write('---\n')
#         yaml.dump(frontmatter, fh)
#         fh.write('---\n')
#         extra_data = get_media_extra(media)
#         fh.write(extra_data)

# print("updated files:", len(updated_files))
# print("Changed status:", CHANGED_STATUS)
# print("Unvisited files:", len(md_files), md_files)

