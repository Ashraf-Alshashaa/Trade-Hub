from . import *
from schemas.bid import BidDisplay, BidBase
from db import db_bid

router = APIRouter(prefix='/bid', tags=['bid'])

@router.post('/add', response_model= BidDisplay)
def add_bid(request: BidBase, db: Session = Depends(get_db)):
    return db_bid.add_bid(db, request)