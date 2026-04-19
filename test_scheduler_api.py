import pytest
from fastapi.testclient import TestClient
from scheduler_api import app

client = TestClient(app)

def test_health_endpoint():
    """Verify the Kubernetes liveness probe functions correctly."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "AI Scheduler API is running!"}

def test_predict_good_fit():
    """Verify the XGBoost model approves a small pod on an idle node."""
    payload = {
        "node_cpu_cores": 250.0,
        "node_cpu_percent": 5.0,
        "node_memory_mb": 1024.0,
        "node_memory_percent": 12.0,
        "pod_req_cpu": 100.0,
        "pod_req_mem": 256.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["node_status"] == "LOW_LOAD"
    assert data["schedule_here"] is True

def test_predict_overload():
    """Verify the XGBoost model blocks a massive pod trying to land on a near-cap node."""
    payload = {
        "node_cpu_cores": 3000.0,
        "node_cpu_percent": 80.0,
        "node_memory_mb": 6000.0,
        "node_memory_percent": 75.0,
        "pod_req_cpu": 2500.0,  # Huge pod should trigger a rejection
        "pod_req_mem": 4096.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["node_status"] == "HIGH_LOAD"
    assert data["schedule_here"] is False

def test_predict_invalid_payload():
    """Verify Pydantic validation fails when required features are missing."""
    payload = {
        "node_cpu_cores": 3000.0
        # Missing other 5 variables
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
