from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Song
from api.helpers import *


class SearchTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1", password="user1password")
        self.client.force_authenticate(self.user1)

    def test_search_track0(self):
        url = "/api/search?track="
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Song.objects.count(), 0)

    def test_search_track1(self):
        url = "/api/search?track=Yellow+Submarine"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Yellow Submarine")
        self.assertEqual(response.data[1]["title"], "Yellow Submarine")
        self.assertEqual(Song.objects.count(), 2)

    def test_search_track2(self):
        url = "/api/search?track=Yellow"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Yellow")
        self.assertEqual(response.data[1]["title"], "Bodak Yellow")
        self.assertEqual(Song.objects.count(), 3)

    def test_search_track3(self):
        url = "/api/search?track=Youre+So+Vain"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "You're So Vain")
        self.assertEqual(response.data[1]["title"], "You're So Vain")
        self.assertEqual(Song.objects.count(), 8)

    def test_search_artist1(self):
        url = "/api/search?artist=Beatles"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Song.objects.count(), 0)

    def test_search_artist2(self):
        url = '/api/search?artist=Arctic+Monkeys'
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "A Certain Romance")
        self.assertEqual(response.data[1]["title"], "Fireside")
        self.assertEqual(response.data[2]["title"], "Crying Lightning")
        self.assertEqual(response.data[3]["title"], "No. 1 Party Anthem")
        self.assertEqual(response.data[4]["title"], "Mardy Bum")
        self.assertEqual(response.data[5]["title"], "When the Sun Goes Down")
        self.assertEqual(Song.objects.count(), 14)
