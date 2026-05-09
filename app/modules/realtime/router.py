import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from shared.message_store import add_message, upsert_driver_state

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect:
            break
        print(f"Received: {data}")
        add_message("ws", data)

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            await websocket.send_text(f"Echo: {data}")
            continue

        if payload.get("type") == "driver_location":
            driver_id = str(payload.get("driverId", "unknown"))
            lat = float(payload.get("lat"))
            lng = float(payload.get("lng"))
            status = str(payload.get("status", "online"))
            upsert_driver_state(driver_id, lat, lng, status)
            await websocket.send_text(
                json.dumps(
                    {
                        "type": "driver_ack",
                        "driverId": driver_id,
                        "lat": lat,
                        "lng": lng,
                        "status": status,
                    }
                )
            )
            continue

        await websocket.send_text(json.dumps({"type": "ack", "payload": payload}))
