from . import *
from schemas.product import ProductBase
from db.models import DbProduct, DbBid
from schemas.bid import BidStatus
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


def get_products_by_seller_and_state(db: Session, seller_id: int, state: StateEnum) -> List[DbProduct]:
    return db.query(DbProduct).filter(DbProduct.seller_id == seller_id, DbProduct.state == state).all()


def get_products_by_seller(db: Session, seller_id: int) -> List[DbProduct]:
    return db.query(DbProduct).filter(DbProduct.seller_id == seller_id).all()


def get_products_bought_by_user(db: Session, user_id: int) -> List[DbProduct]:
    return db.query(DbProduct).filter(DbProduct.buyer_id == user_id).all()


def get_products_user_is_bidding_on(db: Session, user_id: int) -> List[DbProduct]:
    pending_bids = db.query(DbBid).filter(
            DbBid.bidder_id == user_id,
            DbBid.status == BidStatus.PENDING
    ).all()
    product_ids = [bid.product_id for bid in pending_bids]
    return db.query(DbProduct).filter(DbProduct.id.in_(product_ids)).all()
