from . import *

router = APIRouter(prefix='/bid', tags=['bidding'])

@router.post('/add')
def add_bid(id: int, db: Session = Depends(get_db)):
    return id