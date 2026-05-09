from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from modules.dispatch.service import list_driver_states

router = APIRouter()
dispatch_file = Path(__file__).resolve().parent / "templates" / "dispatch.html"


@router.get("/dispatch")
def dispatch_page() -> FileResponse:
    return FileResponse(dispatch_file)


@router.get("/api/drivers")
def drivers_api() -> list[dict[str, str | float]]:
    return list_driver_states()
