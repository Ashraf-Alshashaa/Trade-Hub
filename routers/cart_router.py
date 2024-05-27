from . import *
from schemas.product import ProductDisplay
from typing import List, Dict, Union
from db import db_product


router = APIRouter(prefix='/cart', tags=['cart'])


@router.get("", response_model=Dict[str, Union[List[ProductDisplay], float]])
def get_cart(
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
        products, total_price = db_product.get_cart(db, current_user.id)
        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products in cart")
        return {
            "products": products,
            "total_price": total_price
        }


@router.delete("/remove_product/{product_id}")
def delete_product_from_cart(
        product_id: int,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    return db_product.delete_product_from_cart(db, product_id, current_user.id)
