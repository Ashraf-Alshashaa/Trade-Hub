from . import *
from controllers.products import get_product_controller

router = APIRouter(
  prefix='/products',
  tags=['products']
)

@router.get('/{id}')
def get_product(id: int):
    return get_product_controller(id)
