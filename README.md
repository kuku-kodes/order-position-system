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