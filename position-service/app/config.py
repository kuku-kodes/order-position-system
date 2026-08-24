import os

HOST = os.getenv("POSITION_SERVICE_HOST", "0.0.0.0")
PORT = int(os.getenv("POSITION_SERVICE_PORT", 8000))