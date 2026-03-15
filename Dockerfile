FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn mlflow xgboost numpy pydantic -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "scheduler_api:app", "--host", "0.0.0.0", "--port", "8000"]
