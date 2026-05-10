from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
simulator_file = Path(__file__).resolve().parent / "templates" / "simulator.html"


@router.get("/sim")
def simulator_page() -> FileResponse:
    return FileResponse(simulator_file)
