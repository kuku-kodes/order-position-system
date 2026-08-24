from app.store import PositionStore
from app.models import OrderEvent


def test_buy_increases_position():
    store = PositionStore()

    event = OrderEvent(
        event_id="1",
        symbol="ABC",
        transaction_type="BUY",
        quantity=100,
    )

    store.process_event(event)

    assert store.get_positions()["ABC"] == 100


def test_sell_decreases_position():
    store = PositionStore()

    store.process_event(
        OrderEvent(
            event_id="1",
            symbol="ABC",
            transaction_type="BUY",
            quantity=100,
        )
    )

    store.process_event(
        OrderEvent(
            event_id="2",
            symbol="ABC",
            transaction_type="SELL",
            quantity=40,
        )
    )

    assert store.get_positions()["ABC"] == 60