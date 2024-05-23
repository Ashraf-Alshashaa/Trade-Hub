from . import *
from db import db_product
from schemas.product import ProductDisplay, ProductBase
from schemas.product import StateEnum
from sqlalchemy.sql.sqltypes import List

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


@router.delete('/delete/{id}', response_model=ProductDisplay)
def delete_product(id: int, db: Session = Depends(get_db)):
    return db_product.delete_product(db, id)


@router.get('/{seller_id}/my_selling', response_model=List[ProductDisplay])
def get_products_by_seller(
        seller_id: int,
        db: Session = Depends(get_db)
):
    return db_product.get_products_by_seller(db, seller_id)


@router.get('/{seller_id}/my_selling/state', response_model=List[ProductDisplay])
def get_products_by_seller_and_state(
        seller_id: int,
        state: StateEnum = Query(...),
        db: Session = Depends(get_db)
):
    return db_product.get_products_by_seller_and_state(db, seller_id, state)


@router.get('/{user_id}/my_buying/bought_before', response_model=List[ProductDisplay])
def get_products_bought_by_user(user_id: int, db: Session = Depends(get_db)):
    return db_product.get_products_bought_by_user(db, user_id)


@router.get('/{user_id}/my_buying/my_biddings', response_model=List[ProductDisplay])
def get_products_user_is_bidding_on(user_id: int, db: Session = Depends(get_db)):
    return db_product.get_products_user_is_bidding_on(db, user_id)
