# Order Position Processing System

A small two-service system for processing order updates from a CSV file and maintaining the current net position for each trading symbol.

The system consists of:

- **Order Update Service** — reads and validates CSV events incrementally, throttles delivery, and sends valid events to the Position Maintaining Service.
- **Position Maintaining Service** — receives order events, handles event idempotency, maintains in-memory positions, and exposes the current positions through an HTTP API.

The solution focuses on correctness, validation, idempotency, testability, and simple service-to-service communication.

## Architecture

```text
                    order_updates.csv
                           |
                           v
                +----------------------+
                | Order Update Service |
                |----------------------|
                | CSV Reader           |
                | Validation           |
                | Rate Limiter         |
                | HTTP Client          |
                +----------+-----------+
                           |
                           | HTTP POST /events
                           v
                +----------------------+
                | Position Service     |
                |----------------------|
                | Event Validation     |
                | Idempotency Set      |
                | Position Store       |
                | Thread-safe Updates  |
                +----------+-----------+
                           |
                           v
                    GET /position

## Technology Choices

### Python

Python was selected because the assessment explicitly prefers Python or Rust, and Python provides a concise implementation for CSV streaming, HTTP services, validation, and automated testing.

The implementation uses:

- Python
- FastAPI
- Pydantic
- HTTPX
- pytest
- Docker
- Docker Compose                    

### Why HTTP instead of gRPC?

HTTP REST was selected for communication between the two services.

The communication pattern is simple request/response:

```text
Order Update Service
        |
        | POST /events
        v
Position Maintaining Service

## Services

### Order Update Service

Responsibilities:

1. Read the input CSV incrementally.
2. Validate each row.
3. Convert valid rows into order events.
4. Preserve CSV order.
5. Send valid events to the Position Maintaining Service.
6. Limit delivery to no more than 50 events per second.
7. Log accepted, rejected, sent, and failed events.
8. Continue processing after invalid rows.

### Position Maintaining Service

Responsibilities:

1. Receive order events.
2. Validate the event contract.
3. Ignore duplicate event IDs.
4. Apply BUY and SELL operations.
5. Maintain positions in memory.
6. Keep zero positions for symbols that have been seen.
7. Provide `GET /position`.
8. Keep API reads and updates thread-safe.

## Event Contract

Each order event contains:

| Field | Type | Rules |
|---|---|---|
| `event_id` | string | Non-empty and uniquely identifies the event |
| `symbol` | string | Non-empty; supplied case/value is preserved |
| `transaction_type` | string | Exactly `BUY` or `SELL` |
| `quantity` | integer | Must be positive |

Example:

```json
{
  "event_id": "evt-0001",
  "symbol": "RELIANCE",
  "transaction_type": "BUY",
  "quantity": 90
}

## CSV Processing

The Order Update Service reads the CSV using Python's streaming CSV reader.

Rows are processed one at a time rather than loading the complete file into memory.

Conceptually:

```text
read row
   |
   v
validate
   |
   +---- invalid ----> log and continue
   |
   v
create event
   |
   v
send event

## Validation

Invalid rows are logged and skipped without stopping subsequent processing.

Examples of rejected input include:

- Blank event IDs
- Blank symbols
- Invalid transaction types
- Zero quantity
- Negative quantity
- Non-integer quantity
- Blank quantity

For HTTP requests, invalid event payloads are rejected by the Position Maintaining Service validation layer.

## Idempotency

The Position Maintaining Service maintains an in-memory set of processed event IDs.

When an event is received:

```text
event_id already processed?
       |
   +---+---+
   |       |
  yes      no
   |       |
ignore    process
           |
      record event ID

## Position Calculation

For each accepted event:

- `BUY` increases the position by `quantity`.
- `SELL` decreases the position by `quantity`.

Example:

```text
RELIANCE BUY 100
RELIANCE SELL 40

Final position:
RELIANCE = 60

## Concurrency

The position state is protected by a lock.

Both position updates and reads acquire the same lock, ensuring that concurrent API reads do not observe an inconsistent state while an event is being applied.

The store returns a copy of the current positions rather than exposing the internal mutable dictionary directly.

## Rate Limiting

The Order Update Service limits event delivery to a configurable maximum rate.

Default:

```text
MAX_EVENTS_PER_SECOND=50

## Error Handling

### Invalid CSV rows

Invalid rows are logged and skipped. Processing continues with subsequent rows.

### Position Service unavailable

The Order Update Service attempts delivery multiple times for connection/server failures.

The retry count is configurable using:

```text
MAX_RETRIES

## Delivery and Persistence Limitations

This implementation does not provide durable delivery.

Events are sent directly over HTTP from the Order Update Service to the Position Maintaining Service.

If the Position Maintaining Service is unavailable, the Order Update Service retries delivery according to its configured retry limit. Events that still cannot be delivered are logged and skipped.

The Position Maintaining Service stores positions and processed event IDs only in memory.

Therefore:

- State is lost when the Position Maintaining Service restarts.
- Processed event IDs are lost after restart.
- There is no persistent event queue.
- There is no exactly-once guarantee across process restarts.

These limitations are intentional because durable delivery, persistence, and recovery after a complete restart are outside the scope of the assessment.

## API

### GET /health

Checks whether the Position Maintaining Service is available.

Example:

```bash
curl http://localhost:8000/health

## Configuration

### Order Update Service

| Variable | Default | Description |
|---|---|---|
| `INPUT_FILE` | `../data/order_updates.csv` locally | CSV input path |
| `POSITION_SERVICE_URL` | `http://127.0.0.1:8000` locally | Position service URL |
| `MAX_EVENTS_PER_SECOND` | `50` | Maximum event delivery rate |
| `REQUEST_TIMEOUT` | `5` | HTTP request timeout in seconds |
| `MAX_RETRIES` | `3` | Maximum delivery attempts |

### Position Maintaining Service

| Variable | Default | Description |
|---|---|---|
| `POSITION_SERVICE_HOST` | `0.0.0.0` | HTTP bind address |
| `POSITION_SERVICE_PORT` | `8000` | HTTP port |

## Running Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd order-position-system

### 2. Start the Position Maintaining Service

cd position-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --host 127.0.0.1 --port 8000

### 3. Start the Order Update Service

cd order-position-system/order-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m app.main

## Running with Docker Compose

Build and start:

```bash
docker compose up --build

docker compose up -d --build

Check status:

docker compose ps

View logs:

docker compose logs

View individual service logs:

docker compose logs order-service
docker compose logs position-service

Check positions:

curl http://localhost:8000/position

Check health:

curl http://localhost:8000/health

Stop:

docker compose down

### Docker Networking

When running through Docker Compose, the Order Update Service communicates with the Position Maintaining Service using:

```text
http://position-service:8000

## Testing

The project includes unit, API, integration, and end-to-end tests.

### Order Update Service

```bash
cd order-service
source .venv/bin/activate
pytest

## Project Structure

```text
order-position-system/
├── data/
│   └── order_updates.csv
│
├── order-service/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── position-service/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── tests/
│   └── test_e2e.py
│
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md

## Design Trade-offs

### HTTP instead of gRPC

HTTP provides sufficient functionality for the simple request/response communication pattern while keeping the implementation easy to inspect and test.

### In-memory state

An in-memory store keeps the implementation small and matches the assessment scope, which explicitly excludes persistence.

### Direct HTTP delivery

Direct HTTP communication avoids introducing a broker when durable messaging is not required.

### Simple rate limiter

A configurable time-based throttle is sufficient because precise sub-millisecond scheduling is not required.

### In-memory idempotency

A set of processed event IDs provides simple idempotency during a service lifetime. The state is intentionally not persisted across restarts.

## Out of Scope

The following were intentionally not implemented:

- Database persistence
- Authentication/authorization
- Frontend/dashboard
- Cloud deployment
- Kubernetes/distributed orchestration
- Production monitoring
- Exactly-once delivery across restarts
- Durable message broker

## AI Assistance

AI-assisted development tools were used during the implementation for guidance, code review, debugging assistance, and discussion of design alternatives.

All submitted code was reviewed, tested, and adapted as part of the implementation. I am able to explain the architecture, implementation choices, testing strategy, and trade-offs in the submitted solution.

## Known Limitations

1. Position state is stored only in memory.
2. Processed event IDs are lost when the Position Maintaining Service restarts.
3. Events that cannot be delivered after the configured retry attempts are logged and skipped.
4. There is no durable message queue.
5. There is no cross-restart exactly-once delivery guarantee.
6. The Order Update Service is a batch processor and exits after the CSV has been fully processed.

## Assessment Scope

The implementation intentionally favors correctness, readability, automated testing, and simple service communication over unnecessary infrastructure or abstractions.