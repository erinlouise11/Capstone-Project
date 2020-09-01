import os
import dateutil.parser
import babel
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from .auth.auth import AuthError, requires_auth

DETAILS_PER_PAGE = 10

# paginating either the movies or actors
def pagination(request, selection, type):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * DETAILS_PER_PAGE
  end = start + DETAILS_PER_PAGE

  if(type == 'movies'):
    movies = [movie.format() for movie in selection]
    return movies[start:end]
  elif(type == 'actors'):
    actors = [actor.format() for actor in selection]
    return actors[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # initializing CORS to enable cross-domain requests
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # setting response headers
  @app.after_request
  def after_request(response):
    response.headers.add('Acess-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Acess-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  
  # endpoints
  @app.route('/')
  def handler():
    return jsonify({
        "success": True
    })

  # display all the movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies():
    movies = Movie.query.order_by(Movie.title).all()
    current_movies = pagination(request, movies, 'movies')

    if(len(current_movies) == 0):
      abort(404)
    
    return jsonify({
      'success': True, 
      'movies': current_movies,
      'total_movies': len(movies)
    }), 200

  # display all the actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors():
    actors = Actor.query.order_by(Actor.name).all()
    current_actors = pagination(request, actors, 'actors')

    if(len(current_actors) == 0):
      abort(404)

    return jsonify({
      'success': True, 
      'actors': current_actors, 
      'total_actors': len(actors)
    }), 200
  
  # display a specific movie
  @app.route('/movies/<int:movie_id>', methods=['GET'])
  @requires_auth('get:movies')
  def get_specific_movie(movie_id):
    specific_movie = Movie.query.filter_by(id=movie_id).one_or_none()    

    if(specific_movie is None):
      abort(404)  
    
    return jsonify({
      'success': True, 
      'movie': specific_movie.format()
    }), 200

  # display a specific actor
  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth('get:actors')
  def get_specific_actor(actor_id):
    specific_actor = Actor.query.filter_by(id=actor_id).one_or_none()

    if(specific_actor is None):
      abort(404)
    
    return jsonify({
      'success': True, 
      'actor': specific_actor.format()
    }), 200

  # delete a movie
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(movie_id):
    try:
      movie = Movie.query.filter_by(id=movie_id).one_or_none()

      if(movie is None):
        abort(404)

      movie.delete()
      movies = Movie.query.order_by(Movie.id).all()
      current_movies = pagination(request, movies, 'movies')

      return jsonify({
        'success': True, 
        'deleted': movie_id, 
        'movies': current_movies,
        'total_movies': len(movies)
      }), 200     

    except:
      abort(422)    

  # delete an actor
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(actor_id):
    try:
      actor = Actor.query.filter_by(id=actor_id).one_or_none()

      if(actor is None):
        abort(404)

      actor.delete()
      actors = Actor.query.order_by(Actor.id).all()
      current_actors = pagination(request, actors, 'actors')

      return jsonify({
        'success': True, 
        'deleted': actor_id, 
        'actors': current_actors, 
        'total_actors': len(actors)
      }), 200     

    except:
      abort(422) 

  # create a movie
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie():
    # getting the json body and splitting the elemtents
    body = request.get_json()

    new_title = body.get('title')
    new_release_date = body.get('release_date')

    if not('title' in body and 'release_date' in body):
      abort(400)

    movie = Movie(title=new_title, release_date=new_release_date)
    movie.insert()

    movies = Movie.query.order_by(Movie.id).all()
    current_movies = pagination(request, movies, 'movies')

    return jsonify({
      'success': True,
      'created': movie.id, 
      'movies': current_movies,
      'total_movies': len(movies)
    }), 200

  # create an actor
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor():
    # getting the json body and splitting the elemtents
    body = request.get_json()

    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')

    if not('name' in body and 'age' in body and 'gender' in body):
      abort(400)

    actor = Actor(name=new_name, age=new_age, gender=new_gender)
    actor.insert()

    actors = Actor.query.order_by(Actor.id).all()
    current_actors = pagination(request, actors, 'actors')

    return jsonify({
      'success': True,
      'created': actor.id, 
      'actors': current_actors, 
      'total_actors': len(actors)
    }), 200

  # update a movie
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(movie_id):
    specific_movie = Movie.query.filter_by(id=movie_id).one_or_none()

    if(specific_movie is None):
      abort(404)

    body = request.get_json()

    try:
      if('title' in body):
        specific_movie.title = body['title']
      if('release_date' in body):
        specific_movie.release_date = body['release_date']
    except:
      abort(400)    

    specific_movie.update()

    return jsonify({
      'success': True, 
      'movie': specific_movie.format()
    }), 200

  # update an actor
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(actor_id):
    specific_actor = Actor.query.filter_by(id=actor_id).one_or_none()

    if(specific_actor is None):
      abort(404)

    body = request.get_json()

    try:
      if('name' in body):
        specific_actor.name = body['name']
      if('age' in body):
        specific_actor.age = body['age']
      if('gender' in body):
        specific_actor.gender = body['gender']
    except:
      abort(400)    

    specific_actor.update()

    return jsonify({
      'success': True, 
      'actor': specific_actor.format()
    }), 200

  # error handlers (AuthError, 400, 404, 405, 422, 500)
  @app.errorhandler(AuthError)
  def authentication_eror(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code

  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': "Bad request"
    }), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "Not found"
    }), 404
  
  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': "Method not allowed"
    }), 405  

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Unprocessable"
    }), 422

  @app.errorhandler(500)
  def internal(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': "Internal server error"
    }), 500  

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)