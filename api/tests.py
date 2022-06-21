# from django.test import TestCase

# Create your tests here.


# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# import json

# scope ='playlist-modify-public'
# username ='22yw7ak2iuqbzhlkprlbcbnka'

# token = SpotifyOAuth(scope=scope,username=username)
# spotifyObject = spotipy.Spotify(auth_manager=token)

# create mixtape. using "playlist" because i think it may be spotify terminology
# playlist_name= input("Enter Mixtape Name: ")
# playlist_description= input("Enter Mixtape Description: ")

# spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True, description=playlist_description)

# user_input = input("Enter Song Title: ")
# list_of_songs = []

# while user_input != 'quit':
#     result = spotifyObject.search(q=user_input)
#     print(result)
#     print(json.dumps(result,sort_keys=4,indent=4))
#     print(result['tracks']['items'][0]['uri'])
#     list_of_songs.append(result['tracks']['items'][0]['uri'])
#     user_input = input("Enter Song Title: ")

# prePlaylist = spotifyObject.user_playlists(user=username)
# playlist = prePlaylist['items'][0]['id']

# add songs
# spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_songs)



import base64
import requests
import json
from urllib.parse import urlencode


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


client_id = '1e6071d60ecc4bcaa9e077b9be068df2'
client_secret = 'fbd694a6c13048059bc032386f5eee36'

spotify_client = SpotifyAPI(client_id, client_secret)
access_token = spotify_client.access_token

headers = {'Authorization': f"Bearer {access_token}"}

endpoint = "https://api.spotify.com/v1/search"

search = "Walk the Walk"

data = urlencode({
    "q": f"{search}",
    "type": "track",
    "limit": 1
})

lookup_url = f"{endpoint}?{data}"

req = requests.get(lookup_url, headers=headers)

# print(json.dumps(req.json(), sort_keys=4, indent=4))
print(req.json()['tracks']['items'][0]['uri'])
