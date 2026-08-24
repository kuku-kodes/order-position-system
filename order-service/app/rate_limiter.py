import time


class RateLimiter:

    def __init__(self, max_events_per_second: int):
        if max_events_per_second <= 0:
            raise ValueError(
                "max_events_per_second must be positive"
            )

        self.interval = 1.0 / max_events_per_second
        self.last_sent_at = None

    def wait(self):
        now = time.monotonic()

        if self.last_sent_at is not None:

            elapsed = now - self.last_sent_at
            remaining = self.interval - elapsed

            if remaining > 0:
                time.sleep(remaining)

        self.last_sent_at = time.monotonic()