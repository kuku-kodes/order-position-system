import time

import httpx

from app.models import OrderEvent


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
                    print(
                        f"ERROR failed to send "
                        f"event_id={event.event_id}: {error}"
                    )

                    return False

                print(
                    f"WARNING retrying event_id="
                    f"{event.event_id}, "
                    f"attempt={attempt}"
                )

                time.sleep(0.5)

        return False