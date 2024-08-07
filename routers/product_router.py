from . import *
from db import db_product, db_bid
from schemas.product import ProductDisplay, ProductBase
from sqlalchemy.sql.sqltypes import List
from typing import Optional
from db.models import DbProduct, DbUser, DbBid
from notifications.notification import NotificationCenter, NotificationType


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
    request.buyer_id = None
    return db_product.add_product(db, request)


@router.get('', response_model=List[ProductDisplay])
def get_products_filtered(
        db: Session = Depends(get_db),
        search_str: Optional[str] = None,
        category_id: Optional[int] = None,
        seller_id: Optional[int] = None,
        sold: Optional[bool] = None,
        buyer_id: Optional[int] = None,
        bidder_id: Optional[int] = None,
        user_id: Optional[int] = None,
        max_price: Optional[int] = None,
        min_price: Optional[int] = None,
        current_user: UserBase = Depends(optional_get_current_user)
):

    """
        Get products filtered by various criteria.
        
        If you don't specify any query the Endpoint will return you all available products

        - **db**: Database session.
        - **search_str**: search for product using it's name or description (optional).
        - **max_price**: Integer for filtering available products with a price less than or equal to the max_price value (optional).
        - **min_price**: Integer for filtering available products with a price greater than or equal to the min_price value (optional).
        - **current_user**: Currently authenticated user.
        - **seller_id**: Filter products by seller ID (optional).
        - **sold**: Add this True/False to see seller's sold/available products (optional).
        - **buyer_id**: Filter products bought by user (optional).
        - **bidder_id**: Filter products that user id bidding on by bidder ID (optional).
        - **user_id**: Get all products in the cart of the user, where their bid is accepted (optional).
        """
    products = []
    if search_str or max_price or min_price or category_id:
        products = db_product.filter_available_products(db, search_str, category_id, max_price, min_price)    
    elif buyer_id is not None:
        if buyer_id != current_user.id:  # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're only authorized to list bought products of your own")
        products = db_product.get_products_bought_by_user(db, buyer_id)

    elif bidder_id is not None:
        if bidder_id != current_user.id:  # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You're only authorized to list bids of your own")
        products = db_product.get_products_user_is_bidding_on(db, bidder_id)

    elif seller_id is not None or sold is not None:
        products = db_product.get_products_by_seller_and_state(db, seller_id, sold)

    elif user_id is not None:
        if user_id != current_user.id:  # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Please Login!")
        products = db_product.get_cart(db, user_id)
        return products
    else:
        products = db_product.get_all_available_products(db)
    return products        

@router.get('/price-range')
def get_price_range(db: Session = Depends(get_db)):
    return db_product.get_price_range(db)


@router.get('/{id}', response_model=ProductDisplay)
def get_product(id: int, db: Session = Depends(get_db)):
    """
       Get a product by its ID.

       - **id**: ID of the product to retrieve.
       - **db**: Database session.
       """
    return db_product.get_product(db, id)


@router.put('/{id}', response_model=ProductDisplay)
async def change_product(
        id: int,
        request: ProductBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    """
        Modify an existing product or choose a buyer for it.

        - **product_id**: ID of the product to be modified.
        - **request**: New product details.
        - **current_user**: Currently authenticated user.
        """

    product = db_product.get_product(db, id)
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this product")
    return db_product.modify_product(db, id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
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
