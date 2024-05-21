from . import *
from db import db_product, db_bid
from schemas.product import ProductDisplay
from schemas.bid import BidDisplay
from typing import List

router = APIRouter(prefix='/product', tags=['product'])


@router.get('/{id}', response_model=ProductDisplay)
def get_product(id: int, db: Session = Depends(get_db)):
    return db_product.get_product(db, id)


@router.post('/add', response_model=ProductDisplay)
def add_product(request: ProductBase, db: Session = Depends(get_db)):
    return db_product.add_product(db, request)


@router.put('/modify/{id}', response_model=ProductDisplay)
def modify_product(id: int, request: ProductBase, db: Session = Depends(get_db)):
    return db_product.modify_product(db, id, request)


@router.get('/{id}/bids', response_model=List[BidDisplay])
def get_all_bids(id: int, db: Session = Depends(get_db)):
    return db_bid.get_all_bids(db, id)