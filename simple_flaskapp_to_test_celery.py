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
from robot import Robot
from tasks import send_message

app = Flask(__name__)


@app.route('/')
def hello():
    send_message.delay("Hello")
    return jsonify({
        'Running Flask Application': 'simple_flaskapp_to_test_celery',
        'Message': 'Hello world!'})


@app.route('/activate_robot')
def activate_robot():
    robot = Robot("Ronney", "Hello")
    print("ROBOT ACTIVATED")
    robot.speak()
    return jsonify({
        'Running Flask Application': 'simple_flaskapp_to_test_celery',
        'Message': 'Robot will send a message: Hello and retry Hello 5 times'})
