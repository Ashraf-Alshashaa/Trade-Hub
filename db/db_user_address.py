from . import *
from schemas.user_address import AddressBase
from db.models import DbAddress
from fastapi import status, HTTPException


def is_first_address(db: Session, current_user: int):
    address_count = db.query(DbAddress).filter(DbAddress.user_id == current_user).count()
    if address_count == 1:
        return True
    return False


def add_address(db: Session, request: AddressBase, user_id: int):
    new_address = DbAddress(
                    street_name=request.street_name,
                    house_number=request.house_number,
                    city=request.city,
                    country=request.country,
                    postcode=request.postcode,
                    user_id=request.user_id,
                    default=False
                    )
    db.add(new_address)
    db.commit()
    if is_first_address(db,user_id):
        new_address.default = True
        db.commit()
    db.refresh(new_address)
    return new_address


def my_addresses(db: Session, user_id: int):
    address = db.query(DbAddress).filter(DbAddress.user_id == user_id).all()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address


def get_address(db: Session, id: int):
    address = db.query(DbAddress).filter(DbAddress.id == id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address.all()


def modify_address(db: Session, id: int, request: AddressBase):
    address = db.query(DbAddress).filter(DbAddress.id == id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    address.update({
                DbAddress.street_name: request.street_name,
                DbAddress.house_number: request.house_number,
                DbAddress.city: request.city,
                DbAddress.country: request.country,
                DbAddress.postcode: request.postcode,
                })
    db.commit()
    return address.first()


def set_default_address(db: Session, id: int, current_user: int):
    address = db.query(DbAddress).filter(DbAddress.id == id)
    db.query(DbAddress).filter(DbAddress.user_id == current_user).update({DbAddress.default: False})
    db.commit()
    address.update({DbAddress.default: True})
    db.commit()
    return address.first()


def get_default_address(db: Session, user_id: int):
    return db.query(DbAddress).filter(DbAddress.default, DbAddress.user_id == user_id).all()


def delete_address(db: Session, id: int):
    address = db.query(DbAddress).filter(DbAddress.id == id).first()
    count = db.query(DbAddress).filter(DbAddress.id == id).count()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    if address.default and count != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete your default address,"
                                                                             " change it first!")
    db.delete(address)
    db.commit()
    return 'ok'

