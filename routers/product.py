from . import *

router = APIRouter(prefix='/product', tags=['product'])

@router.get('/{id}')
def get_product(id: int, db: Session = Depends(get_db)):
    return id