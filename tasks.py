from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def send_message(message):
    print(message)


@app.task(bind=True)  # The bind argument to the task decorator will give access to self (the task type instance).
def send_message_with_retry(self, message):
    try:
        print(message)
        raise ValueError("Force retry")
    except ValueError as e:
        print(f"Retry count: {send_message_with_retry.request.retries}; Max retries set at: {send_message_with_retry.max_retries}")
        # At this point the max_retries can be updated
        raise self.retry(
            countdown=1,
            exc=e,
            max_retries=5
        )
