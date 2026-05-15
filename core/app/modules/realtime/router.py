import json
from datetime import UTC, datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
connections: set[WebSocket] = set()


async def broadcast(message: str, *, skip: WebSocket | None = None) -> None:
    for client in list(connections):
        if client is skip:
            continue
        try:
            await client.send_text(message)
        except RuntimeError:
            connections.discard(client)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    connections.add(websocket)
    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect:
            connections.discard(websocket)
            break

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
            await broadcast(
                json.dumps(
                    {
                        "type": "driver_location",
                        "driverId": driver_id,
                        "lat": lat,
                        "lng": lng,
                        "status": status,
                        "updatedAt": datetime.now(UTC).isoformat(),
                    }
                ),
                skip=websocket,
            )
            continue

        await websocket.send_text(json.dumps({"type": "ack", "payload": payload}))
        await broadcast(
            json.dumps(
                {
                    "type": "message",
                    "payload": payload,
                    "updatedAt": datetime.now(UTC).isoformat(),
                }
            ),
            skip=websocket,
        )
