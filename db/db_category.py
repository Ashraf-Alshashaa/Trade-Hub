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