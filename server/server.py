from flask import Flask, render_template
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS
import os
import sys

from modules.db import DB
from modules.redis import REDIS
from config import APP_CONFIG

dbconn = DB()
dbconn.create_table()

redisConn = REDIS()

app = Flask(__name__)
FlaskJSON(app)

# set cors to accept all
cors = CORS(app, resources={"/metaserver/api/*": {"origins": "*"}})

NAMESPACE='metaserver/api'

#ping
@app.route(f"/{NAMESPACE}/ping", methods=["POST", "GET"])
def index():
    payload = {
        'msg' : 'pong'
    }
    return json_response( callback=payload )

#get title
@app.route(f"/{NAMESPACE}/title/<movietitle>", methods=["GET"])
def get_title(movietitle):
    sample_payload = {
        "id": "tt0068646",
        "href": "https://imdb.com/title/tt0068646",
        "title": "The Godfather",
        "year": "1972",
        "meta": {
            "certificate": "18A",
            "runtime": "175 min",
            "genre": ["Crime", "Drama"],
            "meta_score": "100",
            "description": "An organized crime ...",
            "directors": [
                "Francis Ford Coppola"
            ],
            "votes": "1,628,276",
            "gross": "$134.97M",
            "awards": {
                "Actors": "5 Stars",
                "Direction": "5 Stars",
                "Screenplay": "5 Stars",
                "Oscars": "3",
                "Oscar Nominations": "11",
                "BAFTA Awards": "0",
                "BAFTA Nominations": "4",
                "Golden Globes": "6",
                "Golden Globe Nominations": "8"
            },
            "cast": [
                {
                    "actor": "Marlon Brando",
                    "actor_link": "/name/nm0000008/",
                    "character": "Don Vito Corleone",
                    "character_link": "/title/tt0068646/characters/nm0000008"
                },
                ...
            ],
            "Country:": ["USA"],
            "Language:": ["English","Italian","Latin"],
            "Release Date:": "24 March 1972 (Canada)",
            "Also Known As:": "Le parrain",
            "Filming Locations:": [
                "NY Eye and Ear Infirmary, 2nd Avenue & East 13th Street, New York City, New York, USA"
            ],
            "Budget:": "$6,000,000            (estimated)",
            "Opening Weekend USA:": "$302,393,19 March 1972",
            "Gross USA:": "$134,966,411",
            "Cumulative Worldwide Gross:": "$246,120,986",
            "Production Co:": ["Paramount Pictures", "Alfran Productions"],
            "Runtime:": "175 min",
            "Sound Mix:": ["DTS", "Mono"],
            "Color:": ["Color"],
            "Aspect Ratio:": "1.85 : 1",
            "storyline": "The Godfather ....",
            "rating": "18A"
        }
    }
    
    payload = {
        'title' : movietitle,
        'payload': sample_payload,
    }
    return json_response( callback=payload )


@app.errorhandler(400)
def page_not_found(e):
    payload = {
        'success' : False,
        'error'   : 'Page Not Found',
    }
    return json_response( resp=payload )

if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0', port=8282, threaded=True )
