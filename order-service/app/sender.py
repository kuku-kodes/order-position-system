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

                response.raise_for_status()

                return True

            except httpx.HTTPError as error:

                if attempt == self.max_retries:
                    # print(
                    #     f"ERROR failed to send "
                    #     f"event_id={event.event_id}: {error}"
                    # )
                    logger.error(
                            "Failed to send event_id=%s: %s",
                            event.event_id,
                            error,
                        )

                    return False

                # print(
                #     f"WARNING retrying event_id="
                #     f"{event.event_id}, "
                #     f"attempt={attempt}"
                # )
                logger.warning(
                            "Retrying event_id=%s attempt=%d",
                            event.event_id,
                            attempt,
                        )

                time.sleep(0.5)

        return False