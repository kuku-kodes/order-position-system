import httpx

from app.models import OrderEvent
from app.sender import EventSender


def test_sender_returns_false_after_connection_failure(monkeypatch):

    def fake_post(*args, **kwargs):
        raise httpx.ConnectError(
            "connection failed"
        )

    monkeypatch.setattr(
        httpx,
        "post",
        fake_post,
    )

    sender = EventSender(
        service_url="http://localhost:8000",
        max_retries=2,
    )

    event = OrderEvent(
        event_id="failure-1",
        symbol="TCS",
        transaction_type="BUY",
        quantity=10,
    )

    result = sender.send(event)

    assert result is False

def test_sender_does_not_retry_client_error(monkeypatch):

    calls = []

    def fake_post(*args, **kwargs):

        calls.append(1)

        return httpx.Response(
            status_code=400,
            text="invalid event",
        )

    monkeypatch.setattr(
        httpx,
        "post",
        fake_post,
    )

    sender = EventSender(
        service_url="http://localhost:8000",
        max_retries=3,
    )

    event = OrderEvent(
        event_id="bad-1",
        symbol="TCS",
        transaction_type="BUY",
        quantity=10,
    )

    result = sender.send(event)

    assert result is False
    assert len(calls) == 1    