from collections import deque
from datetime import datetime, timezone
from threading import Lock

message_log = deque(maxlen=500)
message_log_lock = Lock()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def add_message(source: str, data: str) -> None:
    with message_log_lock:
        message_log.append(
            {
                "time": now_iso(),
                "source": source,
                "data": data,
            }
        )


def get_messages() -> list[dict[str, str]]:
    with message_log_lock:
        return list(message_log)