from . import *
from schemas.product import ProductBase, ProductDisplay
from db.models import DbProduct, DbBid
from schemas.bid import BidStatus
from typing import Optional
from sqlalchemy import or_


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
                    category_id=request.category_id
                    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_all_available_products(db: Session):
    available_products = (
        db.query(DbProduct)
        .outerjoin(DbBid, (DbProduct.id == DbBid.product_id) & (DbBid.status == BidStatus.ACCEPTED))
        .filter(DbProduct.buyer_id == None)
        .filter(DbBid.id == None)
        .all()
    )
    return available_products


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
                DbProduct.category_id: request.category_id,
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


def get_products_by_seller_and_state(
        db: Session,
        seller_id: Optional[int] = None,
        sold: Optional[bool] = None
):
    query = db.query(DbProduct)

    # Filter by seller_id if provided
    if seller_id is not None:
        query = query.filter(DbProduct.seller_id == seller_id)

    # Filter by sold status if provided
    if sold is not None:
        if sold:
            query = query.filter(DbProduct.buyer_id.isnot(None))
        else:
            query = query.filter(DbProduct.buyer_id.is_(None))

    products = query.all()

    if not products:
        return []
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")

    return [ProductDisplay.model_validate(product) for product in products]


def get_products_bought_by_user(db: Session, user_id: int):
    # Fetch products where buyer_id matches user_id
    bought_items = db.query(DbProduct).filter(DbProduct.buyer_id == user_id).all()

    # if not bought_items:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")

    # Filter out products with accepted bids
    valid_products = []
    for product in bought_items:
        # Check for accepted bids for each product
        accepted_bid = db.query(DbBid).filter(
                DbBid.product_id == product.id,
                DbBid.status == BidStatus.ACCEPTED
        ).first()

        if not accepted_bid:
            valid_products.append(product)

    # if not valid_products:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No valid products found")

    return valid_products


def get_products_user_is_bidding_on(db: Session, user_id: int):
    pending_bids = db.query(DbBid).filter(
        DbBid.bidder_id == user_id,
        DbBid.status == BidStatus.PENDING
    ).all()

    # Extract product IDs from pending bids
    product_ids_with_pending_bids = {bid.product_id for bid in pending_bids}

    # Get products where there is no buyer_id and all bids are PENDING
    products = db.query(DbProduct).filter(
        DbProduct.id.in_(product_ids_with_pending_bids),  # Filter by products with pending bids
        DbProduct.buyer_id.is_(None)  # Filter by products without a buyer
    ).all()

    # if not products:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")

    return products


def get_cart(db: Session, user_id: int):
    my_accepted_bids = db.query(DbBid).filter(DbBid.bidder_id == user_id, DbBid.status == BidStatus.ACCEPTED).all()
    # Extract product IDs from the accepted bids
    product_ids = [bid.product_id for bid in my_accepted_bids]

    # Query products using the extracted product IDs
    products = db.query(DbProduct).filter(DbProduct.id.in_(product_ids)).all()

    if not products:
        # 
        return []

    return products




def filter_available_products(
        db: Session, 
        search_str: Optional[str] = None, 
        category_id: Optional[int] = None,
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
    - **category_id**: Optional[int]
        Filter products with a category. This is an optional integer parameter.
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
            or_(DbProduct.name.ilike(f"%{search_str}%"),
            DbProduct.description.ilike(f"%{search_str}%"))
        )

    if category_id:
        available_products_query = available_products_query.filter(DbProduct.category_id == category_id)

    if max_price:
        available_products_query = available_products_query.filter(DbProduct.price <= max_price)

    if min_price:
        available_products_query = available_products_query.filter(DbProduct.price >= min_price)

    products = available_products_query.all()

    return [ProductDisplay.model_validate(product) for product in products]

def get_price_range(db: Session):
    available_products = db.query(DbProduct).filter(DbProduct.buyer_id == None).all()
    min_price = min(product.price for product in available_products)
    max_price = max(product.price for product in available_products)
    return {"min_price": min_price, "max_price": max_price}

