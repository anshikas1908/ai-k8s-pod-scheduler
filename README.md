🚀 AI K8s Pod Scheduler

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An intelligent, machine-learning-powered Kubernetes Pod Scheduling Assistant. This project replaces simple threshold guessing with an **XGBoost Classifier** to accurately predict node load and recommend optimal pod placement by evaluating both live node telemetry and incoming pod constraints.

🌟 Overview

The default Kubernetes `kube-scheduler` makes placement decisions purely based on raw requested resources. This AI Scheduler goes a step further by evaluating the complex non-linear relationship between a Node's capacity and an incoming Pod's footprint. Trained on **10,000 synthesized K8s node state samples**, the AI Engine accurately predicts whether a specific Pod can safely reside on a Node without causing an overload.

With a highly validated accuracy of **~96%**, this system serves as a robust intelligent decision engine for dynamic pod scheduling.

# ⚡ Key Features

*   **🧠 XGBoost ML Engine:** Trained on 10,000 realistic stress-tested metric profiles spanning 6 distinct variables.
*   **🖥️ Production SPA Dashboard:** A stunning, animated Single Page Application (SPA) with multi-page navigation built dynamically to visualize pod requirements and node constraints.
*   **📡 RESTful API Wrapper:** A FastAPI backend with standard Pydantic schema validation.
*   **🩺 K8s Probes:** Integrated Liveness and Readiness Kubernetes probes via the `/health` endpoint.
*   **🐳 Container Ready:** Fully configured `Dockerfile` and `k8s-scheduler.yaml` for instant cluster deployment.

---

## 🏗️ System Architecture

```text
                                  Pod Constraints
                                      (CPU/Mem)
                                          ↓
☸️ K8s Cluster (Node Metrics) → ⚡ FastAPI Webhook → 🖥️ Dashboard
                                          ↓
                              🧠 XGBoost Pipeline (MLflow)
                                          ↓
                             ✅ ❌ Scheduling Decision
```

### Technology Stack
*   **Backend:** Python 3.10, FastAPI, Uvicorn, pytest
*   **Machine Learning:** XGBoost, scikit-learn, Pandas, Joblib, MLflow
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla SPA)
*   **Deployment:** Docker, Kubernetes

---

## 🚀 Getting Started (Local Demo)

You can run the full AI scheduling engine right on your laptop without needing to spin up a Kubernetes cluster.

### 1. Prerequisites
Ensure you have Python 3.10+ installed and create a virtual environment.

```powershell
# Create and activate virtual environment (Windows)
python -m venv auth
.\auth\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
pip install pytest httpx
```

### 3. Start the Server
Run the FastAPI Uvicorn server locally.

```powershell
uvicorn scheduler_api:app --host 0.0.0.0 --port 8000
```

### 4. Open the Dashboard
Navigate to your browser:
**➡️ http://localhost:8000/**

---

## 📡 API Endpoints

The system exposes programmatic REST APIs for Kubernetes to interact with:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/predict` | Submit Node telemetry and incoming Pod constraints to receive a prediction. |
| `GET` | `/stats` | Returns underlying ML training dataset statistics. |
| `GET` | `/health` | Kubernetes Liveness & Readiness probe check. |

**Example `POST /predict` Request:**
```json
{
  "node_cpu_cores": 2250.0,
  "node_cpu_percent": 50.0,
  "node_memory_mb": 620.0,
  "node_memory_percent": 10.0,
  "pod_req_cpu": 500.0,
  "pod_req_mem": 256.0
}
```

**Response:**
```json
{
  "node_status": "LOW_LOAD",
  "schedule_here": true,
  "features_received": {
    "node_cpu_cores": 2250.0,
    "node_cpu_percent": 50.0,
    "node_memory_mb": 620.0,
    "node_memory_percent": 10.0,
    "pod_req_cpu": 500.0,
    "pod_req_mem": 256.0
  }
}
```

---

## 📊 Model Performance

*   **Algorithm:** XGBoost Classifier
*   **Dataset Size:** 10,000 synthesized samples
*   **Validation Accuracy:** ~96.2%
*   **Target:** Binary Classification (1 = Schedulable, 0 = Do Not Schedule)

## 👨‍💻 Author
**Anshika** (Project Lead & Developer)
