from collections import deque
from datetime import UTC, datetime
from threading import Lock

message_log = deque(maxlen=500)
message_log_lock = Lock()
driver_states: dict[str, dict[str, str | float]] = {}
driver_states_lock = Lock()


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


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


def upsert_driver_state(driver_id: str, lat: float, lng: float, status: str = "online") -> None:
    with driver_states_lock:
        driver_states[driver_id] = {
            "driverId": driver_id,
            "lat": lat,
            "lng": lng,
            "status": status,
            "updatedAt": now_iso(),
        }


def get_driver_states() -> list[dict[str, str | float]]:
    with driver_states_lock:
        return list(driver_states.values())
