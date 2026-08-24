from threading import Lock


class PositionStore:
    def __init__(self):
        self.positions = {}
        self.processed_event_ids = set()
        self.lock = Lock()

    def process_event(self, event):
        with self.lock:

            if event.event_id in self.processed_event_ids:
                return "duplicate"

            self.processed_event_ids.add(event.event_id)

            current = self.positions.get(event.symbol, 0)

            if event.transaction_type == "BUY":
                current += event.quantity
            else:
                current -= event.quantity

            self.positions[event.symbol] = current

            return "accepted"

    def get_positions(self):
        with self.lock:
            return dict(self.positions)