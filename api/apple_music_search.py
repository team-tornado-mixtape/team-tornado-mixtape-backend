import datetime
import jwt
from urllib.parse import urlencode


secret = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgzWJ1tPxyB39nEjUn
WCjymhCf2sfZF6IO3VJPNqpmRFOgCgYIKoZIzj0DAQehRANCAARE/4mbn57GPe8n
/yd3zQ005COG7hj0A8L4f/4KoU4eDj1piuShHjdY3rle6TnAqw+srQBxjcCkvA2v
692QycXe
-----END PRIVATE KEY-----"""

key_ID = "5BBHF2WLJF"
team_ID = "C2NAAJY6Z3"
alg = "ES256"

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

if __name__ == "__main__":
    token = jwt.encode(payload, secret, algorithm=alg, headers=headers)

    print("----TOKEN----")
    print(token)

    search = "Walk the Walk"

    endpoint = "https://api.music.apple.com/v1/catalog/US/search"

    data = urlencode({
        "types": "songs",
        "term": f"{search}",
        "limit": 1
        })

    print("----CURL----")
    print(f"curl -v -H 'Authorization: Bearer %s' \"{endpoint}?{data}\" " % (token))
