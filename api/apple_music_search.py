import datetime
import jwt
from urllib.parse import urlencode
import environ
import requests
import json
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

KEY_ID = env("APPLE_KEY_ID")
TEAM_ID = env("APPLE_TEAM_ID")
alg = "ES256"

secret = f"""
-----BEGIN PRIVATE KEY-----
{env("APPLE_SECRET1")}
{env("APPLE_SECRET2")}
{env("APPLE_SECRET3")}
{env("APPLE_SECRET4")}
-----END PRIVATE KEY-----
"""


def SearchAppleMusicAPI(search_track=None, search_artist=None, limit=20):

    time_now = datetime.datetime.now()
    time_expired = time_now + datetime.timedelta(hours=12)

    headers = {"alg": alg, "kid": KEY_ID}

    payload = {
        "iss": TEAM_ID,
        "exp": int(time_expired.strftime("%s")),
        "iat": int(time_now.strftime("%s")),
    }

    token = jwt.encode(payload, secret, algorithm=alg, headers=headers)

    if search_track is not None and search_artist is None:
        data = urlencode({"types": "songs", "term": f"{search_track}", "limit": f"{limit}"})
    elif search_track is None and search_artist is not None:
        data = urlencode({"types": "songs", "term": f"{search_artist}", "limit": f"{limit}"})
    elif search_track is not None and search_artist is not None:
        data = urlencode({"types": "songs", "term": f"{search_track} {search_artist}", "limit": f"{limit}"})

    url = f"https://api.music.apple.com/v1/catalog/US/search?{data}"

    req = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    results = []

    for i in range(len(req.json()["results"]["songs"]["data"])):
        result = {"apple_id": req.json()["results"]["songs"]["data"][i]["id"]}
        result["apple_title"] = req.json()["results"]["songs"]["data"][i]["attributes"][
            "name"
        ]
        result["apple_album"] = req.json()["results"]["songs"]["data"][i]["attributes"][
            "albumName"
        ]
        result["apple_artist"] = req.json()["results"]["songs"]["data"][i][
            "attributes"
        ]["artistName"]
        result["apple_url"] = req.json()["results"]["songs"]["data"][i]["attributes"]["url"]
        result["apple_preview_url"] = req.json()["results"]["songs"]["data"][i]["attributes"]['previews'][0]["url"]
        results.append(result)

    # print(json.dumps(req.json(), sort_keys=4,indent=4))
    return results


# apple_search_results = SearchAppleMusicAPI(search_track="Enter Galactic", search_artist='Kid Cudi')
# print(apple_search_results)
