import datetime
import jwt
from urllib.parse import urlencode
import environ
import os
import requests
import json

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

key_ID = env('apple_key_ID')
team_ID = env('apple_team_ID')
alg = "ES256"

secret = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgzWJ1tPxyB39nEjUn
WCjymhCf2sfZF6IO3VJPNqpmRFOgCgYIKoZIzj0DAQehRANCAARE/4mbn57GPe8n
/yd3zQ005COG7hj0A8L4f/4KoU4eDj1piuShHjdY3rle6TnAqw+srQBxjcCkvA2v
692QycXe
-----END PRIVATE KEY-----"""


def apple_music_search(search, limit=10):
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
        "types": "songs,artists",
        "term": f"{search}",
        "limit": f"{limit}"
        })

    url = f"https://api.music.apple.com/v1/catalog/US/search?{data}"

    req = requests.get(url, headers={'Authorization': "Bearer " + token})

    return req.json()

search_results = apple_music_search("Enter Galactic", limit=1)
print(search_results)
