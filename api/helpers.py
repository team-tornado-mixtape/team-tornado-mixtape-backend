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
from difflib import SequenceMatcher
import spotipy
from spotipy.oauth2 import SpotifyOAuth


env = environ.Env(DEBUG=(bool, False))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

q = queue.Queue() # defining q here is important

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# my_search function runs searches through Spotify and Apple Music and compares results
def my_search(search_track=None, search_artist=None, limit=25):
# lines 24-25 set up threads for Spotify and Apple Music
# notice that q is passed as an argument and within each function
# q.put(results) is run to be retrievable later and q.task_done() to update status
    spotify_thread = threading.Thread(target=SearchSpotifyAPI, kwargs={"q":q ,"search_track":search_track, "search_artist":search_artist, "limit":limit})
    apple_thread = threading.Thread(target=SearchAppleMusicAPI, args=[q], kwargs={"search_track":search_track, "search_artist":search_artist, "limit":limit})
# lines 28-32 start the two threads and make sure they wait for each other
# to finish, then get the results from q
    spotify_thread.start()
    apple_thread.start()
    q.join()
    spotify_results = q.get()
    apple_results = q.get()
# define songs in line 35 in case no results from either Spotify or Apple Music 
# search because if either has no results, no match will be found, as checked in line 36
    songs = []
    if len(apple_results) == 0 or len(spotify_results) == 0:
        return songs
# I do not know ahead of time which search will be faster (Spotify or Apple Music)
# and thus need to check in line 40 and switch only if necessary
    if "apple_title" in spotify_results[0]:
        spotify_results, apple_results = apple_results, spotify_results
# iterate through both sets of results and make sure matches are returned as 
# well as being unique results
    for i in range(len(spotify_results)):
        for j in range(len(apple_results)):
# checking for an exact match of titles and artists in line 47
            if similar(spotify_results[i]["spotify_title"], apple_results[j]["apple_title"]) >= 0.92 and spotify_results[i]["spotify_artist"] == apple_results[j]["apple_artist"] and similar(spotify_results[i]["spotify_album"], apple_results[j]["apple_album"]) >= 0.92:
# if match, create dict of song info as per Song model in api.models in lines 49-57
                song = {
                    "title": apple_results[j]["apple_title"],
                    "artist": apple_results[j]["apple_artist"],
                    "album": apple_results[j]["apple_album"],
                    "spotify_id": spotify_results[i]["spotify_id"],
                    "apple_id": apple_results[j]["apple_id"],
                    "spotify_uri": spotify_results[i]["spotify_uri"],
                    "preview_url": apple_results[j]["apple_preview_url"],
                    }
# in lines 61-62 delete instance of apple_results[j] and break inner loop for
# optimization purposes
                songs.append(song)
                del apple_results[j]
                break
# return songs that are matches from Spotify and Apple Music search results
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


def SearchAppleMusicAPI(q=None, search_track=None, search_artist=None, limit=25):
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
        result["apple_preview_url"] = req.json()["results"]["songs"]["data"][i]["attributes"]["previews"][0]["url"]
        results.append(result)

    # print(json.dumps(req.json(), sort_keys=4,indent=4))
    q.put(results)
    q.task_done()


# apple_search_results = SearchAppleMusicAPI(search_track="Enter Galactic", search_artist='Kid Cudi')
# print(apple_search_results)



SPOTIFY_CLIENT_ID = env("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = env("SPOTIFY_CLIENT_SECRET")

# lines 139-205 function in a similar way as lines 82-131 but for Spotify search
class SpotifyAPI:
    def __init__(self):
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
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


def SearchSpotifyAPI(q=None, search_track=None, search_artist=None, limit=25):
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
        results.append(result)

    # print(json.dumps(req.json()["tracks"], sort_keys=4,indent=4))
    q.put(results)
    q.task_done()


# spotify_search_results = SearchSpotifyAPI(search_track='Enter Galactic', search_artist='Kid Cudi')
# print(spotify_search_results)


def create_spotify_playlist(username, mixtape):
    scope = "playlist-modify-public"

    token = SpotifyOAuth(scope=scope, username=username)
    spotifyObject = spotipy.Spotify(auth_manager=token)

    playlist_name = mixtape.title
    playlist_description = mixtape.description

    spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)

    list_of_songs = mixtape.songs.all()
    list_of_uris = [song.spotify_uri for song in list_of_songs]

    prePlaylist = spotifyObject.user_playlists(user=username)
    playlist_id = prePlaylist['items'][0]['id']

    spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_uris)


def apple_playlist_create(mixtape):
    # https://developer.apple.com/documentation/applemusicapi/libraryplaylistcreationrequest
    payload = {'attributes': {'name': mixtape.title}}
    payload['attributes']['description'] = mixtape.description

    return requests.post(
        endpoint='/me/library/playlists',
        payload=payload,
    )

def apple_playlist_add_tracks(playlist_id, track_ids):
    """https://developer.apple.com/documentation/applemusicapi/add_tracks_to_library_playlist
    """
    payload = {'data': track_ids}
    return self._make_request(
        method='POST',
        endpoint="/me/library/playlists/%s/tracks" % playlist_id,
        payload=payload,
    )
