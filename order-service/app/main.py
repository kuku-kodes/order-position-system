import logging

from app.config import (
    INPUT_FILE,
    MAX_EVENTS_PER_SECOND,
    MAX_RETRIES,
    POSITION_SERVICE_URL,
    REQUEST_TIMEOUT,
)
from app.processor import OrderProcessor
from app.rate_limiter import RateLimiter
from app.sender import EventSender


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main():

    sender = EventSender(
        service_url=POSITION_SERVICE_URL,
        timeout=REQUEST_TIMEOUT,
        max_retries=MAX_RETRIES,
    )

    rate_limiter = RateLimiter(
        MAX_EVENTS_PER_SECOND
    )

    processor = OrderProcessor(
        input_file=INPUT_FILE,
        sender=sender,
        rate_limiter=rate_limiter,
    )

    processor.process()


if __name__ == "__main__":
    main()