import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor
from dotenv import load_dotenv

# using dotenv to unpack the environment variables
load_dotenv()

# assigning env variables to contants
CASTING_ASSISTANT = os.environ.get('CASTING_ASSISTANT_JWT')
CASTING_DIRECTOR = os.environ.get('CASTING_DIRECTOR_JWT')
EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER_JWT')

def get_headers(token):
    return {'Authorization': f'Bearer {token}'}

class AgencyTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_agency"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'Psqlpass!', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        # Executed after reach test
        pass

    # test and error tests for each enpoint (get, delete, post, patch)
    def test_get_paginated_movies(self):
        res = self.client().get('/movies', headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_error_get_paginated_movies(self):
        res = self.client().get('/movies?page=1000', headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_get_paginated_actors(self):
        res = self.client().get('/actors', headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_error_get_paginated_actors(self):
        res = self.client().get('/actors?page=1000', headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_movie(self):    
        res = self.client().delete('/movies/3', headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 3).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_error_delete_movie(self):    
        res = self.client().delete('/movies/5000', headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_delete_actor(self):    
        res = self.client().delete('/actors/3', headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 3).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
        self.assertEqual(actor, None)

    def test_error_delete_actor(self):    
        res = self.client().delete('/actors/5000', headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
    
    def test_create_movie(self):
        res = self.client().post('/movies', json={'title': 'Dr. Strange', 'release_date': '10-20-2016'}, headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))

    def test_error_create_movie(self):
        res = self.client().post('/movies/100', json={'title': 'A Horrible Year', 'release_date': '01-01-2020'}, headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_create_actor(self):
        res = self.client().post('/actors', json={'name': 'Rachel McAdams', 'age': 41, 'gender': 'Female'}, headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actors']))

    def test_error_create_actor(self):
        res = self.client().post('/actors/100', json={'name': 'Dorris Bob', 'age': 11, 'gender': 'Male'}, headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_update_movie(self):
        res = self.client().patch('/movies/5', json={'release_date': '11-11-2015'}, headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_error_update_movie(self):
        res = self.client().patch('/movies/1000', json={'release_date': '11-11-2015'}, headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')  

    def test_update_actor(self):    
        res = self.client().patch('/actors/5', json={'age': 50}, headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_error_update_actor(self):
        res = self.client().patch('/actors/1000', json={'age': 50}, headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')  

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()