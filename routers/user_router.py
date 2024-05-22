from . import *
from schemas.users import UserBase, UserDisplay
from db import db_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('', response_model=UserDisplay)
def register_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.register_user(db, request)

@router.put('/{id}/update')
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return db_user.update_user(db, id, request)