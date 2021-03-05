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
    payload = {
        'title' : movietitle,
        'payload': {}
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
