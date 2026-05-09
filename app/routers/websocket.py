from fastapi import APIRouter, WebSocket

from services.message_store import add_message

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received: {data}")
        add_message("ws", data)
        await websocket.send_text(f"Echo: {data}")