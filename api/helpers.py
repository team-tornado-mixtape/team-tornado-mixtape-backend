from difflib import SequenceMatcher
import time
import threading
import datetime
import jwt
from urllib.parse import urlencode
import environ
import requests
import json
import os
import base64
import queue

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

q = queue.Queue()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def my_search(search_track=None, search_artist=None, limit=20):

    spotify_thread = threading.Thread(target=SearchSpotifyAPI, args=[q], kwargs={'search_track':search_track, 'search_artist':search_artist, 'limit':limit})
    apple_thread = threading.Thread(target=SearchAppleMusicAPI, args=[q], kwargs={'search_track':search_track, 'search_artist':search_artist, 'limit':limit})

    spotify_thread.start()
    apple_thread.start()
    q.join()
    spotify_results = q.get()
    apple_results = q.get()

    if 'apple_title' in spotify_results[0]:
        spotify_results, apple_results = apple_results, spotify_results

    songs = []
    # apple_ids = {}

    for i in range(len(spotify_results)):
        for j in range(len(apple_results)):

            if spotify_results[i]["spotify_title"] == apple_results[j]["apple_title"] and spotify_results[i]["spotify_artist"] == apple_results[j]["apple_artist"]:

                song = {
                    "title": apple_results[j]["apple_title"],
                    "artist": apple_results[j]["apple_artist"],
                    "album": apple_results[j]["apple_album"],
                    "spotify_id": spotify_results[i]["spotify_id"],
                    "apple_id": apple_results[j]["apple_id"],
                    "spotify_uri": spotify_results[i]["spotify_uri"],
                    "preview_url": apple_results[j]["apple_preview_url"],
                    }

                # apple_ids[apple_results[j]["apple_id"]] = 1
                songs.append(song)
                del apple_results[j]
                break

    return songs



KEY_ID = env("APPLE_KEY_ID")
TEAM_ID = env("APPLE_TEAM_ID")
alg = "ES256"

secret = f"""
-----BEGIN PRIVATE KEY-----
{env("APPLE_SECRET1")}
{env("APPLE_SECRET2")}
{env("APPLE_SECRET3")}
{env("APPLE_SECRET4")}
-----END PRIVATE KEY-----
"""

def SearchAppleMusicAPI(q, search_track=None, search_artist=None, limit=20):

    time_now = datetime.datetime.now()
    time_expired = time_now + datetime.timedelta(hours=12)

    headers = {"alg": alg, "kid": KEY_ID}

    payload = {
        "iss": TEAM_ID,
        "exp": int(time_expired.strftime("%s")),
        "iat": int(time_now.strftime("%s")),
    }

    token = jwt.encode(payload, secret, algorithm=alg, headers=headers)

    if search_track is not None and search_artist is None:
        data = urlencode({"types": "songs", "term": f"{search_track}", "limit": f"{limit}"})
    elif search_track is None and search_artist is not None:
        data = urlencode({"types": "songs", "term": f"{search_artist}", "limit": f"{limit}"})
    elif search_track is not None and search_artist is not None:
        data = urlencode({"types": "songs", "term": f"{search_track} {search_artist}", "limit": f"{limit}"})

    url = f"https://api.music.apple.com/v1/catalog/US/search?{data}"

    req = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    results = []

    for i in range(len(req.json()["results"]["songs"]["data"])):
        result = {"apple_id": req.json()["results"]["songs"]["data"][i]["id"]}
        result["apple_title"] = req.json()["results"]["songs"]["data"][i]["attributes"][
            "name"
        ]
        result["apple_album"] = req.json()["results"]["songs"]["data"][i]["attributes"][
            "albumName"
        ]
        result["apple_artist"] = req.json()["results"]["songs"]["data"][i][
            "attributes"
        ]["artistName"]
        result["apple_url"] = req.json()["results"]["songs"]["data"][i]["attributes"]["url"]
        result["apple_preview_url"] = req.json()["results"]["songs"]["data"][i]["attributes"]['previews'][0]["url"]
        results.append(result)

    # print(json.dumps(req.json(), sort_keys=4,indent=4))
    q.put(results)
    q.task_done()


# apple_search_results = SearchAppleMusicAPI(search_track="Enter Galactic", search_artist='Kid Cudi')
# print(apple_search_results)



CLIENT_ID = env("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = env("SPOTIFY_CLIENT_SECRET")

class SpotifyAPI:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.token_url = "https://accounts.spotify.com/api/token"
        self.authenticate()

    def token_data(self):
        return {"grant_type": "client_credentials"}

    def client_credentials(self):
        client_creds = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(client_creds.encode())

    def token_headers(self):
        return {"Authorization": f"Basic {self.client_credentials().decode()}"}

    def authenticate(self):
        req = requests.post(
            self.token_url, data=self.token_data(), headers=self.token_headers()
        )
        print(req.json)

        token_response_data = req.json()
        access_token = token_response_data["access_token"]
        expires_in = token_response_data["expires_in"]

        self.access_token = access_token
        return token_response_data


def SearchSpotifyAPI(q, search_track=None, search_artist=None, limit=20):
    spotify_client = SpotifyAPI()
    access_token = spotify_client.access_token

    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = "https://api.spotify.com/v1/search"

    if search_track is not None and search_artist is None:
        data = urlencode({"q": f"track:{search_track}", "type": "track", "limit": f"{limit}"})
    elif search_track is None and search_artist is not None:
        data = urlencode({"q": f"artist:{search_artist}", "type": "track", "limit": f"{limit}"})
    elif search_track is not None and search_artist is not None:
        data = urlencode({"q": f"track:{search_track} artist:{search_artist}", "type": "track", "limit": f"{limit}"})

    lookup_url = f"{endpoint}?{data}"
    req = requests.get(lookup_url, headers=headers)

    results = []

    for i in range(len(req.json()["tracks"]["items"])):
        result = {"spotify_id": req.json()["tracks"]["items"][i]["id"]}
        result["spotify_title"] = req.json()["tracks"]["items"][i]["name"]
        result["spotify_album"] = req.json()["tracks"]["items"][i]["album"]["name"]
        result["spotify_artist"] = req.json()["tracks"]["items"][i]["artists"][0][
            "name"
        ]
        result["spotify_uri"] = req.json()["tracks"]["items"][i]["uri"]
        # result["spotify_preview_url"] = req.json()["tracks"]["items"][i]["preview_url"]
        results.append(result)

    # print(json.dumps(req.json()["tracks"], sort_keys=4,indent=4))
    q.put(results)
    q.task_done()


# spotify_search_results = SearchSpotifyAPI(search_track='Enter Galactic', search_artist='Kid Cudi')
# print(spotify_search_results)
