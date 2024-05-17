from . import *

router = APIRouter(
  prefix='/products',
  tags=['products']
)

@router.get('/{id}')
def get_product(id: int):
  return {
    'data':  id
  }