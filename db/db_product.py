from . import *
from schemas.product import ProductBase
from db.models import DbProduct
from schemas.product import StateEnum


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
    return db.query(DbProduct).filter(DbProduct.id == id).first()


def modify_product(db: Session, id: int, request: ProductBase):
    item = db.query(DbProduct).filter(DbProduct.id == id)
    if not item:
        raise status.HTTPException(status_code=404, detail="Product not found")
    item.update({
                DbProduct.name: request.name,
                DbProduct.image: request.image,
                DbProduct.description: request.description,
                DbProduct.seller_id: request.seller_id,
                DbProduct.buyer_id: request.buyer_id,
                DbProduct.price: request.price,
                DbProduct.date: request.date,
                DbProduct.condition: request.condition,
                DbProduct.state: request.state})
    db.commit()
    return item


def delete_product(db: Session, id: int):
    item = db.query(DbProduct).filter(DbProduct.id == id).first()
    if not item:
        raise status.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(item)
    db.commit()
    return 'ok'


def get_products_by_seller_and_state(db: Session, seller_id: int, state: StateEnum) -> List[DbProduct]:
    return db.query(DbProduct).filter(DbProduct.seller_id == seller_id, DbProduct.state == state).all()


def get_products_by_seller(db: Session, seller_id: int) -> List[DbProduct]:
    return db.query(DbProduct).filter(DbProduct.seller_id == seller_id).all()
