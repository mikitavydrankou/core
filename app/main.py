from fastapi import FastAPI, WebSocket

app = FastAPI()

# простой REST
@app.get("/")
def read_root():
    return {"message": "Taxi dispatch prototypeee"}

# WebSocket для real-time координат
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received: {data}")
        await websocket.send_text(f"Echo: {data}")