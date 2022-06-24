import base64
import requests
import json
from urllib.parse import urlencode
import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

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


def SearchSpotifyAPI(search_track=None, search_artist=None, limit=20):
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
    return results


# spotify_search_results = SearchSpotifyAPI(search_track='Enter Galactic', search_artist='Kid Cudi')
# print(spotify_search_results)
