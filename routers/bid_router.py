from . import *
from schemas.bid import BidDisplay, BidBase
from db import db_bid
from typing import List


router = APIRouter(prefix='/bid', tags=['bid'])


@router.post('/add', response_model= BidDisplay)
def add_bid(request: BidBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_bid.add_bid(db, request)

  
@router.delete('/delete/{id}')
def delete_bid( id: int, db: Session =  Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_bid.delete_bid(db, id)

  
@router.get('/product_bids', response_model=List[BidDisplay])
def get_all_bids(id: int = Query(..., alias='product_id'), db: Session = Depends(get_db)):
    return db_bid.get_all_bids(db, id)

  
@router.put('/status', response_model=BidDisplay)
def change_bid_status(request: BidBase, bid_id: int,db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_bid.change_bidding_status(db, bid_id, request)
