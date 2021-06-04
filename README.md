# Pokedex

## About
This app provides a REST API for managing pokemons.

The functionalities include:
- storing Pokemon data in database
- getting all Pokemons, or getting one by id
- adding, deleting and Updating Pokemons
- searching by types and name
- pagination
- authentication
- API documentation
- error handling 

## Prerequisites
The project was developed and tested using Python 3.9 and Windows 10 and is not guaranteed
 to work with other Python releases or other OS's.
## Installation
Create the virtual environment:

 `python -m venv venv`
    
When on Windows you can explicitly specify the Python version by running:

 `py -3.9 -m venv venv`
 
Activate the virtual environment:

`venv\Scripts\activate.bat`

Install the requirements:

`pip install -r requirements.txt`

To set your own [SECRET KEY](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SECRET_KEY),
In the main project folder, create a new directory, called "sensitive_data". 
Inside, create a file called "passes.json" which should contain JSON data, where the key
is "secret_key" and the value is your secret key.

## Usage

To use the app, first, start your server on localhost:


`py manage.py runserver`

by default, it will run on http://127.0.0.1:8000.

To use the API, you can either use Django Rest Framework's browsable API by entering 
http://127.0.0.1:8000/api/ in your browser, or use a tool like [Postman](https://www.postman.com)

This repository comes with populated database, but if, for some reason, your database records get
deleted, you can restore it to its initial state by reinstalling fixtures (the data was taken 
from [here](https://gist.github.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6)):

`py manage.py loaddata fixtures.json`

### Examples

##### List all Pokemons

`GET http://127.0.0.1:8000/api/pokemon/`

##### Get a single Pokemon by id

`GET http://127.0.0.1:8000/api/pokemon/5/`

##### Create a new Pokemon

`POST http://127.0.0.1:8000/api/pokemon/ {"name": "TestPokemon",
        "type1": "Fire",
        "legendary": True}`

##### Delete a single Pokemon by id

`DELETE http://127.0.0.1:8000/api/pokemon/5/`

##### Update a Pokemon

`PUT http://127.0.0.1:8000/api/pokemon/ {"name": "TestPokemon",
        "type1": "Fire",
        "legendary": True}`

##### Partially update a Pokemon

`PATCH http://127.0.0.1:8000/api/pokemon/ {"attack": 42}`

### Authentication and permissions
All users are allowed to read Pokemon info. Only authenticated users are allowed to create
a new Pokemon, and in order to be able to delete or update a Pokemon, you need to be its 
creator.

### Searching and filtering

You can search and filter by types and name.

Searching and filtering is done two ways. You can either specify what parameter you want 
to filter against. The request:

`GET http://127.0.0.1:8000/api/pokemon/?type1=Fire`

will return all the pokemons with type1 = 'Fire'

The other way is to use the broader "search" clause. The request:

`GET http://127.0.0.1:8000/api/pokemon/?search=char`

will return all the pokemons with name, type1 or type2 containing phrase "char"



## API documentation

Documentation for this API is provided in both Swagger (http://127.0.0.1:8000/docs/swagger/)
, and ReDoc (http://127.0.0.1:8000/docs/redoc/) format. This was done using a great [yasg](https://github.com/axnsan12/drf-yasg)
library. 

## Testing

To test the project, run :

`
py manage.py test manage_pokemons.tests
`