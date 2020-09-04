# Capstone Project - Casting Agency

Casting Agency URL: https://casting-agency-heroku-app.herokuapp.com/
Heroku GitHub repository: https://git.heroku.com/casting-agency-heroku-app.git 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once the virtual environment is setup and running, install dependencies by navigating to the working project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests. 

## Running the server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints

GET '/movies'
- First checks that the token provided is allowed to perform this operation. If authorized, then fetches a dictionary of movies.
- Request Arguments: token
- Returns: Each object in the movies dictionary and an object showing the total number of movies. 
```bash
{
    "movies": [
        {
            "id": 3,
            "release_date": "2008-05-02 00:00:00",
            "title": "Iron Man"
        },
        {
            "id": 2,
            "release_date": "2012-05-05 00:00:00",
            "title": "The Avengers"
        }
    ],
    "success": true,
    "total_movies": 2
}
```

GET '/actors'
- First checks that the token provided is allowed to perform this operation. If authorized, then fetches a dictionary of actors.
- Request Arguments: token
- Returns: Each object in the actors dictionary and an object showing the total number of actors. 
```bash
{
    "actors": [
        {
            "age": 55,
            "gender": "Male",
            "id": 2,
            "name": "Robert Downey Jr."
        },
        {
            "age": 35,
            "gender": "Female",
            "id": 3,
            "name": "RScarlett Johansson"
        }
    ],
    "success": true,
    "total_actors": 2
}
```

DELETE '/movies/<int:movie_id>'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in a movie ID, if the movie exists, then it is deleted from the database
- Request Arguments: token, movie_id 
- Returns: The ID of the deleted movie and each object in the list of modified movies and an object showing the total number of movies.
```bash
{
    "deleted": 1,
    "movies": [],
    "success": true,
    "total_movies": 0
}
```

DELETE '/actors/<int:actor_id>'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in a actor ID, if the actor exists, then it is deleted from the database
- Request Arguments: token, actor_id 
- Returns: The ID of the deleted actor and each object in the list of modified actors and an object showing the total number of actors.
```bash
{
    "actors": [],
    "deleted": 1,
    "success": true,
    "total_actors": 0
}
```

POST '/movies'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in an object with key value pairs for the new movie namely the title and release_date. 
- Request Arguments: token
- Returns: An object containing the newly created movie's id, each object in the list of modified movies and an object showing the total number of movies.
```bash
{
    "created": 2,
    "movies": [
        {
            "id": 2,
            "release_date": "2012-05-04 00:00:00",
            "title": "The Avengers"
        }
    ],
    "success": true,
    "total_movies": 1
}
```

POST '/actors'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in an object with key value pairs for the new actor namely the name, age and gender. 
- Request Arguments: token
- Returns: An object containing the newly created actors's id, each object in the list of modified actors and an object showing the total number of actors.
```bash
{
    "actors": [
        {
            "age": 55,
            "gender": "Male",
            "id": 2,
            "name": "Robert Downey Jr."
        }
    ],
    "created": 2,
    "success": true,
    "total_actors": 1
}
```

PATCH '/movies'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in an object with key value pairs for the desired fields to be changes. 
- Request Arguments: token, movie_id
- Returns: An object containing the updated movie.
```bash
{
    "movie": {
        "id": 2,
        "release_date": "2012-05-05 00:00:00",
        "title": "The Avengers"
    },
    "success": true
}
```

PATCH '/actors'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in an object with key value pairs for the desired fields to be changes. 
- Request Arguments: token, actor_id
- Returns: An object containing the updated actor.
```bash
{
    "actor": {
        "age": 35,
        "gender": "Female",
        "id": 3,
        "name": "Scarlett Johansson"
    },
    "success": true
}
```