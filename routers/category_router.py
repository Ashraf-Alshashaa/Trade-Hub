from . import *
from schemas.category import CategoryDisplay, CategoryBase
from db import db_category
from typing import List, Optional


router = APIRouter(prefix='/categories', tags=['categories'])


@router.post('', response_model=CategoryDisplay)
def add_category(request: CategoryBase, db: Session = Depends(get_db)):
    return db_category.add_category(db, request)


@router.get('', response_model=List[CategoryDisplay])
def get_categories(
        category_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    return db_category.get_category(db, category_id)


@router.put('/{id}', response_model=CategoryDisplay)
def update_category(request: CategoryBase, id: int, db: Session = Depends(get_db)):
    return db_category.update_category(db, id, request)


@router.delete('/{id}')
def get_bid(id: int, db: Session = Depends(get_db)):
    return db_category.delete_category(db, id)