from . import *
from schemas.bid import BidBase
from db.models import DbBid

def add_bid(db: Session, request: BidBase):
    new_bid = DbBid(
        product_id = request.product_id,
        price = request.price,
        bidder_id = request.bidder_id
    )
    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)
    return new_bid