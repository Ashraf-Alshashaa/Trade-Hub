from . import *
from schemas.user_address import AddressPublicDisplay, AddressPrivateDisplay, AddressBase
from db import db_address
from typing import List

router = APIRouter(
    prefix='/address',
    tags=['address']
)


@router.post('/add', response_model=AddressPrivateDisplay)
def add_address(request: AddressBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_address.add_address(db, request)


@router.get('/my_addresses', response_model=List[AddressPrivateDisplay])
def my_addresses(id: int = Query(..., alias='user_id'), db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_address.get_address(db, id)


@router.get('', response_model=AddressPublicDisplay)
def show_address_publicly(id: int, db: Session = Depends(get_db)):
    return db_address.get_address(db, id)


@router.put('/modify/{id}', response_model=AddressPrivateDisplay)
def modify_product(id: int, request: AddressBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_address.modify_address(db, id, request)


@router.delete('/delete/{id}')
def delete_product(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_address.delete_address(db, id)
