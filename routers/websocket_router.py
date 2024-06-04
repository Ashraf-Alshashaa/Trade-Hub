from notifications.notification import NotificationCenter, NotificationType, InAppNotification
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter

router = APIRouter(prefix='/ws', tags=['notifications'])
notify = NotificationCenter()
connections: [WebSocket] = []

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await notify.in_app.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notify.in_app.disconnect(websocket)



@router.post("/trigger-event/")
async def trigger_event(message: str):
    await notify.notify_user(NotificationType.IN_APP,recipient=1, message=message)
    return {"message": f"Notification sent{message}"}


