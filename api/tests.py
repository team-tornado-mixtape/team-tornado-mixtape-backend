from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.apple_music_search import *
from api.spotify_search import *
from api.helpers import *


# class SearchTestCase(TestCase):
#     def setUp(self):
#         self.search_track = "Yellow"
#         self.search_artist = "Coldplay"

#         self.apple_songs_track = SearchAppleMusicAPI(search_track=self.search_track)
#         self.apple_songs_artist = SearchAppleMusicAPI(search_artist=self.search_artist)
#         self.apple_songs = SearchAppleMusicAPI(search_track=self.search_track, search_artist=self.search_artist)

#         self.spotify_songs_track = SearchSpotifyAPI(search_track=self.search_track)
#         self.spotify_songs_artist = SearchSpotifyAPI(search_artist=self.search_artist)
#         self.spotify_songs = SearchSpotifyAPI(search_track=self.search_track, search_artist=self.search_artist)

#         self.my_songs_track = my_search(search_track=self.search_track)
#         self.my_songs_track = my_search(search_artist=self.search_artist)
#         self.my_songs = my_search(search_track=self.search_track, search_artist=self.search_artist)

#     def test_results(self):
#         for id in [self.spotify_songs[i]['spotify_id'] for i in range(len(self.spotify_songs))]:
#             if id not in [self.my_songs[i]['spotify_id'] for i in range(len(self.my_songs))]:
#                 print(id)


# class AccountTests(APITestCase):
#     def test_create_account(self):
#         """
#         Ensure we can create a new account object.
#         """
#         url = reverse('account-list')
#         data = {'name': 'DabApps'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Account.objects.count(), 1)
#         self.assertEqual(Account.objects.get().name, 'DabApps')


class SearchTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1", password="user1password")
        self.client.force_authenticate(self.user1)

    def test_search_track(self):
        url = '/api/search?track=Yellow+Submarine'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Yellow Submarine In Pepperland')
        self.assertEqual(Song.objects.count(), 3)

    def test_search_artist(self):
        url = '/api/search?artist=Beatles'
        response = self.client.get(url, format='json')
        breakpoint()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data[0]['title'], 'Yellow Submarine In Pepperland')
        self.assertEqual(Song.objects.count(), 6)
