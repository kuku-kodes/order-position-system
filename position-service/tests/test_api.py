from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_position_endpoint():

    client.post(
        "/events",
        json={
            "event_id": "api-1",
            "symbol": "TCS",
            "transaction_type": "BUY",
            "quantity": 50,
        },
    )

    response = client.get("/position")

    assert response.status_code == 200
    assert response.json()["TCS"] == 50