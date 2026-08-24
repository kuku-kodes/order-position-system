import logging

from app.csv_reader import read_csv_rows
from app.rate_limiter import RateLimiter
from app.sender import EventSender
from app.validator import validate_row


logger = logging.getLogger(__name__)


class OrderProcessor:

    def __init__(
        self,
        input_file: str,
        sender: EventSender,
        rate_limiter: RateLimiter,
    ):
        self.input_file = input_file
        self.sender = sender
        self.rate_limiter = rate_limiter

    def process(self):

        accepted = 0
        rejected = 0
        sent = 0

        logger.info(
            "Starting input processing: %s",
            self.input_file,
        )

        for row_number, row in enumerate(
            read_csv_rows(self.input_file),
            start=2,
        ):

            try:
                event = validate_row(row)

                accepted += 1

                logger.info(
                    "Accepted event_id=%s symbol=%s",
                    event.event_id,
                    event.symbol,
                )

            except ValueError as error:

                rejected += 1

                logger.warning(
                    "Rejected row=%d reason=%s",
                    row_number,
                    error,
                )

                continue

            self.rate_limiter.wait()

            success = self.sender.send(event)

            if success:

                sent += 1

                logger.info(
                    "Successfully sent event_id=%s",
                    event.event_id,
                )

            else:

                logger.error(
                    "Failed to send event_id=%s",
                    event.event_id,
                )

        logger.info(
            "Input processing complete: "
            "accepted=%d rejected=%d sent=%d",
            accepted,
            rejected,
            sent,
        )