FROM python:3.12-slim

WORKDIR /app

COPY order-service/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY order-service/app ./app
COPY data ./data

CMD ["python", "-m", "app.main"]