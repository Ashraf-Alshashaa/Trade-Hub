from . import *


class NotificationType(Enum):
    IN_APP = "in_app"
    EMAIL = "email"


class EmailNotification:
    def send(self, recipient: int, message: str):
        print(f"sending an email from TradeHub to {recipient}")
        print(message)


class InAppNotification:
    def send(self,recipient: int, message: str):
        print(f"sending an a notification to {recipient}")
        print(message)


class NotificationCenter:
    def __init__(self):
        self.email = EmailNotification()
        self.in_app = InAppNotification()

    def notify_user(self, recipient: int, message: str, type: NotificationType):
        if type == NotificationType.EMAIL:
            self.email.send(recipient, message)
        elif type == NotificationType.IN_APP:
            self.in_app.send(recipient, message)

