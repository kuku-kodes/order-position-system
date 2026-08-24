import os

INPUT_FILE = os.getenv(
    "INPUT_FILE",
    "../data/order_updates.csv",
)

POSITION_SERVICE_URL = os.getenv(
    "POSITION_SERVICE_URL",
    "http://127.0.0.1:8000",
)

MAX_EVENTS_PER_SECOND = int(
    os.getenv("MAX_EVENTS_PER_SECOND", "50")
)

REQUEST_TIMEOUT = float(
    os.getenv("REQUEST_TIMEOUT", "5")
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "3")
)