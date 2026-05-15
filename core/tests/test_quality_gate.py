import json


def test_core_pages_are_available(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["simulator"] == "/sim"
    assert body["dispatcher"] == "/dispatch"
    assert body["logs"] == "/monitor"

    for path in ("/sim", "/dispatch", "/monitor"):
        page_response = client.get(path)
        assert page_response.status_code == 200
        assert "text/html" in page_response.headers.get("content-type", "")


def test_websocket_driver_ack_and_broadcast(client) -> None:
    payload = {
        "type": "driver_location",
        "driverId": "7",
        "lat": 53.91234,
        "lng": 27.55678,
        "status": "online",
    }

    with client.websocket_connect("/ws") as listener:
        with client.websocket_connect("/ws") as sender:
            sender.send_text(json.dumps(payload))
            raw_message = sender.receive_text()

            ack = json.loads(raw_message)
            assert ack["type"] == "driver_ack"
            assert ack["driverId"] == "7"

            broadcast_message = listener.receive_text()
            broadcast = json.loads(broadcast_message)
            assert broadcast["type"] == "driver_location"
            assert broadcast["driverId"] == "7"


def test_websocket_echo_for_non_json_payload(client) -> None:
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("ping")
        message = websocket.receive_text()

    assert message == "Echo: ping"
