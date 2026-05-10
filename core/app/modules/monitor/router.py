from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from modules.monitor.service import list_messages

router = APIRouter()
monitor_file = Path(__file__).resolve().parent / "templates" / "monitor.html"


@router.get("/monitor")
def monitor_page() -> FileResponse:
    return FileResponse(monitor_file)


@router.get("/api/messages")
def messages_api() -> list[dict[str, str]]:
    return list_messages()
