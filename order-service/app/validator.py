from pydantic import ValidationError

from app.models import OrderEvent


def validate_row(row: dict) -> OrderEvent:
    event_id = row.get("event_id", "")
    symbol = row.get("symbol", "")
    transaction_type = row.get("transaction_type", "")
    quantity = row.get("quantity", "")

    if not isinstance(event_id, str) or not event_id.strip():
        raise ValueError("event_id must be a non-empty string")

    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("symbol must be a non-empty string")

    if transaction_type not in {"BUY", "SELL"}:
        raise ValueError(
            "transaction_type must be exactly BUY or SELL"
        )

    if not isinstance(quantity, str) or not quantity.strip():
        raise ValueError("quantity must be a positive integer")

    quantity = quantity.strip()

    try:
        quantity_int = int(quantity)
    except ValueError:
        raise ValueError(
            "quantity must be a positive integer"
        )

    if quantity_int <= 0:
        raise ValueError(
            "quantity must be a positive integer"
        )

    return OrderEvent(
        event_id=event_id,
        symbol=symbol,
        transaction_type=transaction_type,
        quantity=quantity_int,
    )