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
        colour_print('params', f"name: {send_message_with_retry.name}")
        colour_print('params', f"request: {send_message_with_retry.request}")
        colour_print('params', f"max_retries: {send_message_with_retry.max_retries}")
        colour_print('params', f"throws: {send_message_with_retry.throws}")
        colour_print('params', f"Default retry delay: {send_message_with_retry.default_retry_delay}")
        colour_print('params', f"Rate limit: {send_message_with_retry.rate_limit}")
        colour_print('params', f"Time limit: {send_message_with_retry.time_limit}")
        colour_print('params', f"Soft time limit: {send_message_with_retry.soft_time_limit}")
        colour_print('params', f"Ignore result: {send_message_with_retry.ignore_result}")
        colour_print('params', f"store_errors_even_if_ignored: {send_message_with_retry.store_errors_even_if_ignored}")
        colour_print('params', f"serializer: {send_message_with_retry.serializer}")
        colour_print('params', f"backend: {send_message_with_retry.backend}")
        colour_print('params', f"acks_late: {send_message_with_retry.acks_late}")
        colour_print('params', f"track_started: {send_message_with_retry.track_started}")

        # At this point the max_retries can be updated
        raise self.retry(
            countdown=CELERY_RETRY_CONFIG['POINTS_REPEATABLE_READ_EXCEPTION']['retry_delay'],
            exc=e,
            max_retries=CELERY_RETRY_CONFIG['POINTS_REPEATABLE_READ_EXCEPTION']['max_retries']
        )


def colour_print(style, message):
    if style is 'info':
        print(f'\033[1;35;40m {message}\033[1;37;40m')
    elif style is 'error':
        print(f'\033[1;31;40m {message}\033[1;37;40m')
    elif style is 'params':
        print(f'\033[1;34;40m {message}\033[1;37;40m')

