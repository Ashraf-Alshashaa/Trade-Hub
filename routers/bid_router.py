from . import *
from schemas.bid import BidDisplay, BidBase
from db import db_bid
from typing import List


router = APIRouter(prefix='/bid', tags=['bid'])


@router.post('/add', response_model= BidDisplay)
def add_bid(request: BidBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Set the bidder_id to the current user's id
    request.bidder_id = current_user.id
    return db_bid.add_bid(db, request)


@router.get('/product_bids', response_model=List[BidDisplay])
def get_all_bids(id: int = Query(..., alias='product_id'), db: Session = Depends(get_db)):
    return db_bid.get_all_bids(db, id)


@router.get('/{id}', response_model=BidDisplay)
def get_bid(id: int, db: Session = Depends(get_db)):
    return db_bid.get_bid(db, id)


@router.put('/status', response_model=BidDisplay)
def change_bid_status(request: BidBase, bid_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Fetch the bid to verify authorization
    bid = db_bid.get_bid(db, bid_id)
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found")

    # Check if the current user is the bidder
    if bid.bidder_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to change the status of this bid")

    return db_bid.change_bidding_status(db, bid_id, request)


@router.delete('/delete/{id}')
def delete_bid(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Fetch the bid to verify authorization
    bid = db_bid.get_bid(db, id)
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found")

    # Check if the current user is the bidder
    if bid.bidder_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this bid")

    return db_bid.delete_bid(db, id)
