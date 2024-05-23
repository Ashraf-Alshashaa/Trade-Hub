from . import *


def insert_bid(session, bid):
    session.add(DbBid(
                date=bid['date'],
                status=bid['status'],
                product_id=bid['product_id'],
                price=bid['price'],
                bidder_id=bid['bidder_id']
            ))
    session.commit()