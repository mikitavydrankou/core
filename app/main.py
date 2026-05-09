from fastapi import FastAPI

from routers.monitor import router as monitor_router
from routers.root import router as root_router
from routers.websocket import router as websocket_router

app = FastAPI()

app.include_router(root_router)
app.include_router(monitor_router)
app.include_router(websocket_router)