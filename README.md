🚀 AI K8s Pod Scheduler

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An intelligent, machine-learning-powered Kubernetes Pod Scheduling Assistant. This project replaces simple threshold guessing with an **XGBoost Classifier** to accurately predict node load and recommend optimal pod placement.

🌟 Overview

The default Kubernetes `kube-scheduler` makes placement decisions based on requested resources, but it often struggles to predict complex real-world load patterns. This AI Scheduler solves that by analyzing a dataset of **1,053 real-world K8s node metrics** (including noisy edge cases) to determine if a node is experiencing **HIGH LOAD** or **LOW LOAD**.

With a hardened accuracy of **99.05%**, this system serves as a robust intelligent decision engine for dynamic pod scheduling.

# ⚡ Key Features

*   **🧠 XGBoost ML Engine:** Trained on thousands of realistic edge-case metrics (CPU Cores, CPU %, Memory MB, Memory %).
*   **🖥️ Production SPA Dashboard:** A stunning, animated Single Page Application (SPA) with multi-page navigation built in pure HTML/CSS/JS (no heavy framework overhead).
*   **📡 RESTful API Wrapper:** A FastAPI backend that safely exposes the ML model to Kubernetes components.
*   **📈 Real-time Analytics:** View feature importance, class distribution, and a running history of predictions dynamically.
*   **🐳 Container Ready:** Fully configured `Dockerfile` and `k8s-scheduler.yaml` for instant cluster deployment.

---

## 🏗️ System Architecture

```text
☸️ K8s Cluster (kubectl top nodes)
      ↓
📊 Metrics CSV (1,053 samples)
      ↓
🧠 XGBoost Pipeline (MLflow tracked)
      ↓
⚡ FastAPI (REST API Server)
      ↓
🖥️ Dashboard (Interactive Client Browser)
```

### Technology Stack
*   **Backend:** Python 3.10, FastAPI, Uvicorn
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
| `POST` | `/predict` | Submit JSON node metrics (CPU/Mem) to receive a scheduling recommendation. |
| `GET` | `/stats` | Returns underlying training dataset statistics. |
| `GET` | `/health` | Kubernetes Liveness & Readiness probe check. |

**Example `POST /predict` Request:**
```json
{
  "cpu_cores": 250,
  "cpu_percent": 5.0,
  "memory_mb": 620,
  "memory_percent": 5.0
}
```

**Response:**
```json
{
  "node_status": "LOW_LOAD",
  "schedule_here": true,
  "message": "✅ CLASS 0: LOW LOAD. Recommended for Pod Scheduling."
}
```

---

## 📊 Model Performance

*   **Algorithm:** XGBoost Classifier
*   **Dataset:** 1,053 Node Samples
*   **Accuracy:** 99.05%
*   **Top Feature Weight:** `cpu_cores` (85.1%)

## 👨‍💻 Author
**Anshika** (Project Lead & Developer)
