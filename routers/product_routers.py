from . import *

router = APIRouter(prefix='/product', tags=['product'])


@router.post('/add', response_model=ProductDisplay)
def add_item(request: ProductBase, db: Session = Depends(get_db)):
    return db_product.add_item(db, request)


@router.put('/modify/{id}', response_model=ProductDisplay)
def modify_item(id: int, request: ProductBase, db: Session = Depends(get_db)):
    return db_product.modify_item(db, id, request)