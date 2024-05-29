from . import *
from schemas.bid import BidBase, BidStatus
from db.models import DbBid, DbProduct
from schemas.product import StateEnum



def add_bid(db: Session, request: BidBase):
    new_bid = DbBid(
        status=request.status,
        date=request.date,
        product_id=request.product_id,
        price=request.price,
        bidder_id=request.bidder_id
    )
    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)
    return new_bid


def get_bid(db: Session, id: int):
    return db.query(DbBid).filter(DbBid.id == id).first()


def get_all_bids(db: Session, id: int):
    return db.query(DbBid).filter(DbBid.product_id == id).all()


def delete_bid(db: Session, id: int):
    bid = db.query(DbBid).filter(DbBid.id == id).first()
    # handle any exceptions
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Bid with id {id} not found')
    db.delete(bid)
    db.commit()
    return 'ok'

  
def choose_won_bidding(db: Session, id: int, request: BidBase):

    bid = db.query(DbBid).filter(DbBid.id == id).first()
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found")

    bid.status = request.status
    # Retrieve the associated product using the product_id from the bid
    product = db.query(DbProduct).filter(DbProduct.id == bid.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product state to PENDING
    product.state = StateEnum.PENDING
    product.price = bid.price

    # Commit the changes to the database
    db.commit()

    return bid

def remove_product_from_cart(db: Session, product_id: int, user_id: int):
    bid = db.query(DbBid).filter(
        DbBid.product_id == product_id,
        DbBid.bidder_id == user_id,
        DbBid.status == BidStatus.ACCEPTED
    ).first()

    if not bid:
        raise status.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    product = db.query(DbProduct).filter(DbProduct.id == product_id)
    product.update({DbProduct.state : StateEnum.AVAILABLE})

    bids_to_delete = db.query(DbBid).filter(
        DbBid.product_id == product_id,
        DbBid.bidder_id == user_id
    ).all()

    for b in bids_to_delete:
        delete_bid(db, b.id)
        db.commit()
    return 'Item removed from the cart'
