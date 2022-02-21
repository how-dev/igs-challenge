# Howard's Technical Test

## Introduction

Hi! This is the tutorial on how to upload 
the project locally and the documentation of its endpoints.

## Running the project locally

1. First, create the .env file inside the core_api directory
2. Create "migrations" modules within each app. Don't forget __init__.py
3. As this is a technical test, I will provide the data to be inserted inside the .env file:

```dotenv
SECRET_KEY=django-insecure-o!1)-*j0iq@!kd6tptwu=gyuj$h3)n=b($w=8^g-i-4(2cp=y^

POSTGRES_DB=postgres
POSTGRESD_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432

PAGE_SIZE=15
```

4. Create a docker volume on your machine with the following command:

```commandline
docker volume create --name=igs_challenge
```

5. Run the following command to upload the docker services:

```commandline
docker-compose up --build
```

6. Open another terminal and access the docker machine with the following command:

```commandline
docker exec -it igs-challenge_web_1 /bin/bash
```

or (to zsh system):

```commandline
docker exec -it igs-challenge_web_1 /bin/sh
```

7. Run the following command:

```commandline
python manage.py makemigrations
```

Then:

```commandline
python manage.py migrate
```

8. Run the following custom command to create 500 users in the database and 1 user for you to test the routes and admin

```commandline
python manage.py start_igs_test
```

And a user with the following credentials will be created

```json
{
  "email": "igs_tester@igs-software.com.br",
  "password": "1g5@t35t3r"
}
```

## API

### Concept

`base_url` = http://localhost:8000/

> __Me__ as a user of the RH department
> 
> __can I__ list
> 
> __can I__ edit
> 
> __can I__ create
> 
> __can I__ delete
> 
> __Any other__ company user.

### Login

`endpoint` = login/

allowed_methods = `POST`

__Example__:

`POST`

body:
```json
{
  "email": "example@example.com",
  "password": "example_password"
}
```

response:
```json
{
  "status": 200,
  "result": {
  "id": 123,
  "name": "IGS Tester",
  "email": "igs_tester@igs-software.com.br",
  "document": "00022255588",
  "last_login": "2022-02-21T16:40:17.496420-03:00",
  "date_joined": "2022-02-21T16:40:14.601272-03:00",
  "is_superuser": true,
  "department": {
    "id": 2,
    "name": "RH"
  }, 
  "token": "c0a04f687aa5e60b7c62dc7ed8a052f199e68408"
  }
}
```

status: _200 OK_

### Employee

`endpoint` = employee/

allowed_methods = `POST`, `GET`, `PATCH`, `PUT`, `DELETE`

__Example__:

### `POST`

header:

key: `Authorization`

value: `Bearer < token >`

body:

```json
{
  "name": "Test",
  "email": "test@testt.com",
  "password": "bla",
  "document": "62208311361",
  "department": {
    "name": "RH"
  },
  "is_staff": true,  // optional
  "is_superuser": true  // optional
}
```

response:

```json
{
  "id": 1278,
  "name": "Test",
  "email": "test@testt.com",
  "document": "62208311361",
  "last_login": null,
  "date_joined": "2022-02-21T17:51:59.848146-03:00",
  "is_superuser": true,
  "department": {
    "id": 3,
    "name": "RH"
  }
}
```

status: _201 CREATED_

### `GET`

body: No Body

header:

key: `Authorization`

value: `Bearer < token >`


response:

```json
{
  "count": 505,
  "next": "http://localhost:8000/employee/?page=2",
  "previous": null,
  "results": [
    {
      "id": 3,
      "name": "admin",
      "email": "admin@admin.com",
      "document": "06872098112",
      "last_login": "2022-02-21T15:52:30.484683-03:00",
      "date_joined": "2022-02-21T14:00:03.461903-03:00",
      "is_superuser": true,
      "department": {
        "id": 2,
        "name": "RH"
      }
    },
    {
      "id": 7,
      "name": "Test",
      "email": "test@testt.com",
      "document": "62208311361",
      "last_login": "2022-02-21T16:06:07.828693-03:00",
      "date_joined": "2022-02-21T16:05:54.144545-03:00",
      "is_superuser": true,
      "department": {
        "id": 3,
        "name": "bla"
      }
    },
    {"": "And more..."}
  ]
}
```

status: _200 OK_

> OBS: You can GET retrieve with employee/< int:employee_id >/

### `PATCH`

> You need to put the id of whomever you want to select, employee/< int:employee_id >/

header:

key: `Authorization`

value: `Bearer < token >`

body:

```json
{
  "name": "DocumentationTest"
}
```

response:

```json
{
  "id": 3,
  "name": "DocumentationTest",
  "email": "admin@admin.com",
  "document": "06872098112",
  "last_login": "2022-02-21T15:52:30.484683-03:00",
  "date_joined": "2022-02-21T14:00:03.461903-03:00",
  "is_superuser": true,
  "department": {
    "id": 2,
    "name": "RH"
  }
}
```

status: _200 OK_

### `PUT`

> You need to put the id of whomever you want to select, employee/< int:employee_id >/

header:

key: `Authorization`

value: `Bearer < token >`

body:

```json
{
  "name": "DocumentationTestPUT",
  "email": "admin@admin.com",
  "document": "06872098112",
  "last_login": "2022-02-21T15:52:30.484683-03:00",
  "date_joined": "2022-02-21T14:00:03.461903-03:00",
  "is_superuser": true,
  "department": {
    "id": 2,
    "name": "RH"
  }
}
```

response:

```json
{
  "id": 3,
  "name": "DocumentationTestPUT",
  "email": "admin@admin.com",
  "document": "06872098112",
  "last_login": "2022-02-21T15:52:30.484683-03:00",
  "date_joined": "2022-02-21T14:00:03.461903-03:00",
  "is_superuser": true,
  "department": {
    "id": 2,
    "name": "RH"
  }
}
```

### `DELETE`

> You need to put the id of whomever you want to select, employee/< int:employee_id >/

header:

key: `Authorization`

value: `Bearer < token >`

body: No Body

response: No Content

status: _204 NO CONTENT_

> OBS: All deletions are only logical, that is, they do not remove from the database, they only inactivate the system.


## ADMIN

To access Django Admin, you can use the same user credentials:

```json
{
  "email": "igs_tester@igs-software.com.br",
  "password": "1g5@t35t3r"
}
```

Or create a user via the command:

```commandline
python manage.py createsuperuser
```

All superusers created are part of the RH department.
