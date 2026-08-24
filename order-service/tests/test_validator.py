import pytest

from app.validator import validate_row


def test_blank_event_id():

    with pytest.raises(ValueError):

        validate_row({
            "event_id": "",
            "symbol": "RELIANCE",
            "transaction_type": "BUY",
            "quantity": "10",
        })


def test_blank_symbol():

    with pytest.raises(ValueError):

        validate_row({
            "event_id": "evt-1",
            "symbol": "",
            "transaction_type": "BUY",
            "quantity": "10",
        })


def test_invalid_transaction_type():

    with pytest.raises(ValueError):

        validate_row({
            "event_id": "evt-1",
            "symbol": "RELIANCE",
            "transaction_type": "HOLD",
            "quantity": "10",
        })


@pytest.mark.parametrize(
    "quantity",
    [
        "",
        "0",
        "-10",
        "1.5",
        "abc",
    ],
)
def test_invalid_quantities(quantity):

    with pytest.raises(ValueError):

        validate_row({
            "event_id": "evt-1",
            "symbol": "RELIANCE",
            "transaction_type": "BUY",
            "quantity": quantity,
        })

def test_valid_buy_event():

    event = validate_row({
        "event_id": "evt-1",
        "symbol": "RELIANCE",
        "transaction_type": "BUY",
        "quantity": "90",
    })

    assert event.event_id == "evt-1"
    assert event.symbol == "RELIANCE"
    assert event.transaction_type == "BUY"
    assert event.quantity == 90


def test_valid_sell_event():

    event = validate_row({
        "event_id": "evt-2",
        "symbol": "TCS",
        "transaction_type": "SELL",
        "quantity": "75",
    })

    assert event.transaction_type == "SELL"
    assert event.quantity == 75       