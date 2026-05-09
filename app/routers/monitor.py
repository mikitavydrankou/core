from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from services.message_store import get_messages

router = APIRouter()
monitor_file = Path(__file__).resolve().parents[1] / "templates" / "monitor.html"


@router.get("/monitor")
def monitor_page() -> FileResponse:
    return FileResponse(monitor_file)


@router.get("/api/messages")
def messages_api() -> list[dict[str, str]]:
    return get_messages()