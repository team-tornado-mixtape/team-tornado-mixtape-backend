import base64
import requests
import json
from urllib.parse import urlencode
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

client_id = env('spotify_client_id')
client_secret = env('spotify_client_secret')


class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
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
        req = requests.post(self.token_url, data=self.token_data(), headers=self.token_headers())
        print(req.json)

        token_response_data = req.json()
        access_token = token_response_data['access_token']
        expires_in = token_response_data['expires_in']

        self.access_token = access_token
        return token_response_data

def SearchSpotifyAPI(search, limit=10):
    spotify_client = SpotifyAPI(client_id, client_secret)
    access_token = spotify_client.access_token

    headers = {'Authorization': f"Bearer {access_token}"}
    endpoint = "https://api.spotify.com/v1/search"

    data = urlencode({
        "q": f"{search}",
        "type": "track",
        "limit": f"{limit}"
    })

    lookup_url = f"{endpoint}?{data}"
    req = requests.get(lookup_url, headers=headers)

    results = []

    for i in range(len(req.json()['tracks']['items'])):
        result = {"spotify_id": req.json()['tracks']['items'][i]['id']}
        result["spotify_title"] = req.json()['tracks']['items'][i]['name']
        result["spotify_album"] = req.json()['tracks']['items'][i]['album']['name']
        result["spotify_artist"] = req.json()['tracks']['items'][i]['artists'][0]['name']
        result["spotify_uri"] = req.json()['tracks']['items'][i]['uri']
        results.append(result)

    # print(json.dumps(req.json(), sort_keys=4,indent=4)) 
    return results


# spotify_search_results = SearchSpotifyAPI('Enter Galactic')
# print(spotify_search_results)
