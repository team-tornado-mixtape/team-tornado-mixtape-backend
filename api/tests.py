from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Song


class SearchTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1", password="user1password")
        self.client.force_authenticate(self.user1)

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
        self.assertEqual(Song.objects.count(), 4)

    # def test_search_track3(self):
    #     url = "/api/search?track=You're+So+Vain"
    #     response = self.client.get(url, format="json")

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data[0]["title"], "")
    #     self.assertEqual(response.data[1]["title"], "")
    #     self.assertEqual(Song.objects.count(), 3)

    def test_search_artist1(self):
        url = "/api/search?artist=Beatles"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Eleanor Rigby")
        self.assertEqual(Song.objects.count(), 1)

    # def test_search_artist2(self):
    #     url = '/api/search?artist=Arctic+Monkeys'
    #     response = self.client.get(url, format="json")

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data[0]["title"], "No. 1 Party Anthem")
    #     self.assertEqual(response.data[1]["title"], "Old Yellow Bricks")
    #     self.assertEqual(response.data[2]["title"], "Brianstorm")
    #     self.assertEqual(response.data[3]["title"], "Mardy Bum")
    #     self.assertEqual(response.data[4]["title"], "Baby I'm Yours")
    #     self.assertEqual(response.data[5]["title"], "Knee Socks")
    #     self.assertEqual(Song.objects.count(), 13)
