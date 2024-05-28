from . import *
from schemas.product import ProductBase, ProductDisplay
from db.models import DbProduct, DbAddress
from db.db_user_address import is_first_address


def add_product(db: Session, request: ProductBase):
    new_item = DbProduct(
                    name=request.name,
                    image=request.image,
                    description=request.description,
                    seller_id=request.seller_id,
                    buyer_id=request.buyer_id,
                    price=request.price,
                    date=request.date,
                    condition=request.condition,
                    state=request.state)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# Needs reconsidaration - All items based on their state
def get_all_products(db: Session):
    return db.query(DbProduct).all()


def get_product(db: Session, id: int):
    item = db.query(DbProduct).filter(DbProduct.id == id).first()
    address = db.query(DbAddress).filter(DbAddress.default, item.seller_id == DbAddress.user_id).first()
    if not item:
        raise status.HTTPException(status_code=404, detail="Product not found")
    if is_first_address(db, id):
        db_address = db.query(DbAddress).filter(DbAddress.default).first()
        if not db_address:
            address = None
    product = ProductDisplay(
        name=item.name,
        image=item.image,
        description=item.description,
        price=item.price,
        date=item.date,
        condition=item.condition,
        state=item.state,
        address=address
    )
    return product


def modify_product(db: Session, id: int, request: ProductBase):
    item = db.query(DbProduct).filter(DbProduct.id == id)
    if not item:
        raise status.HTTPException(status_code=404, detail="Product not found")
    item.update({
                DbProduct.name: request.name,
                DbProduct.image: request.image,
                DbProduct.description: request.description,
                DbProduct.price: request.price,
                DbProduct.date: request.date,
                DbProduct.condition: request.condition,
                DbProduct.state: request.state})
    db.commit()
    return item.first()


def delete_product(db: Session, id: int):
    item = db.query(DbProduct).filter(DbProduct.id == id).first()
    if not item:
        raise status.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(item)
    db.commit()
    return 'ok'

