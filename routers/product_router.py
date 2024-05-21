from . import *
from db import db_product
from schemas.product import ProductDisplay

router = APIRouter(prefix='/product', tags=['product'])


@router.get('/{id}', response_model=ProductDisplay)
def get_product(id: int, db: Session = Depends(get_db)):
    return db_product.get_product(db, id)


@router.post('/add', response_model=ProductDisplay)
def add_item(request: ProductBase, db: Session = Depends(get_db)):
    return db_product.add_item(db, request)


@router.put('/modify/{id}', response_model=ProductDisplay)
def modify_item(id: int, request: ProductBase, db: Session = Depends(get_db)):
    return db_product.modify_item(db, id, request)