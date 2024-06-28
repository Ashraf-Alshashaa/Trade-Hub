from . import *
from schemas.users import UserBase, UserDisplay, UserUpdateDisplay, UserPublicDisplay
from db import db_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('', response_model=UserUpdateDisplay)
def register_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.register_user(db, request)


@router.get('', response_model= UserPublicDisplay)
def get_user_publicly(id: int, db: Session= Depends(get_db)):
    try:
        return db_user.get_user_by_id(db,id)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user does not exist.")

@router.get('/{id}',response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to see this user")
    return db_user.get_user_by_id(db, id)



@router.put('/{id}', response_model=UserUpdateDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Ensure that the current user is updating their own account
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

    return db_user.update_user(db, id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Ensure that the current user is deleting their own account
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")

    return db_user.delete_user(db, id)
