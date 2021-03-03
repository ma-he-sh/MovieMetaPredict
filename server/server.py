from flask import Flask
import os
import sys

app = Flask(__name__)

#index page 
@app.route('/')
def index():
    return 'test'

#404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8282)
