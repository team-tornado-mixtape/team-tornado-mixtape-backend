# MixTape

Let's get ready to jam!  Mixtape allows users to create authorization and upon signing in, the ability to create Mixtapes.  When a user searches for songs by song title or artist, relevant information is pulled from the Spotify and Apple Music APIs and added to a list of songs which a user can compile into a Mixtape. Songs are kept in the database and made available to other users for faster search capabilities.


*Mixtape is an Application Programming Interface (API) built using Django Rest Framework (DRF)

All requests require authentication.



## Base URL:

All endpoints begin with `https://team-tornado-mixtape.herokuapp.com/`

NOTE: API Root is /api/


|  Method  |  Endpoint  |  Description |
| -------- | ---------- | ------------ |
|POST|[/auth/users/](#create-a-new-user)|Create a new user|
|POST|[/auth/token/login/](#login-user)|Login user|
|POST|[/auth/users/me/](#users-info)|User's info|
|POST|[/auth/token/logout/](#logout-user)|Logout user|
|GET|[/mixtapes/](#list-of-all-MixTapes)|List all public MixTapes|
|GET|[/my/mixtapes](#list-of-MixTapes-per-user)|List all MixTapes of logged in user|
|GET|[/my/profile](#show-Logged-In-User-Profile)|Show profile of logged in user|
|GET|[/followers](#list-of-followers)|List all followers of logged in user|
|GET|[/following](#list-of-following)|List all users that current user is following|
|GET|[/mixtapes?search=<search_term>](#search-MixTapes)|Search MixTape titles (limited to one search term)|
|POST|[/mixtapes/](#create-a-new-MixTape)|Create a new MixTape|
|GET|[/mixtapes/{id}](#details-for-a-specific-MixTape)|Details for a specific MixTape|
|PUT|[/mixtapes/{id}](#update-an-existing-MixTape)|Update an existing  (Only the creator of the MixTape can do this)|
|PATCH|[/mixtapes/{id}](#update-part-of-an-existing-mixtape)|Update part of an existing MixTape|
|POST|[/mixtapes/{id}/favorite/](#favorite-a-MixTape)|Favorite a MixTape|
|POST|[/mixtapes/{id}/follow/](#follow-a-User)|Follow a user's profile|
|DELETE|[/mixtapes/{id}/](#delete-MixTape)|Delete an existing MixTape (Only the creator of the MixTape may do this)|
|GET|[/profiles](#list-All-Profiles)|List all profiles|
|GET|[/profiles?search=<search_term>](#search-Profiles)|Search profiles (by username)|
|GET|[/search?track=&artist=&limit=](#search-spotify-and-apple-music-APIs)|Search for songs in Apple Music and Spotify API|
|GET|[/api/songs?search=<search_term>](#search-local-database)|Search local database for song titles|




## Create a new user

### Request

Required fields: username and password

Optional fields: email

```json
POST auth/users/

{
  "username": "Luke",
  "password": "Momentum1"
}
```

### Response

Response: If you receive the same info you provided, user creation was successful!

```json
201 Created

{
  "email": "", 
  "username": "Luke",
  "id": 4, 
}

```


## Login user

### Request

Required fields: username, password

```json
POST auth/token/login/

{
    "username": "Luke",
    "password": "Momentum1"
}
```

### Response

```json
200 OK

{
    "auth_token": "d99a2de1b0a09db0fc2da23c9fdb1fc2447fff5d"
}
``` 
NOTE: auth_token must be passed for all requests with the logged in user. It remains active till user is [logged out](#logout-user).


## User's info

Requirement: user must be logged in.

```json
GET /auth/users/me/
```

### Response

```json
200 OK

{
    "id": 4,
    "username": "Luke",
    "email": "",
}
```



## Logout user

### Request

Required fields: None

```json
POST /auth/token/logout/
```

### Response

```json
204 No Content
```



## list of all MixTapes

Returns list of all MixTapes.

### Request

Required fields: None

```json
GET /mixtapes/
```

### Response

```json
200 OK

[
	{
		"id": 1,
		"title": "Mixtape 1",
		"created_at": "2022-06-22T14:46:22.036783-04:00",
		"creator": "User1",
		"songs": [
			2,
			4
		]
	},
	{
		"id": 2,
		"title": "Mixtape 2",
		"created_at": "2022-06-22T14:46:37.815208-04:00",
		"creator": "User1",
		"songs": [
			2,
			3
		]
	},
	{
		"id": 3,
		"title": "Mixtape 3",
		"created_at": "2022-06-22T14:46:51.199678-04:00",
		"creator": "User2",
		"songs": [
			2
		]
	},
]
```



## list of MixTapes per user

Returns list of all MixTapes for a logged in user.

### Request

Requirement: user must be logged in.

```json
GET /my/mixtapes
```

### Response

```json
200 OK

[
	{
		"id": 3,
		"title": "Mixtape 3",
		"created_at": "2022-06-22T14:46:51.199678-04:00",
		"creator": "User2",
		"songs": [
			2
		]
	},
	{
		"id": 5,
		"title": "Mixtape 5",
		"created_at": "2022-06-22T16:01:02.607586-04:00",
		"creator": "User2",
		"songs": []
	}
]
```



## Search MixTapes

Search through MixTapes.

### Request

Note: can only use 1 search parameter. It queries MixTape title.

```json
GET /mixtapes?search=kitty
```

### Response

```json
200 OK

[
	{
		"id": 5,
		"title": "Mixtape 5 Kitty Jams",
		"created_at": "2022-06-22T16:01:02.607586-04:00",
		"creator": "User2",
		"songs": []
	}
]
```



## Create a new MixTape (logged in user)

Requirement: user must be logged in.

### Request

Required fields: title,description, songs

```json
POST /mixtapes/

{
		"title": "Mixtape 5",
		"creator": "3",
		"description": "lotsa songs",
		"songs": [ 2
]
}
```

### Response

```json
201 Created

{
	"created_at": "2022-06-23T15:25:24.109951-04:00",
	"creator": null,
	"title": "Mixtape 5",
	"songs": [
		2
	],
	"theme": 0,
	"is_public": false,
	"description": "lotsa songs",
	"modified_at": "2022-06-23T15:25:24.109991-04:00",
	"favorited_by": []
}
```

If anonymous / guest user attempts to POST:

```json
401 Unauthorized

{
	"detail": "Authentication credentials were not provided."
}
```



## Details for a specific MixTape

Requirement: user must be logged in.

### Request

```json
GET /mixtapes/id/ 
```

### Response

Response for GET: id, created_at, title, creator, description,is_public,theme, modified_at,favorited_by and songs. 

```json
200 OK

{
	"id": 4,
	"created_at": "2022-06-22T14:47:19.126652-04:00",
	"creator": "User3",
	"title": "Mixtape 4",
	"songs": [
		2,
		3,
		4
	],
	"theme": 0,
	"is_public": false,
	"description": "Mixtape 4 description",
	"modified_at": "2022-06-22T14:47:19.126713-04:00",
	"favorited_by": [
		3
	]
}
```



## Update an existing MixTape

Requirement: user must be logged in, user must be creator of MixTape

### Request

Required fields: songs and description 

```json
PUT /mixtapes/id/

{
		"title": "Mixtape 5",
		"creator": "3",
		"description": "lotsa songs",
		"songs": [ 2
]
}
```

### Response

```json
200 OK

{
	"created_at": "2022-06-23T15:25:24.109951-04:00",
	"creator": null,
	"title": "Mixtape 5",
	"songs": [
		2
	],
	"theme": 0,
	"is_public": false,
	"description": "lotsa songs",
	"modified_at": "2022-06-23T15:25:24.109991-04:00",
	"favorited_by": []
}
```

If non-creator attempts to PUT:

```json
403 Forbidden

{
	"detail": "Editing MixTapes is restricted to the creator only."
}
```


## Update part of an existing MixTape

Requirement: user must be logged in.

### Request

Required fields: title and/or description 

```json
PATCH /mixtapes/id/ 

{
		"title": "Mixtape 3 newer title"


}
```

### Response

```json
200 OK

{
	"id": 3,
	"created_at": "2022-06-22T14:46:51.199678-04:00",
	"creator": "User2",
	"title": "Mixtape 3 newer title",
	"songs": [
		2
	],
	"theme": 0,
	"is_public": false,
	"description": "Mixtape 3 description",
	"modified_at": "2022-06-23T16:10:55.002153-04:00",
	"favorited_by": [
		4
	]
}
```
If non-creator attempts to PUT:

```json
403 Forbidden

{
	"detail": "Editing MixTapes is restricted to the creator only."
}
```



## Favorite a MixTape

Logged in user can favorite any MixTape.

Requirement: user must be logged in.

### Request

Required in URL: MixTape's id.

```json
POST /mixtape/id/favorite/
```

### Response


```json
201 Created

{
	"created_at": "2022-06-22T14:46:37.815208-04:00",
	"creator": "User1",
	"title": "Mixtape 2",
	"songs": [
		2,
		3
	],
	"theme": 0,
	"is_public": false,
	"description": "Mixtape 2 description",
	"modified_at": "2022-06-22T14:46:37.815274-04:00",
	"favorited_by": [
		3,
		4
	]
}
```



## Delete MixTape

Requirement: user must be logged in and user must be creator of MixTape

### Request

Required in URL: MixTape's id.

```json
DELETE /mixtapes/id/
```

### Response

A successful deletion returns:

```json
204 No Content
```

If non-creator tries to delete a mixtape:
```json
401 Unauthorized
{
	"detail": "Editing MixTapes is restricted to the creator only."
}
```



## List all profiles

Returns list of all profiles.

User can be anonymous / guest or logged in.

### Request

```json
GET /profiles/
```

### Response

```json
200 OK

[

	{
		"id": 1,
		"user": "User2",
		"created_at": "2022-06-22T16:35:54.792728-04:00",
		"image": "http://127.0.0.1:8000/files/profilepics/unnamed.jpeg",
		"followed_by": [
			3
		]
	}
]
	
```


## Search Profiles

Search through profiles by user name

### Request

Note: can only use 1 search parameter. It queries the username.

```json
GET /profiles?search=kitten
```

### Response

```json
200 OK

{
		"id": 1,
		"user": "kitten",
		"created_at": "2022-06-22T16:35:54.792728-04:00",
		"image": "http://127.0.0.1:8000/files/profilepics/unnamed.jpeg",
		"followed_by": [
			3
		]
	}
```

## Details for a profile

Requirement: user must be logged in.

### Request

Required in URL: profile's id.

```json
GET /profiles/1
```

### Response

```json
200 OK

{
	"id": 1,
	"user": "kitten",
	"created_at": "2022-06-22T16:35:54.792728-04:00",
	"image": "http://127.0.0.1:8000/files/profilepics/unnamed.jpeg",
	"followed_by": [
		3
	]
}

```


## Update an existing profile

Requirement: updater must be owner of the profile

### Request

Required field for PUT or PATCH: description 

Required in URL: profile's id.

```json
PUT /profiles/id/ or PATCH /profiles/id/ 

{
    "image": "http://127.0.0.1:8000/files/profilepics/unnamed.jpeg",
}
```

### Response

```json
200 OK

{
	"id": 1,
	"user": "kitten",
	"created_at": "2022-06-22T16:35:54.792728-04:00",
	"image": "http://127.0.0.1:8000/files/profilepics/unnamed.jpeg",
	"followed_by": [
		3
	]
}
```



## Follow a User

Logged in user can follow any user's profile

Requirement: user must be logged in.

### Request

Required in URL: profile's id.

```json
PUT /profiles/<int:profile_pk>/followers
```

### Response

```json
201 CREATED
{
	"id": 1,
	"user": "kitten",
	"created_at": "2022-06-22T16:35:54.792728-04:00",
	"image": "http://127.0.0.1:8000/files/profilepics/unnamed.jpeg",
	"followed_by": [
		3
	]
}
```


## List favorite MixTapes

Returns list of all the favorite MixTapes of logged in users.

User can be anonymous / guest or logged in.

### Request

```json
GET /my/favorites
```

### Response

```json
200 OK

[

	{
		"id": 1,
		"user": "User2",
		"created_at": "2022-06-22T16:35:54.792728-04:00",
		"image": "http://127.0.0.1:8000/files/profilepics/unnamed.jpeg",
		"followed_by": [
			3
		]
	}
]
	
```

## List Followers

### Request

```json
GET /followers
```

### Response

```json
200 OK

[

[
	{
		"followed_by": [
			"Lammalammadingdong"
		]
	}
]
]
	
```

## Show Logged In User Profile

Requirement: user must be logged in.

### Request

Required in URL: profile's id.

```json
GET /profiles/1
```

### Response

```json
200 OK

{
	"id": 1,
	"user": "kitten",
	"created_at": "2022-06-22T16:35:54.792728-04:00",
	"image": "http://127.0.0.1:8000/files/profilepics/unnamed.jpeg",
	"followed_by": [
		3
	]
}

```


## List of following
Shows a list of all the users the current user is following

### Request

```json
GET /following
```

### Response

```json
200 OK

[

	{
		"id": 2,
		"user": "Lammalammadingdong",
		"followed_by": [
			"kitten",
			"hueylooway",
			"chunkamonka"
		],
		"created_at": "2022-06-24T18:52:00.988019-04:00",
		"image": "http://127.0.0.1:8000/files/profilepics/bluegrass_betty.jpeg"
	}

]
	
```

## Search Spotify and Apple Music APIs


### Request

```json
GET /search?track=yellow
```

### Response

```json
200 OK

{
		"id": 103,
		"created_at": "2022-06-24T15:25:30.005403-04:00",
		"title": "Bodak Yellow",
		"artist": "Cardi B",
		"album": "Invasion of Privacy",
		"spotify_id": "3HOXNIj8NjlgjQiBd3YVIi",
		"spotify_uri": "spotify:track:3HOXNIj8NjlgjQiBd3YVIi",
		"apple_id": "1368156577",
		"mixtapes": []
	},
	{
		"id": 102,
		"created_at": "2022-06-24T15:25:30.004726-04:00",
		"title": "Bodak Yellow",
		"artist": "Cardi B",
		"album": "Invasion of Privacy",
		"spotify_id": "3HOXNIj8NjlgjQiBd3YVIi",
		"spotify_uri": "spotify:track:3HOXNIj8NjlgjQiBd3YVIi",
		"apple_id": "1368156577",
		"mixtapes": []
	},
    ...

```

### Request

```json
GET /search?track=yellow&artist=coldplay
```

### Response

```json
200 OK

{
		"id": 123,
		"created_at": "2022-06-24T15:27:24.405165-04:00",
		"title": "Yellow",
		"artist": "Coldplay",
		"album": "Parachutes",
		"spotify_id": "3AJwUDP919kvQ9QcozQPxg",
		"spotify_uri": "spotify:track:3AJwUDP919kvQ9QcozQPxg",
		"apple_id": "1122782283",
		"mixtapes": []
	},
	{
		"id": 122,
		"created_at": "2022-06-24T15:27:24.404367-04:00",
		"title": "Yellow",
		"artist": "Coldplay",
		"album": "Parachutes",
		"spotify_id": "3AJwUDP919kvQ9QcozQPxg",
		"spotify_uri": "spotify:track:3AJwUDP919kvQ9QcozQPxg",
		"apple_id": "1122782283",
		"mixtapes": []
	},
    ...

```



## Search Local Database


### Request

```json
GET /api/songs?search=black
```

### Response

```json
200 OK

{
		"id": 13,
		"created_at": "2022-06-24T15:03:55.069226-04:00",
		"title": "Black and Yellow",
		"artist": "Wiz Khalifa",
		"album": "Rolling Papers (Deluxe Version)",
		"spotify_id": "6OL3ylnbe2DWDWpiYnUwba",
		"spotify_uri": "spotify:track:6OL3ylnbe2DWDWpiYnUwba",
		"apple_id": "426663069",
		"mixtapes": []
	},
	{
		"id": 16,
		"created_at": "2022-06-24T15:03:55.070543-04:00",
		"title": "Black and Yellow",
		"artist": "Wiz Khalifa",
		"album": "Rolling Papers (Deluxe Version)",
		"spotify_id": "6OL3ylnbe2DWDWpiYnUwba",
		"spotify_uri": "spotify:track:6OL3ylnbe2DWDWpiYnUwba",
		"apple_id": "426663069",
		"mixtapes": []
	},
```
