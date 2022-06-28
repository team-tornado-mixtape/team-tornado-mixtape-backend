from difflib import SequenceMatcher
from api.spotify_search import *
from api.apple_music_search import *
import time
import threading


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def my_search(search_track=None, search_artist=None, limit=20):
    start = time.perf_counter()

    spotify_results = threading.Thread(target=SearchSpotifyAPI, kwargs={'search_track':search_track, 'search_artist':search_artist, 'limit':limit})
    apple_results = threading.Thread(target=SearchAppleMusicAPI, kwargs={'search_track':search_track, 'search_artist':search_artist, 'limit':limit})

    spotify_results.start()
    apple_results.start()
    spotify_results.join()
    apple_results.join() 

    stop = time.perf_counter()
    print(f"finished external api calls in: {round(stop-start, 2)} second(s)")

    # spotify_results = SearchSpotifyAPI(search_track=search_track, search_artist=search_artist, limit=limit)
    # apple_results = SearchAppleMusicAPI(search_track=search_track, search_artist=search_artist, limit=limit)

    songs = []
    apple_ids = {}

    for i in range(len(spotify_results)):

        for j in range(len(apple_results)):
            if spotify_results[i]["spotify_title"] == apple_results[j]["apple_title"] and spotify_results[i]["spotify_artist"] == apple_results[j]["apple_artist"] and apple_results[j]["apple_id"] not in apple_ids:
                song = {
                    "title": apple_results[j]["apple_title"],
                    "artist": apple_results[j]["apple_artist"],
                    "album": apple_results[j]["apple_album"],
                    "spotify_id": spotify_results[i]["spotify_id"],
                    "apple_id": apple_results[j]["apple_id"],
                    "spotify_uri": spotify_results[i]["spotify_uri"],
                    "preview_url": apple_results[j]["apple_preview_url"],
                    }

                apple_ids[apple_results[j]["apple_id"]] = 1
                songs.append(song)

    return songs
