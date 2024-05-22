from . import *
from schemas.users import UserBase, UserDisplay
from db import db_user
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('', response_model=UserDisplay)
def register_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.register_user(db, request)


@router.delete('/delete/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)
