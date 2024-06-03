from . import *

FROM_TRADEHUB = "tradehub@mail.com"


class NotificationType(Enum):
    IN_APP = "in_app"
    EMAIL = "email"


class EmailNotification:

    def __init__(self, server='localhost', port=1025):
        self.server = server
        self.port = port

    def send(self, **kwargs):
        recipient = kwargs.get("recipient")
        subject = kwargs.get("subject")
        body = kwargs.get("body")
        message = f"Subject: '{subject}'\n\n{body}"
        with smtplib.SMTP(self.server, self.port) as server:
            server.sendmail(FROM_TRADEHUB, recipient, message)

        print(f"sending an email from TradeHub to {recipient}")
        print(message)


class InAppNotification:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send(self, **kwargs):
        recipient = kwargs.get("recipient")
        message = kwargs.get("message")
        for connection in self.active_connections:
            await connection.send_text(message)
            print(f"sending an a notification to {recipient}")
            print(message)


class NotificationCenter:
    def __init__(self):
        self.email = EmailNotification()
        self.in_app = InAppNotification()
        self.websocket: WebSocket

    async def notify_user(self, type: NotificationType, **kwargs):
        if type == NotificationType.EMAIL:
            self.email.send(**kwargs)
        elif type == NotificationType.IN_APP:
            await self.in_app.send(**kwargs)

