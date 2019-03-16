from tasks import send_message_with_retry
import datetime

class Robot(object):
    def __init__(self, name, greeting):
        self.name = name
        self.greeting = greeting

    def speak(self):
        message = f"Hello, the time is {datetime.datetime.now()}"
        send_message_with_retry.apply_async(args=[message])
