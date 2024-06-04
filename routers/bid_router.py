from . import *
from schemas.bid import BidDisplay, BidBase
from db.models import DbBid, DbProduct, DbUser
from db import db_bid
from typing import List, Optional
from notifications.notification import NotificationCenter, NotificationType
from fastapi.websockets import WebSocket, WebSocketDisconnect

connections: [int, WebSocket] = {}

router = APIRouter(prefix='/bids', tags=['bids'])
notify = NotificationCenter()


@router.post('', response_model=BidDisplay)
async def add_bid(request: BidBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Check if the user is authenticated
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be authenticated to place a bid")

    # Check if the product exists
    product = db.query(DbProduct).filter(DbProduct.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Check if the current user is not the seller of the product
    if product.seller_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot bid on your own product")

    # Set the bidder_id to the current user's id
    request.bidder_id = current_user.id
    request.status = "PENDING"

    # Add the bid to the database
    bid = db_bid.add_bid(db, request)
    product_id = db.query(DbBid).filter(DbBid.id == bid.id).first().product_id
    seller_id = db.query(DbProduct).filter(DbProduct.id == product_id).first().seller_id
    user = db.query(DbUser).filter(DbUser.id == seller_id).first()
    product = db.query(DbProduct).filter(DbProduct.id == product_id).first()

    print(connections[user.id])
    await notify.notify_user(NotificationType.IN_APP,
                       recipient=user.id,
                       message=f"There is a new bid on your product {product_id} ")

    await notify.notify_user(NotificationType.EMAIL,
                       recipient=user.email, subject="New bid",
                       body=f"You have a new bid on your product {product.name}")



    return bid


@router.get('', response_model=List[BidDisplay])
def get_all_bids(
        product_id: int = Query(...),
        db: Session = Depends(get_db)
):
    return db_bid.get_all_bids(db, product_id)


@router.get('/{id}', response_model=BidDisplay)
def get_bid(id: int, db: Session = Depends(get_db)):
    return db_bid.get_bid(db, id)


@router.websocket("/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    await notify.in_app.connect(user_id, websocket)
    connections[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notify.in_app.disconnect(websocket)
