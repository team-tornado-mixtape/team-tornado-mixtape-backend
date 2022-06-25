from django.test import TestCase
from api.apple_music_search import *
from api.spotify_search import *
from api.helpers import *


class SearchTestCase(TestCase):
    def __init__(self):
        self.search_track = "Yellow"
        self.search_artist = "Coldplay"

    def setup(self):
        self.apple_songs_track = SearchAppleMusicAPI(search_track=self.search_track)
        self.apple_songs_artist = SearchAppleMusicAPI(search_artist=self.search_artist)
        self.apple_songs = SearchAppleMusicAPI(search_track=self.search_track, search_artist=self.search_artist)

        self.spotify_songs_track = SearchSpotifyAPI(search_track=self.search_track)
        self.spotify_songs_artist = SearchSpotifyAPI(search_artist=self.search_artist)
        self.spotify_songs = SearchSpotifyAPI(search_track=self.search_track, search_artist=self.search_artist)

        self.my_songs_track = my_search(search_track=self.search_track)
        self.my_songs_track = my_search(search_artist=self.search_artist)
        self.my_songs = my_search(search_track=self.search_track, search_artist=self.search_artist)

    def compare_results(self):
        pass
