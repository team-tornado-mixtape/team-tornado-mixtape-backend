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

secret = env.str("APPLE_SECRET", multiline=True)


def SearchAppleMusicAPI(search, limit=10):

    time_now = datetime.datetime.now()
    time_expired = time_now + datetime.timedelta(hours=12)

    headers = {"alg": alg, "kid": KEY_ID}

    payload = {
        "iss": TEAM_ID,
        "exp": int(time_expired.strftime("%s")),
        "iat": int(time_now.strftime("%s")),
    }

    token = jwt.encode(payload, secret, algorithm=alg, headers=headers)

    data = urlencode({"types": "songs", "term": f"{search}", "limit": f"{limit}"})

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
        result["apple_url"] = req.json()["results"]["songs"]["data"][i]["attributes"][
            "url"
        ]
        results.append(result)

    # print(json.dumps(req.json(), sort_keys=4,indent=4))
    return results


# apple_search_results = SearchAppleMusicAPI("Brickhouse")
# print(apple_search_results)
