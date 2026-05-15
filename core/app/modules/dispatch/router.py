from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
dispatch_file = Path(__file__).resolve().parent / "templates" / "dispatch.html"


@router.get("/dispatch")
def dispatch_page() -> FileResponse:
    return FileResponse(dispatch_file)
