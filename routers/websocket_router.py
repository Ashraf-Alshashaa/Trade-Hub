from . import *
from fastapi import APIRouter, Cookie, WebSocketException
from typing import Annotated, Union

router = APIRouter(prefix='/ws', tags=['notifications'])



@router.websocket("/{user_id}")
async def websocket_endpoint(user_id: int,
                             websocket: WebSocket,
                             token: Annotated[Session, Depends(get_current_user)]):
    if token:
        await notify.in_app.connect(user_id, websocket)

        connections[user_id] = websocket
    await websocket.send_text(
            f"Session cookie or query token value is: {token}"
    )
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notify.in_app.disconnect(websocket)
