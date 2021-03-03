from flask import Flask, render_template
from flask_json import FlaskJSON, JsonError, json_response, as_json
import os
import sys

from config import APP_CONFIG

app = Flask(__name__)
FlaskJSON(app)

#index page 
@app.route('/')
def index():
    return json_response(APP_CONFIG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8282)
