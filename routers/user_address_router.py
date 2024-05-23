from . import *
from schemas.user_address import AddressPublicDisplay, AddressPrivateDisplay, AddressBase
from db import db_user_address
from typing import List

router = APIRouter(
    prefix='/address',
    tags=['address']
)


@router.post('/add', response_model=AddressPrivateDisplay)
def add_address(request: AddressBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user_address.add_address(db, request)


@router.get('/my_addresses', response_model=List[AddressPrivateDisplay])
def my_addresses(id: int = Query(..., alias='user_id'), db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user_address.get_address(db, id)


@router.get('', response_model=AddressPublicDisplay)
def show_address_publicly(id: int, db: Session = Depends(get_db)):
    return db_user_address.get_address(db, id)


@router.put('/modify/{id}')
def modify_address(id: int, request: AddressBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user_address.modify_address(db, id, request)


@router.delete('/delete/{id}')
def delete_address(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user_address.delete_address(db, id)
