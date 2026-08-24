from pydantic import BaseModel, field_validator


class OrderEvent(BaseModel):
    event_id: str
    symbol: str
    transaction_type: str
    quantity: int

    @field_validator("event_id", "symbol")
    @classmethod
    def validate_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be blank")
        return value

    @field_validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, value):
        if value not in {"BUY", "SELL"}:
            raise ValueError("transaction_type must be BUY or SELL")
        return value

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("quantity must be positive")
        return value