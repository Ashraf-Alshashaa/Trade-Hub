from . import *
from db import db_product
from schemas.product import ProductDisplay, ProductBase


router = APIRouter(prefix='/product', tags=['product'])


@router.post('/add', response_model=ProductDisplay)
def add_product(request: ProductBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_product.add_product(db, request)


@router.get('/{id}', response_model=ProductDisplay)
def get_product(id: int, db: Session = Depends(get_db)):
    return db_product.get_product(db, id)


@router.put('/modify/{id}', response_model=ProductDisplay)
def modify_product(id: int, request: ProductBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_product.modify_product(db, id, request)


@router.delete('/delete/{id}')
def delete_product(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_product.delete_product(db, id)

