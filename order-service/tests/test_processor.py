from app.processor import OrderProcessor


class FakeSender:

    def __init__(self):
        self.events = []

    def send(self, event):
        self.events.append(event)
        return True


class FakeRateLimiter:

    def wait(self):
        pass


def test_processor_continues_after_invalid_row(tmp_path):

    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "event_id,symbol,transaction_type,quantity\n"
        "evt-001,RELIANCE,BUY,100\n"
        "evt-002,TCS,INVALID,50\n"
        "evt-003,TCS,BUY,50\n"
    )

    sender = FakeSender()
    limiter = FakeRateLimiter()

    processor = OrderProcessor(
        input_file=str(csv_file),
        sender=sender,
        rate_limiter=limiter,
    )

    processor.process()

    assert len(sender.events) == 2

    assert sender.events[0].event_id == "evt-001"
    assert sender.events[1].event_id == "evt-003"

def test_events_are_sent_in_csv_order(tmp_path):

    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "event_id,symbol,transaction_type,quantity\n"
        "evt-001,A,BUY,10\n"
        "evt-002,B,SELL,20\n"
        "evt-003,C,BUY,30\n"
    )

    sender = FakeSender()
    limiter = FakeRateLimiter()

    processor = OrderProcessor(
        input_file=str(csv_file),
        sender=sender,
        rate_limiter=limiter,
    )

    processor.process()

    event_ids = [
        event.event_id
        for event in sender.events
    ]

    assert event_ids == [
        "evt-001",
        "evt-002",
        "evt-003",
    ]    