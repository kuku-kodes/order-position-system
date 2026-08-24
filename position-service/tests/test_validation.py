import pytest
from app.models import OrderEvent


def test_invalid_transaction_type():

    with pytest.raises(ValueError):

        OrderEvent(
            event_id="1",
            symbol="ABC",
            transaction_type="HOLD",
            quantity=10,
        )


def test_zero_quantity():

    with pytest.raises(ValueError):

        OrderEvent(
            event_id="1",
            symbol="ABC",
            transaction_type="BUY",
            quantity=0,
        )


def test_blank_symbol():

    with pytest.raises(ValueError):

        OrderEvent(
            event_id="1",
            symbol="",
            transaction_type="BUY",
            quantity=10,
        )