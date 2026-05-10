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


def test_websocket_driver_ack_and_driver_api(client) -> None:
    payload = {
        "type": "driver_location",
        "driverId": "7",
        "lat": 53.91234,
        "lng": 27.55678,
        "status": "online",
    }

    with client.websocket_connect("/ws") as websocket:
        websocket.send_text(json.dumps(payload))
        raw_message = websocket.receive_text()

    ack = json.loads(raw_message)
    assert ack["type"] == "driver_ack"
    assert ack["driverId"] == "7"

    drivers_response = client.get("/api/drivers")
    assert drivers_response.status_code == 200
    drivers = drivers_response.json()
    assert any(driver["driverId"] == "7" for driver in drivers)


def test_websocket_echo_for_non_json_payload(client) -> None:
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("ping")
        message = websocket.receive_text()

    assert message == "Echo: ping"
