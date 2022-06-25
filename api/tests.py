from django.test import TestCase
from api.apple_music_search import *
from api.spotify_search import *
from api.helpers import *


class SearchTestCase(TestCase):
    def setUp(self):
        self.search_track = "Yellow"
        self.search_artist = "Coldplay"

        self.apple_songs_track = SearchAppleMusicAPI(search_track=self.search_track)
        self.apple_songs_artist = SearchAppleMusicAPI(search_artist=self.search_artist)
        self.apple_songs = SearchAppleMusicAPI(search_track=self.search_track, search_artist=self.search_artist)

        self.spotify_songs_track = SearchSpotifyAPI(search_track=self.search_track)
        self.spotify_songs_artist = SearchSpotifyAPI(search_artist=self.search_artist)
        self.spotify_songs = SearchSpotifyAPI(search_track=self.search_track, search_artist=self.search_artist)

        self.my_songs_track = my_search(search_track=self.search_track)
        self.my_songs_track = my_search(search_artist=self.search_artist)
        self.my_songs = my_search(search_track=self.search_track, search_artist=self.search_artist)

    def test_results(self):
        for id in [self.spotify_songs[i]['spotify_id'] for i in range(len(self.spotify_songs))]:
            if id not in [self.my_songs[i]['spotify_id'] for i in range(len(self.my_songs))]:
                print(id)
