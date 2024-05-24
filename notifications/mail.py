import aiosmtplib
from email.message import EmailMessage
import asyncio
from notification import Observer, Observable
from db import db_bid
from db.models import DbBid, DbProduct
from sqlalchemy.orm.session import Session

FROM_EMAIL = "well"
PASSWORD = 'txaztkcoseyaeuux'


class ProductBids(Observable):
    pass


class EmailNotifier(Observer):
    def __init__(self, stmp_config):
        self.stmp = stmp_config

    async def send_mail(self, to_email, subject, body):
        message = EmailMessage()
        message["From"] = self.stmp[FROM_EMAIL]
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(message,
                              hostname="smtp.gmail.com",
                              port=465,
                              use_tls=True,
                              username="ladan.rb@gmail.com",
                              password=PASSWORD)
    # Notify seller they have a new bid

    def get_seller_id(self, bid_id: int, db: Session):
        pass


    asyncio.run(send_mail(FROM_EMAIL, "testing", "SALAMALEKOM"))




