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


@router.get('/')
def get_user(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    id = current_user.id
    return db_user.get_user_by_id(db, id)


@router.put('/{id}/update', response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Ensure that the current user is updating their own account
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

    return db_user.update_user(db, id, request)


@router.delete('/delete/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Ensure that the current user is deleting their own account
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")

    return db_user.delete_user(db, id)
