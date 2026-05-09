from shared.message_store import get_messages


def list_messages() -> list[dict[str, str]]:
    return get_messages()
