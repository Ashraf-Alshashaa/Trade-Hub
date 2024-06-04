from notifications.notification import NotificationCenter, NotificationType, InAppNotification
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter

router = APIRouter(prefix='/ws', tags=['notifications'])
notify = NotificationCenter()
connections: [int, WebSocket] = {}


@router.websocket("/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    await notify.in_app.connect(user_id, websocket)
    connections[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notify.in_app.disconnect(websocket)


@router.post("/trigger-event/")
async def trigger_event(message: str):
    await notify.notify_user(NotificationType.IN_APP,recipient=connections.keys(), message=message)
    return {"message": f"Notification sent{message}"}


