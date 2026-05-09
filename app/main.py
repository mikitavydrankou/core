from fastapi import FastAPI

from modules.dispatch.router import router as dispatch_router
from modules.monitor.router import router as monitor_router
from modules.realtime.router import router as websocket_router
from modules.root.router import router as root_router
from modules.simulator.router import router as simulator_router

app = FastAPI()

app.include_router(root_router)
app.include_router(monitor_router)
app.include_router(dispatch_router)
app.include_router(simulator_router)
app.include_router(websocket_router)