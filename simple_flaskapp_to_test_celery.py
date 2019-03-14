# This is a simple app created with the purpose of Testing Celery retry methods
# http://flask.pocoo.org/docs/1.0/quickstart/
# Steps to Run 1) export FLASK_APP=simple_flaskapp_to_test_celery.py
#			   2) export FLASK_ENV=development
# 		       3) flask run

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'