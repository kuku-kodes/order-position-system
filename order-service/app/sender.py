import time

import httpx
import logging

from app.models import OrderEvent

logger = logging.getLogger(__name__)

class EventSender:

    def __init__(
        self,
        service_url: str,
        timeout: float = 5,
        max_retries: int = 3,
    ):
        self.service_url = service_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def send(self, event: OrderEvent) -> bool:

        url = f"{self.service_url}/events"

        payload = event.model_dump()

        for attempt in range(1, self.max_retries + 1):

            try:
                response = httpx.post(
                    url,
                    json=payload,
                    timeout=self.timeout,
                )

                if 200 <= response.status_code < 300:
                    return True

                if 400 <= response.status_code < 500:

                    logger.error(
                        "Permanent HTTP error for event_id=%s "
                        "status=%d response=%s",
                        event.event_id,
                        response.status_code,
                        response.text,
                    )

                    return False

                logger.warning(
                    "Server error for event_id=%s "
                    "status=%d attempt=%d",
                    event.event_id,
                    response.status_code,
                    attempt,
                )

            except httpx.RequestError as error:

                logger.warning(
                    "Connection error for event_id=%s "
                    "attempt=%d: %s",
                    event.event_id,
                    attempt,
                    error,
                )

            if attempt < self.max_retries:
                time.sleep(0.5)

        logger.error(
            "Failed to deliver event_id=%s after %d attempts",
            event.event_id,
            self.max_retries,
        )

        return False