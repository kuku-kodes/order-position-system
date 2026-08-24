import subprocess
import time

import httpx


def test_end_to_end():

    process = subprocess.Popen(
        [
            "python",
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8001",
        ],
        cwd="position-service",
    )

    try:

        for _ in range(20):

            try:

                response = httpx.get(
                    "http://127.0.0.1:8001/health",
                    timeout=1,
                )

                if response.status_code == 200:
                    break

            except httpx.RequestError:
                time.sleep(0.2)

        response = httpx.post(
            "http://127.0.0.1:8001/events",
            json={
                "event_id": "e2e-1",
                "symbol": "RELIANCE",
                "transaction_type": "BUY",
                "quantity": 100,
            },
        )

        assert response.status_code == 200

        response = httpx.get(
            "http://127.0.0.1:8001/position"
        )

        assert response.status_code == 200
        assert response.json()["RELIANCE"] == 100

    finally:

        process.terminate()
        process.wait()