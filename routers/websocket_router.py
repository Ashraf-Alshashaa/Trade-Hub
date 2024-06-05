from . import *
from fastapi import APIRouter
from typing import Annotated

router = APIRouter(prefix='/ws', tags=['notifications'])



async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, db] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@router.websocket("/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket, current_user: UserBase = Depends(get_current_user)):
    await notify.in_app.connect(user_id, websocket)
    connections[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notify.in_app.disconnect(websocket)
