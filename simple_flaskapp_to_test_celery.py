"""
This is a simple app created with the purpose of Testing the Celery "retry" method

Create simple flask app
http://flask.pocoo.org/docs/1.0/quickstart/

Integrate Celery
http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps

How to start up app and workers:

# run web
$ FLASK_APP=simple_flaskapp_to_test_celery.py FLASK_ENV=development  flask run

# run workers
$ celery -A tasks worker --loglevel=info

"""

from flask import Flask
from flask import jsonify
from tasks import add

app = Flask(__name__)

@app.route('/')
def hello_world():
    add.delay(4, 4)
    return jsonify({
        'Running Flask Application': 'simple_flaskapp_to_test_celery',
        'Message': 'Hello world!'})
