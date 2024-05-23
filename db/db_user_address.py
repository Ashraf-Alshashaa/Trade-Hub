from . import *

from . import *
from schemas.user_address import AddressBase
from db.models import DbAddress


def add_address(db: Session, request: AddressBase):
    new_address = DbAddress(
                    street_name=request.street,
                    house_number=request.house_number,
                    city=request.city,
                    country=request.country,
                    postcode=request.postcode,
                    user_id = request.user_id
                    )
    db.add(new_address)
    db.commit()
    # db.refresh(new_address)
    return new_address


def my_addresses(db: Session):
    return db.query(DbAddress).filter(DbAddress.user_id == id).all()


def get_address(db: Session, id: int):
    return db.query(DbAddress).filter(DbAddress.id == id).first()


def modify_address(db: Session, id: int, request: AddressBase):
    address = db.query(DbAddress).filter(DbAddress.id == id)
    if not address:
        raise status.HTTPException(status_code=404, detail="Address not found")
    address.update({
                DbAddress.street_name: request.street,
                DbAddress.house_number: request.house_number,
                DbAddress.city: request.city,
                DbAddress.country: request.country,
                DbAddress.postcode: request.postcode,
                DbAddress.user_id: request.user_id
                })
    db.commit()
    return address.first()


def delete_address(db: Session, id: int):
    address = db.query(DbAddress).filter(DbAddress.id == id).first()
    if not address:
        raise status.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(address)
    db.commit()
    return 'ok'

