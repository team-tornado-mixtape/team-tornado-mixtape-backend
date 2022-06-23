# MixTape

Let's get ready to jam!  Mixtape allows users to create authorization and upon signing in, the ability to create Mixtapes.  When a user searches for songs by song title, relevant information is pulled from the Spotify and Apple Music APIs and added to a list of songs which a user can compile as a Mixtape. 


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
|GET|[/users/<int:pk>/mixtapes](#list-of-MixTapes-per-user)|List all MixTapes of one user|
|GET|[/mixtapes?search=<search_term>](#search-MixTapes)|Search MixTape titles (limited to one search term)|
|POST|[/mixtapes/](#create-a-new-MixTape-for-this-user-logged-in-user)|Create a new MixTape|
|GET|[/mixtapes/{id}/](#details-for-a-specific-MixTape)|Details for a specific MixTape|
|PUT|[/mixtapes/{id}/](#update-an-existing-MixTape)|Update an existing  (Only the creator of the mixTape can do this)|
|PATCH|[/mixtapes/{id}/](#update-part-of-an-existing-mixtape)|Update part of an existing MixTape|
|POST|[/mixtapes/{id}/favorite/](#favorite-a-MixTape)|Favorite a MixTape|
|DELETE|[/mixtapes/{id}/](#delete-MixTape)|Delete an existing MixTape (Only the creator of the MixTape may do this)|
|GET|[/profiles](#list-all-profiles)|List all profiles|
|GET|[/profiles?search=<search_term>](#search-profiles)|Search profiles (by username)|
|GET|[/search?search=<search_term>](#seach-Spotify-and-Apple-Music-APIs)|Search for songs in Apple Music and Spotify API|




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



## List of all MixTapes

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
GET /users/<int:pk>/mixtapes
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



## Search Apple Music and Spotify API



### Request



Required in URL: song title

```json
GET /search?search=primadonna

```

### Response

```json
200 OK
[
	{
		"id": 9,
		"created_at": "2022-06-23T18:13:28.868948-04:00",
		"title": "Primadonna",
		"artist": "LA Nightcore",
		"album": "Primadonna - Single",
		"spotify_id": "0nrkiWaB513DpnvJZ8he4v",
		"apple_id": "1629176796",
		"mixtapes": []
	},
	{
		"id": 8,
		"created_at": "2022-06-23T18:13:28.868266-04:00",
		"title": "Primadonna",
		"artist": "Marina and The Diamonds",
		"album": "Electra Heart (Deluxe Version)",
		"spotify_id": "4sOX1nhpKwFWPvoMMExi3q",
		"apple_id": "534340044",
		"mixtapes": []
	},
	{
		"id": 7,
		"created_at": "2022-06-23T18:13:28.867619-04:00",
		"title": "Primadonna",
		"artist": "LA Nightcore",
		"album": "Primadonna - Single",
		"spotify_id": "0nrkiWaB513DpnvJZ8he4v",
		"apple_id": "1629176796",
		"mixtapes": []
	}
]
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









