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
|GET|[/mixtapes?search=<search_term>/](#search-MixTapes)|Search MixTape titles (limited to one search term)|
|POST|[/mixtapes/](#create-a-new-MixTape-for-this-user-logged-in-user)|Create a new MixTape|
|GET|[/mixtapes/{id}/](#details-for-a-specific-MixTape)|Details for a specific MixTape|
|PUT|[/mixtapes/{id}/](#update-an-existing-MixTape)|Update an existing question (Only the creator of the mixTape can do this)|
|PATCH|[/questions/{id}/](#update-part-of-an-existing-question)|Update part of an existing MixTape|
|POST|[/mixtapes/{id}/favorite/](#favorite-a-MixTape)|Favorite a MixTape|
|DELETE|[/mixtapes/{id}/](#delete-MixTape)|Delete an existing MixTape (Only the creator of the MixTape may do this)|
|GET|[/all_answers/](#list-all-answers)|List all answers (anonymous/guest)|
|GET|[/answers/](#list-all-user-created-answers)|List all logged in user created answers|
|GET|[/all_answers?search=<search_term>/](#search-answers)|Search answers (limited to one search term)|
|POST|[/questions/{id}/answers/](#create-a-new-answer)|Create a new answer|
|GET|[/answers/{id}/](#details-for-a-specific-answer)|Details for a specific answer|
|PUT|[/answers/{id}/](#update-an-existing-answer)|Update an existing answer|
|PATCH|[/answers/{id}/](#update-an-existing-answer)|Update an existing answer|
|PUT|[/all_answers/{id}/favorite/](#favorite-an-answer)|Favorite an answer|
|DELETE|[/answers/{id}/](#delete-answer)|Delete answer|
|PATCH|[/all_questions/{id}/all_answers/{id}/](#mark-answer-as-accepted)|Mark an answer as accepted|



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

Returns list of all questions for a logged in user.

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



## Search questions

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



## Favorite a question

Logged in user can favorite any question.

Requirement: user must be logged in.

### Request

Required in URL: MixTape's id.

```json
PUT /all_questions/id/favorite/
```

### Response

Return will be the question's id. 

```json
200 OK

{
	"id": 5
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

If another logged in user attempts to delete a question that is not theirs:
```json
404 Not Found
{
	"detail": "Not found."
}
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



## List all user created answers

Returns list of all answers for a logged in user.

### Request

```json
GET /answers/
```

### Response

```json
200 OK

[
	{
		"pk": 1,
		"author": "user1",
		"description": "user1 question1 answer1",
		"created_at": "2022-06-03T17:52:10.041543-04:00",
		"question": "user1 question1"
	},
	{
		"pk": 2,
		"author": "user1",
		"description": "user1 question1 answer2",
		"created_at": "2022-06-03T17:52:15.895155-04:00",
		"question": "user1 question1"
	},
]
```



## Search answers

Search through answers.

### Request

Note: can only use 1 search parameter. It queries the description field.

```json
GET /all_answers?search=to
```

### Response

```json
200 OK

[
	{
		"id": 14,
		"created_at": "2022-06-09T13:54:18.760647-04:00",
		"author": "Vader",
		"description": "You do not need an answer to this question.."
	},
	{
		"id": 7,
		"created_at": "2022-06-07T10:24:08.771366-04:00",
		"author": "user1",
		"description": "user1 response (.2) to user2's question pk4"
	}
]
```



## Create a new answer

Requirement: user must be logged in.

### Request

Requirement: description

Required in URL: question's id.

```json
POST /questions/id/answers/

{
	"description": "user1 response to user2's question pk4"
}
```

### Response

```json
200 OK
{
	"pk": 7,
	"author": "user1",
	"description": "user1 response to user2's question pk4",
	"created_at": "2022-06-07T10:24:08.771366-04:00",
	"question": "user2 question2"
}
```



## Details for a specific answer

Requirement: user must be logged in.

### Request

Required in URL: answer's id.

```json
GET /answers/id/
```

### Response

```json
200 OK

{
	"pk": 2,
	"author": "Vader",
	"description": "mebbe.. come to the moon by Alderaan!",
	"created_at": "2022-06-05T17:08:08.343275-04:00",
	"question": "Speeder"
}

```


## Update an existing answer

Requirement: user must be logged in.

### Request

Required field for PUT or PATCH: description 

Required in URL: answer's id.

```json
PUT /answer/id/ or PATCH /answer/id/ 

{
    "description": "come to Alderaan..",
}
```

### Response

```json
200 OK

{
	"pk": 2,
	"author": "Vader",
	"description": "come to Alderaan..",
	"created_at": "2022-06-05T17:08:08.343275-04:00",
	"question": "Speeder"
}
```



## Favorite an answer

Logged in user can favorite any answer.

Requirement: user must be logged in.

### Request

Required in URL: answer's id.

```json
PUT /all_answers/pk/favorite/
```

### Response

```json
200 OK
```



## Delete Answer

Requirement: user must be logged in. 

### Request

Required in URL: question id and answer id.

```json
DELETE /question/id/answers/id
```

### Response

A successful deletion returns:

```json
204 No Content
```



## Mark answer as accepted

Requirement: user must be logged in.

### Request

Required in URL: question id and answer id.

```json
PATCH /all_questions/id/all_answers/id/

200 OK 
{
	"accepted": true
}

```

### Response

Required field: accepted

```json
200 OK 
{
	"accepted": true
}
```