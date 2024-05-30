class EmailNotification:
    def send(self, recipient: str, message: str):
        print(f"sending an email from TradeHub to {recipient}")
        print(message)

class InAppNotification:
    def send(self,recipient: str):
        print(f"sending an inAppNotification to{recipient}")


class NotificationCenter:
    def __init__(self):
        self.email = EmailNotification()
        self.in_app = InAppNotification()

    def notify_user(self, recipient: str, message: str, urgent: bool):
        if urgent:
            self.email.send(recipient, message)
        else:
            self.in_app.send(recipient)

