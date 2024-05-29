from . import *
from schemas.bid import BidDisplay, BidBase
from db.models import DbBid, DbProduct
from db import db_bid
from typing import List, Optional


router = APIRouter(prefix='/bids', tags=['bids'])


@router.post('', response_model=BidDisplay)
def add_bid(request: BidBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Set the bidder_id to the current user's id
    request.bidder_id = current_user.id
    return db_bid.add_bid(db, request)


@router.get('', response_model=List[BidDisplay])
def get_all_bids(
        product_id: int = Query(...),
        db: Session = Depends(get_db)
):
    return db_bid.get_all_bids(db, product_id)


@router.get('/{id}', response_model=BidDisplay)
def get_bid(id: int, db: Session = Depends(get_db)):
    return db_bid.get_bid(db, id)


@router.put('/{id}', response_model=BidDisplay)
def choose_won_bidding(
        request: BidBase,
        id: int, db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    # Fetch the bid to verify authorization
    bid = db_bid.get_bid(db, id)
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found")

    product_id = db.query(DbBid).filter(DbBid.id == id).first().product_id
    seller_id = db.query(DbProduct).filter(DbProduct.id == product_id).first().seller_id

    # Check if the current user is the seller
    if seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to change the status of this bid")

    return db_bid.choose_won_bidding(db, id, request)


@router.delete('/{id}')
def remove_product_from_cart(
        id: int,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),
        user_id: Optional[int] = None
):
    if user_id != None:
        if user_id != current_user.id:  # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're only authorized to list bought products of your own")
    return db_bid.remove_product_from_cart(db, id, user_id)
