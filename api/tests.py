from django.test import TestCase
from api.apple_music_search import *
from api.spotify_search import *
from api.helpers import *


class SearchTestCase(TestCase):
    def __init__(self):
        self.search_track = "Yellow"
        self.search_artist = "Coldplay"

    def setup(self):
        apple_songs_track = SearchAppleMusicAPI(search_track=self.search_track)
        apple_songs_artist = SearchAppleMusicAPI(search_artist=self.search_artist)
        apple_songs = SearchAppleMusicAPI(search_track=self.search_track, search_artist=self.search_artist)

        spotify_songs_track = SearchSpotifyAPI(search_track=self.search_track)
        spotify_songs_artist = SearchSpotifyAPI(search_artist=self.search_artist)
        spotify_songs = SearchSpotifyAPI(search_track=self.search_track, search_artist=self.search_artist)

    def test_searches(self):
        my_search()
