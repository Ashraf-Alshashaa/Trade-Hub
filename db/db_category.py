from . import *
from schemas.category import CategoryBase
from db.models import DbCategory


def add_category(db: Session, request: CategoryBase):
    new_category = DbCategory(
        name=request.name,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_categories(db: Session): 
    return db.query(DbCategory).all()

def get_category(db: Session, id: int):
    category = db.query(DbCategory).filter(DbCategory.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'category with id {id} not found')
    return category


def update_category(db: Session, id: int, request: CategoryBase):
    category = db.query(DbCategory).filter(DbCategory.id == id)

    category.update({
        DbCategory.name: request.name
    })
    db.commit()
    category = category.first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'category with id {id} not found')
    return category


def delete_category(db: Session, id: int):
    category = db.query(DbCategory).filter(DbCategory.id == id).first()
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Category with id {id} not found')
    db.delete(category)
    db.commit()
    return 'ok'