from pydantic import BaseModel


class OrderEvent(BaseModel):
    event_id: str
    symbol: str
    transaction_type: str
    quantity: int