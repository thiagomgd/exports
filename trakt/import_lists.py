import json
from urllib.request import urlopen
import copy 
from tqdm import tqdm 
import lists
import time 

MEDIA_FILE = 'media.json'

def load_json():
    with open(MEDIA_FILE, 'r') as json_file:
        media = json.load(json_file)

        return media

def update_record(json_data, trakt_data):
    new_data = copy.deepcopy(json_data)

    # for now, justoverwrite all trakt data (this will skip any custom fields I decide to add)
    new_data["type"] = trakt_data.get("type")
    new_data["premiered"] = trakt_data.get("premiered")
    new_data["showStatus"] = trakt_data.get("showStatus")
    new_data["traktId"] = trakt_data["traktId"]
    new_data["tmdbId"] = trakt_data["tmdbId"]
    # pprint(trakt_data)
    # print(new_data["tmdbId"])
    new_data["name"] = trakt_data["name"]
    new_data["status"] = trakt_data["status"]
    new_data["country"] = trakt_data["country"]
    new_data["language"] = trakt_data["language"]
    new_data["genres"] = trakt_data["genres"]
    new_data["summary"] = trakt_data["summary"]
    new_data["runtime"] = trakt_data["runtime"]
    new_data["certification"] = trakt_data["certification"]
    new_data["link"] = trakt_data["link"]
    new_data["homepage"] = trakt_data["homepage"]
    new_data["year"] = trakt_data["year"]
    new_data["where"] = trakt_data["where"]
    new_data['syncedDate'] = time.time()*1000

    return new_data

media_trakt = lists.get_all_trakt()

media_json = load_json()


print("TOTAL json", len(media_json), 'Total Trakt', len(media_trakt))

# # TODO: keep track of visited, check which ones on JSON are not on trakt, print to terminal so I can delete

new = 0
updated = 0
new_dict = {}

# # for book_id in books_gr:
for id in tqdm(media_trakt):
    thing_trakt = media_trakt[id]
    # id = str(thing_trakt['traktId'])

    if id in media_json:
        # print('EXISTS')
        thing_json = media_json[id]
        # print(book_id)

        
        new_data = update_record(thing_json, thing_trakt)
        # print('@@@', new_data['status'])
        # print('update?')
        new_dict[id] = new_data
        # del media_json[id]
        updated += 1
            # print("!!!!", new_dict[book_id]['status'])
    else:
        # print(id, media_json.get(id), media_json.get(int(id)))
        new_dict[id] = thing_trakt
        new += 1
    

print(
    "new:", len(new_dict),
    "json", len(media_json),
    "trakt", len(media_trakt),
    "new", new,
    "updated", updated
    )

with open(MEDIA_FILE, "w") as f:
    json.dump(new_dict, f, indent=4)

# MAIN_DIR = '/Users/thiago/git/geekosaurblog/src/_cache/'
# with open(MAIN_DIR+'goodreads.json', "w") as f:
#     json.dump(new_dict, f, indent=4)