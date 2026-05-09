import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from main import app  # noqa: E402
from shared import message_store  # noqa: E402


@pytest.fixture(autouse=True)
def reset_in_memory_state() -> None:
    with message_store.message_log_lock:
        message_store.message_log.clear()
    with message_store.driver_states_lock:
        message_store.driver_states.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
