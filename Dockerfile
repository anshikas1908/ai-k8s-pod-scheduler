FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# We only install the locked requirements.txt directly instead of unpinned extra libraries
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000 for FastAPI + Gradio combined
EXPOSE 8000

# Run the unified REST API and visual GUI
CMD ["sh", "-c", "uvicorn scheduler_api:app --host 0.0.0.0 --port ${PORT:-8000}"]
