from app.store import PositionStore
from app.models import OrderEvent


def test_duplicate_event_ignored():

    store = PositionStore()

    event = OrderEvent(
        event_id="dup",
        symbol="ABC",
        transaction_type="BUY",
        quantity=100,
    )

    store.process_event(event)
    store.process_event(event)

    assert store.get_positions()["ABC"] == 100