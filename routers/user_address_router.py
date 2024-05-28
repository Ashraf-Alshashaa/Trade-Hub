from . import *
from schemas.user_address import AddressPrivateDisplay, AddressBase
from db import db_user_address
from typing import List, Optional

router = APIRouter(
    prefix='/addresses',
    tags=['addresses']
)


@router.post('', response_model=AddressPrivateDisplay)
def add_address(request: AddressBase, db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    request.user_id = current_user.id
    return db_user_address.add_address(db, request, current_user.id)


@router.get('', response_model=List[AddressPrivateDisplay])
def all_my_addresses(db: Session = Depends(get_db), default: Optional[bool] = None,
                 current_user: UserBase = Depends(get_current_user)):
    try:
        if not default:
            return db_user_address.my_addresses(db, current_user.id)
        return db_user_address.get_default_address(db, current_user.id)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such address exists!")


@router.get('/{id}', response_model=AddressPrivateDisplay)
def get_address_privately(address_id: int, db: Session = Depends(get_db),
                          current_user: UserBase = Depends(get_current_user)):
    try:
        addresses = db_user_address.my_addresses(db, current_user.id)
        filtered_address = [adr for adr in addresses if adr.id == address_id]
        if filtered_address[0].id == address_id:
            return db_user_address.get_address(db, address_id)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to see this address!")


@router.put('/{id}', response_model=AddressPrivateDisplay)
def modify_address(request: AddressBase, id: int,
                   db: Session = Depends(get_db),
                   default: Optional[bool] = None,
                   current_user: UserBase = Depends(get_current_user)):
    address = db_user_address.get_address(db, id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such address exists!")
    if default != None:
        return db_user_address.set_default_address(db, id, current_user.id)
    if current_user.id != address.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this address!")
    return db_user_address.modify_address(db, id, request)


@router.delete('/{id}')
def delete_address(id: int,
                   db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    address = db_user_address.get_address(db, id)
    try:
        if current_user.id != address.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this address!")
        return db_user_address.delete_address(db, id)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No such address exists!")
