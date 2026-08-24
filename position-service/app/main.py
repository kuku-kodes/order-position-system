from fastapi import FastAPI
from app.models import OrderEvent
from app.service import process_order, get_all_positions

app = FastAPI(title="Position Maintaining Service")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/events")
def receive_event(event: OrderEvent):

    status = process_order(event)

    return {"status": status}


@app.get("/position")
def get_positions():

    return get_all_positions()