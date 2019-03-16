## simple-flaskapp-to-test-celery

This is a simple app created with the purpose of testing the Celery "retry" method

#### Stratergy used

1) Create simple flask app

    http://flask.pocoo.org/docs/1.0/quickstart/

2) Integrate Celery

    http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps

#### How to start up app and workers

run web
```
$ FLASK_APP=simple_flaskapp_to_test_celery.py FLASK_ENV=development  flask run
```
run workers
```
$ celery -A tasks worker --loglevel=info
```
