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
    """
               Add a new address.
    """
    request.user_id = current_user.id
    return db_user_address.add_address(db, request, current_user.id)


@router.get('', response_model=List[AddressPrivateDisplay])
def all_my_addresses(user_id: int,
                     db: Session = Depends(get_db),
                     default: Optional[bool] = None,
                     current_user: UserBase = Depends(get_current_user)):
    """
               View you addresses. You can see all your addresses as a list.
               If you set the default variable to true then you only see your default address.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorised.")
    if default:
        return db_user_address.get_default_address(db, current_user.id)
    elif default==False:
        return []
    return db_user_address.my_addresses(db, current_user.id)


@router.get('/{id}', response_model=AddressPrivateDisplay)
def get_address_by_id(user_id: int,
                      id: int,
                      db: Session = Depends(get_db),
                      current_user: UserBase = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorised.")
    addresses = db_user_address.my_addresses(db, current_user.id)
    try:
        filtered_address = [adr for adr in addresses if adr.id == id]
        if filtered_address[0].id == id:
            return db_user_address.get_address(db, id)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorised.")


@router.put('/{id}', response_model=AddressPrivateDisplay)
def modify_address(request: AddressBase,
                   id: int,
                   db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    """
               Modify an existing address or change your default address by the address ID.
               only if the address default is false then you can set it to true to make it your default address.
               If you intend to modify the sepecifications of your address then you should not change the default value.

               - **address_id**: ID of the address to be modified.
    """
    address = db_user_address.get_address(db, id)
    user_id = address.user_id
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorised.")
    try:
        addresses = db_user_address.my_addresses(db, current_user.id)
        filtered_address = [adr for adr in addresses if adr.id == id]
        if filtered_address[0].id == id:
            if address.default:
                return db_user_address.modify_address(db, id, request)
            else:
                if request.default:
                    return db_user_address.set_default_address(db, id, current_user.id)
            return db_user_address.modify_address(db, id, request)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorised.")


@router.delete('/{id}')
def delete_address(id: int,
                   db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    address = db_user_address.get_address(db, id)
    user_id = address.user_id
    if current_user.id != address.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this address!")
    return db_user_address.delete_address(db, id, user_id)

