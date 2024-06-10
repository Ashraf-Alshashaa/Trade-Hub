from . import *
from fastapi import APIRouter

router = APIRouter(prefix='/ws', tags=['notifications'])



@router.websocket("/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    await notify.in_app.connect(user_id, websocket)
    connections[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notify.in_app.disconnect(websocket)
