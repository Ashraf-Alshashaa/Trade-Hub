from . import *

router = APIRouter(prefix='/bidding', tags=['bidding'])

@router.post('/add')
def add_bidding(id: int, db: Session = Depends(get_db)):
    return id