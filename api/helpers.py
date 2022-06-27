from difflib import SequenceMatcher
from api.spotify_search import *
from api.apple_music_search import *


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def my_search(search_track=None, search_artist=None, limit=20):
    spotify_results = SearchSpotifyAPI(search_track=search_track, search_artist=search_artist, limit=limit)
    apple_results = SearchAppleMusicAPI(search_track=search_track, search_artist=search_artist, limit=limit)
    songs = []
    spotify_ids = {}
    apple_ids = {}

    for i in range(len(spotify_results)):
        similarities = []
        for j in range(len(apple_results)):
            similarity = similar(spotify_results[i]["spotify_title"], apple_results[j]["apple_title"]) + similar(spotify_results[i]["spotify_artist"], apple_results[j]["apple_artist"])
            similarities.append(similarity)

        closest = max(similarities)
        index = similarities.index(closest)

        if closest > 1.6 and spotify_results[index]["spotify_id"] not in spotify_ids and apple_results[index]["apple_id"] not in apple_ids:
            song = {
                "title": apple_results[index]["apple_title"],
                "artist": apple_results[index]["apple_artist"],
                "album": apple_results[index]["apple_album"],
                "spotify_id": spotify_results[index]["spotify_id"],
                "apple_id": apple_results[index]["apple_id"],
                "spotify_uri": spotify_results[index]["spotify_uri"],
                "preview_url": apple_results[index]["apple_preview_url"],
                }

            spotify_ids[song['spotify_id']] = 1
            spotify_ids[song['apple_id']] = 1
            songs.append(song)

    return songs
