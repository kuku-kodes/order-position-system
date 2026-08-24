from app.store import PositionStore

store = PositionStore()


def process_order(event):
    return store.process_event(event)


def get_all_positions():
    return store.get_positions()