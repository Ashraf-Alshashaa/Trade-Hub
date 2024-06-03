from . import *
from db.models import DbUser
from schemas.users import UserBase, UserDisplay
from auth.hash import Hash
from db.db_user_address import is_first_address
from db.models import DbAddress
from schemas.user_address import AddressPrivateDisplay


def register_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="This username is already registered")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))
    
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    return user


def get_user_by_id(db: Session, id: int):
    db_user = db.query(DbUser).filter(DbUser.id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User not found')
    address = db.query(DbAddress).filter(DbAddress.default, DbAddress.user_id == db_user.id).first()
    if is_first_address(db, id):
        db_address = db.query(DbAddress).filter(DbAddress.default).first()
        if not db_address:
            address = None

# Convert address to AddressPrivateDisplay if address is not None
    address_display = AddressPrivateDisplay.from_orm(address) if address else None

    user = UserDisplay(
        username=db_user.username,
        email=db_user.email,
        address=address_display
    )
    return user


def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    # handle any exceptions
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return user.first()

  
def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    # handle any exceptions
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    db.delete(user)
    db.commit()
    return 'ok'
