from fastapi import FastAPI

from app.models import OrderEvent
from app.service import get_all_positions, process_order


app = FastAPI(
    title="Position Maintaining Service"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/events")
def receive_event(event: OrderEvent):

    status = process_order(event)

    return {
        "status": status,
        "event_id": event.event_id,
    }


@app.get("/position")
def get_positions():

    return get_all_positions()