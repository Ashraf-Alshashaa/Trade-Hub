from . import *
from schemas.bid import BidBase
from db.models import DbBid

def add_bid(db: Session, request: BidBase):
    new_bid = DbBid(
        product_id=request.product_id,
        price=request.price,
        bidder_id=request.bidder_id
    )
    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)
    return new_bid

def get_all_bids(db: Session, id: int):
    return db.query(DbBid).filter(DbBid.product_id == id).all()