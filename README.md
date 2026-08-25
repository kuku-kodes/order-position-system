# Order Position Processing System

Two-service order processing system that reads order updates from CSV and maintains the current net position for each trading symbol.

## Services

- Order Update Service
- Position Maintaining Service

## Technology

- Python
- FastAPI
- HTTP REST
- Pydantic
- pytest
- Docker
- Docker Compose

## Testing

The project contains unit tests for validation, position calculations, duplicate event handling, CSV processing, rate limiting, and HTTP delivery.

An end-to-end test also starts the Position Maintaining Service and verifies communication over HTTP.

## Running with Docker

Build and start the services:

```bash
docker compose up --build

Run in detached mode:

docker compose up -d --build

Check service status:

docker compose ps

View logs:

docker compose logs

View Position Service logs:

docker compose logs position-service

View Order Service logs:

docker compose logs order-service

Stop the services:

docker compose down

Check the current positions:

curl http://localhost:8000/position

Check service health:

curl http://localhost:8000/health

---

# 5.46 — Add Configuration Documentation

Also add:

```markdown
## Docker Configuration

The Order Update Service uses the following environment variables:

| Variable | Default | Description |
|---|---|---|
| `INPUT_FILE` | `/app/data/order_updates.csv` | Input CSV path |
| `POSITION_SERVICE_URL` | `http://position-service:8000` | Position service address |
| `MAX_EVENTS_PER_SECOND` | `50` | Maximum event sending rate |
| `REQUEST_TIMEOUT` | `5` | HTTP request timeout |
| `MAX_RETRIES` | `3` | Maximum delivery attempts |

The Position Maintaining Service uses:

| Variable | Default | Description |
|---|---|---|
| `POSITION_SERVICE_HOST` | `0.0.0.0` | HTTP bind address |
| `POSITION_SERVICE_PORT` | `8000` | HTTP port |