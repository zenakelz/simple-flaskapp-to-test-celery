from celery import Celery
import sqlalchemy
import celeryconfig

app = Celery('tasks', broker='redis://localhost:6379/0')
app.config_from_object(celeryconfig)

CELERY_DEFAULT_RETRY_DELAY = 5
CELERY_DEFAULT_AUTO_RETRY_MAX = 8
CELERY_RETRY_CONFIG = {
    'STALE_DATA_ERROR': {
        'retry_delay': 3,
        'max_retries': 5
    },
    'POINTS_INTEGRITY_EXCEPTION': {
        'retry_delay': 3,
        'max_retries': 1
    },
    'POINTS_REPEATABLE_READ_EXCEPTION': {
        'retry_delay': 0,
        'max_retries': 5
    }
}

@app.task
def send_message(message):
    print(message)


# @app.task(bind=True)  # The bind argument to the task decorator will give access to self (the task type instance).

@app.task(
    bind=True,
    autoretry_for=(
        sqlalchemy.exc.InternalError,
    ),
    retry_kwargs={
        'max_retries': CELERY_DEFAULT_AUTO_RETRY_MAX
    },
    default_retry_delay=CELERY_DEFAULT_RETRY_DELAY,
)
def send_message_with_retry(self, message):
    try:
        print(message)
        raise ValueError("Force retry")
    except ValueError as e:
        print(f"Retry count: {send_message_with_retry.request.retries}; Max retries set at: {send_message_with_retry.max_retries}")
        print(f"POINTS retry_delay: {CELERY_RETRY_CONFIG['POINTS_REPEATABLE_READ_EXCEPTION']['retry_delay']}; max_retries: {CELERY_RETRY_CONFIG['POINTS_REPEATABLE_READ_EXCEPTION']['max_retries']}")
        # At this point the max_retries can be updated
        raise self.retry(
            countdown=CELERY_RETRY_CONFIG['POINTS_REPEATABLE_READ_EXCEPTION']['retry_delay'],
            exc=e,
            max_retries=CELERY_RETRY_CONFIG['POINTS_REPEATABLE_READ_EXCEPTION']['max_retries']
        )
