from . import *
from db import db_product
from schemas.product import ProductDisplay, ProductBase
from schemas.product import StateEnum
from sqlalchemy.sql.sqltypes import List
from typing import Optional
from fastapi import HTTPException, status


router = APIRouter(prefix='/products', tags=['products'])


@router.post('', response_model=ProductDisplay)
def add_product(
        request: ProductBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    # Set the seller_id to the current user's id
    request.seller_id = current_user.id
    return db_product.add_product(db, request)


@router.get('', response_model=List[ProductDisplay])
def get_products_filtered(
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),
        seller_id: Optional[int] = None,
        state: StateEnum = Query(None),
        buyer_id: Optional[int] = None,
        bidder_id: Optional[int] = None

):
    if buyer_id != None:
        if buyer_id != current_user.id: # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're only authorized to list bought products of your own")
        return db_product.get_products_bought_by_user(db, buyer_id)

    if bidder_id != None:
        if bidder_id != current_user.id: # and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're only authorized to list bids of your own")
        return db_product.get_products_user_is_bidding_on(db, bidder_id)

    if seller_id != None:
        if state != None:
            products = db_product.get_products_by_seller_and_state(db, seller_id, state)
            if not products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found for this seller")
            return products
        else:
            products = db_product.get_products_by_seller(db, seller_id)
            if not products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found for this seller")
            return products


@router.get('/{id}', response_model=ProductDisplay)
def get_product(id: int, db: Session = Depends(get_db)):
    return db_product.get_product(db, id)


@router.put('/{id}', response_model=ProductDisplay)
def modify_product(id: int, request: ProductBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Fetch the product to verify ownership
    product = db_product.get_product(db, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this product")
    return db_product.modify_product(db, id, request)


@router.delete('/{id}')
def delete_product(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Fetch the product to verify ownership
    product = db_product.get_product(db, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this product")
    return db_product.delete_product(db, id)
