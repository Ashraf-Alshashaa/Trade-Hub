from . import *
from db import db_product, db_bid
from schemas.product import ProductDisplay, ProductBase
from sqlalchemy.sql.sqltypes import List
from typing import Optional
from db.models import DbProduct


router = APIRouter(prefix='/products', tags=['products'])


@router.post('', response_model=ProductDisplay)
def add_product(
        request: ProductBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    """
        Add a new product.

        - **request**: Product details to be added.
        - **db**: Database session.
        - **current_user**: Currently authenticated user.
        """
    # Set the seller_id to the current user's id
    request.seller_id = current_user.id
    return db_product.add_product(db, request)


@router.get('', response_model=List[ProductDisplay])
def get_products_filtered(
        db: Session = Depends(get_db),
        seller_id: Optional[int] = None,
        sold: Optional[bool] = None,
        buyer_id: Optional[int] = None,
        bidder_id: Optional[int] = None,
        user_id: Optional[int] = Query(None, alias='cart of the user'),
        current_user: UserBase = Depends(get_current_user)
):

    """
        Get products filtered by various criteria.

        - **db**: Database session.
        - **current_user**: Currently authenticated user.
        - **seller_id**: Filter products by seller ID (optional).
        - **sold**: Add this True/False to see seller's sold/available products (optional).
        - **buyer_id**: Filter products bought by user (optional).
        - **bidder_id**: Filter products that user id bidding on by bidder ID (optional).
        - **user_id**: Get all products in the cart of the user, where their bid is accepted (optional).
        """
    if buyer_id is not None:
        if buyer_id != current_user.id:  # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're only authorized to list bought products of your own")
        return db_product.get_products_bought_by_user(db, buyer_id)

    if bidder_id is not None:
        if bidder_id != current_user.id:  # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're only authorized to list bids of your own")
        return db_product.get_products_user_is_bidding_on(db, bidder_id)

    if seller_id is not None:
        if sold is not None:
            products = db_product.get_products_by_seller_and_state(db, seller_id, sold)
            return products
        else:
            products = db_product.get_products_by_seller(db, seller_id)
            return products

    if user_id is not None:
        if user_id != current_user.id:  # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're only authorized to see the cart of your own")
        products = db_product.get_cart(db, user_id)
        return products


@router.get('/{id}', response_model=ProductDisplay)
def get_product(id: int, db: Session = Depends(get_db)):
    """
       Get a product by its ID.

       - **id**: ID of the product to retrieve.
       - **db**: Database session.
       """
    return db_product.get_product(db, id)


@router.put('/{id}', response_model=ProductDisplay)
def change_product(
        product_id: int,
        bid_id: Optional[int] = Query(None, alias='bid_id that won'),
        db: Session = Depends(get_db),
        request: Optional[ProductBase] = None,
        current_user: UserBase = Depends(get_current_user)
):
    """
        Modify an existing product or choose a buyer for it.

        - **product_id**: ID of the product to be modified.
        - **bid_id that won**: ID of the bid to add the buyer of the product (optional).
        - **db**: Database session.
        - **request**: New product details (optional).
        - **current_user**: Currently authenticated user.
        """

    # Retrieve the product from the database
    product = db_product.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    seller_id = product.seller_id

    # Check if the current user is the seller
    if seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this product")

    if bid_id is not None:
        bid = db_bid.get_bid(db, bid_id)
        if bid.product_id != product_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this bid")
        return db_product.choose_buyer(db, bid_id)

    if request is not None:

        product = db_product.get_product(db, product_id)
        if product.seller_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this product")
        return db_product.modify_product(db, product_id, request)


@router.delete('/{id}')
def delete_product(
        id: int,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    """
       Delete a product by its ID.

       - **id**: ID of the product to delete.
       - **db**: Database session.
       - **current_user**: Currently authenticated user.
       """
    # Fetch the product to verify ownership
    product = db_product.get_product(db, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this product")
    return db_product.delete_product(db, id)
