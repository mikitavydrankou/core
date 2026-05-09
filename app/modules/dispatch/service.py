from shared.message_store import get_driver_states


def list_driver_states() -> list[dict[str, str | float]]:
    return get_driver_states()
