import json

from flask import Flask, jsonify
from utils import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/movie/<title>')
def get_by_movie_title(title):
    return get_by_title(title)

@app.route('/movie/year/to/year')
def get_movie_by_years(year1: int, year2: int):
    return jsonify(get_by_ages(year1, year2))

@app.route('/rating/<category>')
def get_by_movie_rating(category):
    return jsonify(movies_by_rating(category))

@app.route('/genre/<genre>')
def get_top_movies_by_genre(genre):
    return jsonify(get_top_by_genre(genre))

if __name__ == "__main__":
    app.run(debug=True)