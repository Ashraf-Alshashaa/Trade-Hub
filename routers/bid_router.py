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
