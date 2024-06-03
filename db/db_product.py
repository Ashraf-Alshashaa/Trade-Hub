from . import *
from schemas.product import ProductBase, ProductDisplay
from db.models import DbProduct, DbBid
from schemas.bid import BidStatus
from typing import Optional


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
                    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_all_products(db: Session):
    return db.query(DbProduct).all()


def get_product(db: Session, id: int):
    item = db.query(DbProduct).filter(DbProduct.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return item


def modify_product(db: Session, id: int, request: ProductBase):
    item = db.query(DbProduct).filter(DbProduct.id == id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    item.update({
                DbProduct.name: request.name,
                DbProduct.image: request.image,
                DbProduct.description: request.description,
                DbProduct.price: request.price,
                DbProduct.date: request.date,
                DbProduct.condition: request.condition,
                })
    db.commit()
    return item.first()


def delete_product(db: Session, id: int):
    item = db.query(DbProduct).filter(DbProduct.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
    db.delete(item)
    db.commit()
    return 'ok'


def get_products_by_seller_and_state(db: Session, seller_id: int, sold: bool):
     # Determine the filter condition based on the sold status
    if sold:
        products = db.query(DbProduct).filter(DbProduct.seller_id == seller_id, DbProduct.buyer_id != None).all()
    else:
        products = db.query(DbProduct).filter(DbProduct.seller_id == seller_id, DbProduct.buyer_id == None).all()

    # Raise an exception if no products are found
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")

    return products


def get_products_by_seller(db: Session, seller_id: int):
    item = db.query(DbProduct).filter(DbProduct.seller_id == seller_id).all()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
    return item


def get_products_bought_by_user(db: Session, user_id: int):
    item = db.query(DbProduct).filter(DbProduct.buyer_id == user_id).all()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
    return item


def get_products_user_is_bidding_on(db: Session, user_id: int):
    pending_bids = db.query(DbBid).filter(
            DbBid.bidder_id == user_id,
            DbBid.status == BidStatus.PENDING
    ).all()
    product_ids = [bid.product_id for bid in pending_bids]
    item = db.query(DbProduct).filter(DbProduct.id.in_(product_ids)).all()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
    return item


def get_cart(db: Session, user_id: int):
    my_accepted_bids = db.query(DbBid).filter(DbBid.bidder_id == user_id, DbBid.status == BidStatus.ACCEPTED).all()
    # Extract product IDs from the accepted bids
    product_ids = [bid.product_id for bid in my_accepted_bids]

    # Query products using the extracted product IDs
    products = db.query(DbProduct).filter(DbProduct.id.in_(product_ids)).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")

    return products


def choose_buyer(db: Session, bid_id: int):

    bid = db.query(DbBid).filter(DbBid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found")

    product = db.query(DbProduct).filter(DbProduct.id == bid.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Set the buyer of the product and update the product price
    product.buyer_id = bid.bidder_id
    bid.status = BidStatus.ACCEPTED
    product.price = bid.price

    db.commit()

    return product

def filter_available_products(
        db: Session, 
        search_str: Optional[str] = None, 
        max_price: Optional[int] = None,
        min_price: Optional[int] = None
        ) -> List[ProductDisplay]:
    """
        Filter available products based on search criteria, maximum price, and minimum price.

    Parameters:
    - **db**: Session
        Database session. (Required)
    - **search_str**: Optional[str]
        Search for products using their name or description. This is an optional string parameter.
    - **max_price**: Optional[int]
        Filter products with a price less than or equal to the specified value. This is an optional integer parameter.
    - **min_price**: Optional[int]
        Filter products with a price greater than or equal to the specified value. This is an optional integer parameter.

    Returns:
    - **List[ProductDisplay]**
        List of products matching the specified filters, serialized as `ProductDisplay` Pydantic models.

    """

    available_products_query = db.query(DbProduct).filter(DbProduct.buyer_id == None)


    if search_str and len(search_str) > 0:
        available_products_query = available_products_query.filter(
            DbProduct.name.ilike(f"%{search_str}%") |
            DbProduct.description.ilike(f"%{search_str}%")
        )

    if max_price:
        available_products_query = available_products_query.filter(DbProduct.price <= max_price)

    if min_price:
        available_products_query = available_products_query.filter(DbProduct.price >= min_price)

    products = available_products_query.all()

    return [ProductDisplay.model_validate(product) for product in products]
