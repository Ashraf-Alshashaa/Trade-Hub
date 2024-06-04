from . import *
from schemas.category import CategoryDisplay, CategoryBase
from db import db_category
from typing import List
from schemas.users import UserRole


router = APIRouter(prefix='/categories', tags=['categories'])


@router.post('', response_model=CategoryDisplay)
def add_category(
    request: CategoryBase, 
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
    ):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're not authorized to add category")
    return db_category.add_category(db, request)


@router.get('', response_model=List[CategoryDisplay])
def get_categories(
        db: Session = Depends(get_db)
    ):
    return db_category.get_categories(db)


@router.get('/{id}', response_model=CategoryDisplay)
def get_categorie(
        category_id: int,
        db: Session = Depends(get_db)
    ):
    return db_category.get_category(db, category_id)


@router.put('/{id}', response_model=CategoryDisplay)
def update_category(
        request: CategoryBase, 
        id: int, 
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're not authorized to update category")
    return db_category.update_category(db, id, request)


@router.delete('/{id}')
def get_bid(
        id: int, 
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're not authorized to delete category")
    return db_category.delete_category(db, id)