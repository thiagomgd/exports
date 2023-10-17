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
import requests 

MEDIA_FILE = 'media.json'

STATUS_TO_LIST = {
    'old-stuff': 8271848,
    'brazilian': 8271847,
    'memories': 8271846,
    'on-hold': 8271845,
    'abandoned': 8271844,
    'rewatch': 8271832,
    'b-trashy': 8264706,
    'finished': 8271831,
    'r': 8264522,
    # 'favorites': 'favorites'
}

def load_json():
    media = {}

    with open(MEDIA_FILE, 'r') as json_file:
        media = json.load(json_file)

    return media
 
json_media = load_json()

# import requests

# payload = { "request_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTU1MjgzMTQsIm5iZiI6MTY5NTUyNzQxNCwianRpIjo2NzExNTMxLCJzY29wZXMiOlsicGVuZGluZ19yZXF1ZXN0X3Rva2VuIl0sInJlZGlyZWN0X3RvIjpudWxsLCJ2ZXJzaW9uIjoxLCJhdWQiOiI5N2MxMDFkZWI1ZTU4Mjc1YjcxNzgwYjVjY2MyMmFiMSJ9.45eCo6247DvYaWCVR3c4TLWrjucm46LLgf5Voy9Q2F0" }

# access token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZmRmZTQwMDc2NDg0MTAwM2Y2Zjk2MjciLCJ2ZXJzaW9uIjoxLCJuYmYiOjE2OTU1Mjc1MTQsImF1ZCI6Ijk3YzEwMWRlYjVlNTgyNzViNzE3ODBiNWNjYzIyYWIxIiwianRpIjoiNjcxMTUzMSIsInNjb3BlcyI6WyJhcGlfcmVhZCIsImFwaV93cml0ZSJdfQ.7S1Fr_EyLoxcTqqud6RESKFVhgvXfFwFez2BhmYeMUM


# url = "https://api.themoviedb.org/4/list/8271848"

# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZmRmZTQwMDc2NDg0MTAwM2Y2Zjk2MjciLCJ2ZXJzaW9uIjoxLCJuYmYiOjE2OTU1Mjc1MTQsImF1ZCI6Ijk3YzEwMWRlYjVlNTgyNzViNzE3ODBiNWNjYzIyYWIxIiwianRpIjoiNjcxMTUzMSIsInNjb3BlcyI6WyJhcGlfcmVhZCIsImFwaV93cml0ZSJdfQ.7S1Fr_EyLoxcTqqud6RESKFVhgvXfFwFez2BhmYeMUM"
# }

# response = requests.get(url, headers=headers)

# print(response.text)

# url = "https://api.themoviedb.org/4/8271850/items"

# payload = { "items": [
#         {
#             "media_type": "movie",
#             "media_id": 820609
#         },
#         {
#             "media_type": "tv",
#             "media_id": 72710
#         }
#     ] }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZmRmZTQwMDc2NDg0MTAwM2Y2Zjk2MjciLCJ2ZXJzaW9uIjoxLCJuYmYiOjE2OTU1Mjc1MTQsImF1ZCI6Ijk3YzEwMWRlYjVlNTgyNzViNzE3ODBiNWNjYzIyYWIxIiwianRpIjoiNjcxMTUzMSIsInNjb3BlcyI6WyJhcGlfcmVhZCIsImFwaV93cml0ZSJdfQ.7S1Fr_EyLoxcTqqud6RESKFVhgvXfFwFez2BhmYeMUM"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)

for mediaId in json_media:
    # print(actorId)
    media = json_media[mediaId]

    listCode = STATUS_TO_LIST.get(media['status'], None)

    # print(media['status'], listCode)
    # if media['status'] == "favorites":
    #     tmdbId = media['tmdbId']

    #     url = "https://api.themoviedb.org/3/account/9932771/favorite"

    #     payload = {
    #         "media_type": media["type"].lower(),
    #         "media_id": tmdbId,
    #         "favorite": True
    #     }
    #     headers = {
    #         "accept": "application/json",
    #         "content-type": "application/json",
    #         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5N2MxMDFkZWI1ZTU4Mjc1YjcxNzgwYjVjY2MyMmFiMSIsInN1YiI6IjVmZGZlNDAwNzY0ODQxMDAzZjZmOTYyNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.aBhBtfEkOFW7vNOUQGjQN7o2-yEaF7NspytqcdurKM0"
    #     }

    #     response = requests.post(url, json=payload, headers=headers)

    #     pprint(response.text)

    if listCode != None:
        tmdbId = media['tmdbId']

        url = "https://api.themoviedb.org/4/list/{}/items".format(listCode)

        payload = { "items": [
            {
                "media_type": media["type"].lower(),
                "media_id": tmdbId,
            }
        ]}
      
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZmRmZTQwMDc2NDg0MTAwM2Y2Zjk2MjciLCJ2ZXJzaW9uIjoxLCJuYmYiOjE2OTU1Mjc1MTQsImF1ZCI6Ijk3YzEwMWRlYjVlNTgyNzViNzE3ODBiNWNjYzIyYWIxIiwianRpIjoiNjcxMTUzMSIsInNjb3BlcyI6WyJhcGlfcmVhZCIsImFwaV93cml0ZSJdfQ.7S1Fr_EyLoxcTqqud6RESKFVhgvXfFwFez2BhmYeMUM"
        }

        response = requests.post(url, json=payload, headers=headers)

        print(url, payload)
        pprint(response.text)


