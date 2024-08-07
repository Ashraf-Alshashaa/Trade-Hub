from . import *
import json

FROM_TRADEHUB = "tradehub@mail.com"


class NotificationType(Enum):
    IN_APP = "in_app"
    EMAIL = "email"


class EmailNotification:

    def __init__(self, server='localhost', port=1025):
        self.server = server
        self.port = port

    async def send(self, **kwargs):
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
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        print(f"new websocket added to notify user_ID {user_id}")
        print(f"connections[{user_id}]: {websocket}")
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections.keys():
            del self.active_connections[user_id]

    async def send(self, **kwargs):
        recipient = int(kwargs.get("recipient"))
        product_id = int(kwargs.get("product_id"))
        message = kwargs.get("message")

        data = {
            "userId" : recipient,
            "productId" : product_id,
            "message" : message,
        }

        message_json = json.dumps(data)

        if recipient in self.active_connections.keys():
            await self.active_connections[recipient].send_text(message_json)
            print(f"sending an a notification to {recipient}")
            print(message)

    async def broadcast(self, **kwargs):
        recipient = kwargs.get("recipient")
        product_id = int(kwargs.get("product_id"))
        message = kwargs.get("message")

        for user in recipient:
            data = {
            "userId" : user,
            "productId" : product_id,
            "message" : message,
        }

            message_json = json.dumps(data)
            if user in self.active_connections.keys():
                await self.active_connections[user].send_text(message_json)
                print(f"sending an a notification to {user}")
                print(message)


class NotificationCenter:
    def __init__(self):
        self.email = EmailNotification()
        self.in_app = InAppNotification()
        self.websocket: WebSocket

    async def notify_user(self, type: NotificationType, **kwargs):
        if type == NotificationType.EMAIL:
            await self.email.send(**kwargs)
        elif type == NotificationType.IN_APP:
            await self.in_app.send(**kwargs)

