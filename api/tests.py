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
import datetime


class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://accounts.spotify.com/api/token"

    def token_data(self):
        return {"grant_type": "client_credentials"}

    def client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        client_creds = f"{client_id}:{client_secret}"
        return base64.b64encode(client_creds.encode())

    def token_headers(self):
        client_creds_b64 = self.client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def authenticate(self):
        token_url = self.token_url
        token_data = self.token_data()
        token_headers = self.token_headers()
        req = requests.post(token_url, data=token_data, headers=token_headers)
        print(req.json)

        token_response_data = req.json()
        access_token = token_response_data['access_token']
        expires_in = token_response_data['expires_in']

        self.access_token = access_token
        return token_response_data


client_id = '1e6071d60ecc4bcaa9e077b9be068df2'
client_secret = 'fbd694a6c13048059bc032386f5eee36'

spotify_client = SpotifyAPI(client_id, client_secret)
print(spotify_client.__init__(client_id, client_secret))
print(spotify_client.client_credentials())
print(spotify_client.token_data())
print(spotify_client.token_headers())
print(spotify_client.authenticate())
