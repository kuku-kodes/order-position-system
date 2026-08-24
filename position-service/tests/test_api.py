from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_position_endpoint():

    response = client.post(
        "/events",
        json={
            "event_id": "api-1",
            "symbol": "TCS",
            "transaction_type": "BUY",
            "quantity": 50,
        },
    )

    assert response.status_code == 200

    response = client.get("/position")

    assert response.status_code == 200
    assert response.json()["TCS"] == 50

def test_invalid_transaction_type():

    response = client.post(
        "/events",
        json={
            "event_id": "invalid-1",
            "symbol": "TCS",
            "transaction_type": "HOLD",
            "quantity": 50,
        },
    )

    assert response.status_code == 422

def test_zero_quantity():

    response = client.post(
        "/events",
        json={
            "event_id": "invalid-2",
            "symbol": "TCS",
            "transaction_type": "BUY",
            "quantity": 0,
        },
    )

    assert response.status_code == 422

def test_blank_event_id():

    response = client.post(
        "/events",
        json={
            "event_id": "",
            "symbol": "TCS",
            "transaction_type": "BUY",
            "quantity": 50,
        },
    )

    assert response.status_code == 422

def test_blank_symbol():

    response = client.post(
        "/events",
        json={
            "event_id": "invalid-3",
            "symbol": "",
            "transaction_type": "BUY",
            "quantity": 50,
        },
    )

    assert response.status_code == 422     

def test_duplicate_event_is_ignored():

    event = {
        "event_id": "duplicate-api-1",
        "symbol": "RELIANCE",
        "transaction_type": "BUY",
        "quantity": 100,
    }

    first_response = client.post(
        "/events",
        json=event,
    )

    second_response = client.post(
        "/events",
        json={
            "event_id": "duplicate-api-1",
            "symbol": "RELIANCE",
            "transaction_type": "SELL",
            "quantity": 500,
        },
    )

    assert first_response.json()["status"] == "accepted"

    assert second_response.json()["status"] == "duplicate"    

def test_first_valid_event_wins():

    first = client.post(
        "/events",
        json={
            "event_id": "first-wins",
            "symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": 100,
        },
    )

    second = client.post(
        "/events",
        json={
            "event_id": "first-wins",
            "symbol": "INFY",
            "transaction_type": "SELL",
            "quantity": 500,
        },
    )

    assert first.json()["status"] == "accepted"
    assert second.json()["status"] == "duplicate"

def test_negative_position():

    client.post(
        "/events",
        json={
            "event_id": "negative-1",
            "symbol": "HDFC",
            "transaction_type": "SELL",
            "quantity": 100,
        },
    )

    client.post(
        "/events",
        json={
            "event_id": "negative-2",
            "symbol": "HDFC",
            "transaction_type": "BUY",
            "quantity": 20,
        },
    )

    response = client.get("/position")

    assert response.json()["HDFC"] == -80

def test_zero_position_is_kept():

    client.post(
        "/events",
        json={
            "event_id": "zero-1",
            "symbol": "WIPRO",
            "transaction_type": "BUY",
            "quantity": 100,
        },
    )

    client.post(
        "/events",
        json={
            "event_id": "zero-2",
            "symbol": "WIPRO",
            "transaction_type": "SELL",
            "quantity": 100,
        },
    )

    response = client.get("/position")

    positions = response.json()

    assert "WIPRO" in positions
    assert positions["WIPRO"] == 0               