from . import *
from schemas.user_address import AddressPublicDisplay, AddressPrivateDisplay, AddressBase
from db import db_user_address
from typing import List

router = APIRouter(
    prefix='/address',
    tags=['address']
)


@router.post('/add', response_model=AddressPrivateDisplay)
def add_address(request: AddressBase, db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    request.user_id = current_user.id
    return db_user_address.add_address(db, request, current_user.id)


@router.get('/my-addresses', response_model=List[AddressPrivateDisplay])
def my_addresses(id: int = Query(..., alias='user_id'),
                 db: Session = Depends(get_db),
                 current_user: UserBase = Depends(get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to see this address!")
    return db_user_address.my_addresses(db, id)


@router.get('/{id}')
def get_address_privately(id: int, db: Session = Depends(get_db),
                          current_user: UserBase = Depends(get_current_user)):
    return db_user_address.get_address(db, id)


@router.get('/', response_model=AddressPrivateDisplay)
def my_address(db: Session = Depends(get_db),
               current_user: UserBase = Depends(get_current_user)):
    address = db_user_address.get_default_address(db, current_user.id)
    if current_user.id != address.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to see this address!")
    return db_user_address.get_default_address(db, current_user.id)


@router.put('/modify/{id}', response_model=AddressPrivateDisplay)
def modify_address(request: AddressBase, id: int,
                   db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    address = db_user_address.get_address(db, id)
    if current_user.id != address.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this address!")
    return db_user_address.modify_address(db, id, request)


@router.put('/default/{id}')
def my_default_address(id: int,
                       db: Session = Depends(get_db),
                       current_user: UserBase = Depends(get_current_user)):
    address = db_user_address.get_address(db, id)
    if current_user.id != address.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this address!")
    return db_user_address.set_default_address(db, id, current_user.id)


@router.delete('/delete/{id}')
def delete_address(id: int,
                   db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    address = db_user_address.get_address(db, id)
    if current_user.id != address.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this address!")
    return db_user_address.delete_address(db, id)
