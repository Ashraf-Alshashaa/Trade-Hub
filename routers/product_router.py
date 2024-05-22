from . import *
from db import db_product
from schemas.product import ProductDisplay


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

