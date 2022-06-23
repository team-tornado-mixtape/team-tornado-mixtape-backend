import datetime
import jwt
from urllib.parse import urlencode
import environ
import requests
import json

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

key_ID = env('apple_key_ID')
team_ID = env('apple_team_ID')
alg = "ES256"

secret = env.str('apple_secret', multiline=True)


def SearchAppleMusicAPI(search, limit=10):
    if __name__ != "__main__":
        return

    time_now = datetime.datetime.now()
    time_expired = time_now + datetime.timedelta(hours=12)

    headers = {
        "alg": alg,
        "kid": key_ID
    }

    payload = {
        "iss": team_ID,
        "exp": int(time_expired.strftime("%s")),
        "iat": int(time_now.strftime("%s"))
    }

    token = jwt.encode(payload, secret, algorithm=alg, headers=headers)

    data = urlencode({
        "types": "songs",
        "term": f"{search}",
        "limit": f"{limit}"
        })

    url = f"https://api.music.apple.com/v1/catalog/US/search?{data}"

    req = requests.get(url, headers={'Authorization': "Bearer " + token})

    results = []

    for i in range(len(req.json()['results']['songs']['data'])):
        result = {"apple_id": req.json()['results']['songs']['data'][i]['id']}
        result["apple_title"] = req.json()['results']['songs']['data'][i]['attributes']['name']
        result["apple_album"] = req.json()['results']['songs']['data'][i]['attributes']['albumName']
        result["apple_artist"] = req.json()['results']['songs']['data'][i]['attributes']['artistName']
        result["apple_url"] = req.json()['results']['songs']['data'][i]['attributes']['url']
        results.append(result)

    # print(json.dumps(req.json(), sort_keys=4,indent=4))
    return results


# apple_search_results = SearchAppleMusicAPI("Brickhouse")
# print(apple_search_results)
