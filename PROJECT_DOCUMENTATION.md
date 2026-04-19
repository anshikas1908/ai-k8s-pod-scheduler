# AI K8s Pod Scheduler — Comprehensive Project Documentation

This document serves as the complete technical specification, architectural overview, and workflow guide for the **AI Kubernetes Pod Scheduler** project.

---

## 1. Executive Summary
The AI K8s Pod Scheduler is a machine-learning-driven alternative to the default Kubernetes scheduler. Instead of relying solely on arithmetic resource thresholds, it utilizes an XGBoost Classifier trained on 10,000 synthesized node-state scenarios. It intelligently evaluates the non-linear relationship between a Node's current utilization and an incoming Pod's requested resources to determine safety and fit.

## 2. Project Architecture & Flow

The system operates across four primary distinct layers:

### A. Data Generation Layer (`generate_scheduler_data.py`)
Because live K8s clusters are difficult to predictably stress-test, this file acts as a state engine. 
*   **What it does:** Generates 10,000 highly varied edge cases mimicking real Kubernetes spikes, noisy sensors, and varying Pod requests.
*   **Features generated:** `node_cpu_cores`, `node_cpu_percent`, `node_memory_mb`, `node_memory_percent`, `pod_req_cpu`, `pod_req_mem`.
*   **Target Label:** Computes an `is_schedulable` label (1 = Safe, 0 = Overload) by calculating if the Pod footprint fits securely inside the Node's remaining 85% capacity buffer.

### B. Machine Learning Engine (`train_real_model.py`)
*   **What it does:** Consumes `k8s_metrics_v2.csv` and trains an XGBoost Decision Tree algorithm to recognize scheduling patterns.
*   **Tools:** `scikit-learn` for train/test splits, `xgboost` for the algorithm, `mlflow` for tracking experiment parameters and metrics natively.
*   **Output:** Exports a highly optimized `model.pkl` file containing the frozen decision tree weights.

### C. The API Backend (`scheduler_api.py`)
*   **What it does:** A lightweight `FastAPI` application acting as the bridge between Kubernetes and the ML Model. 
*   **Security:** Leverages Pydantic `BaseModel` to fiercely enforce data types. If a payload is missing `pod_req_cpu`, the API rejects it automatically before it hits the model.
*   **Optimization:** Uses `GzipMiddleware` to compress JSON responses, reducing network overhead in high-traffic clusters.
*   **Endpoints:**
    *   `POST /predict`: Ingests K8s telemetry, formats it as a Pandas DataFrame, and returns the AI's binary decision.
    *   `GET /health`: The Kubernetes Liveness/Readiness probe hook for automatic container recovery.
    *   `GET /stats`: Returns statistical metadata for the frontend.

### D. The Interactive Dashboard (`static/dashboard.html`)
*   **What it does:** A high-fidelity Single Page Application (SPA) providing visual analytics.
*   **Tech:** Pure HTML/Vanilla JS/CSS. (No heavy React/Vue overhead). Includes smooth DOM manipulations, interactive sliders, Chart.js analytics, and real-time prediction history logs.

---

## 3. DevOps & Deployment Strategy

The project is designed to be shipped natively into Kubernetes.

*   `Dockerfile`: Uses a slim Python 3.10 image. It strictly installs dependencies via `requirements.txt` and exposes port `8000`.
*   `k8s-scheduler.yaml`: Defines exactly how the system runs in the cloud.
    *   **Deployment:** Generates a Pod running the Docker container.
    *   **Resource Quotas:** Explicitly limits memory (512Mi) and CPU (500m) to ensure the AI doesn't consume the cluster it is trying to manage.
    *   **Health Probes:** Connects Kubernetes directly to the `/health` API endpoint. If Uvicorn crashes, Kubernetes instantly restarts the pod.

---

## 4. Development & Testing Workflow

### How to Edit the AI Model:
1. Tweak logic inside `generate_scheduler_data.py` (e.g., allow bigger Pods).
2. Run `python generate_scheduler_data.py`.
3. Run `python train_real_model.py`.
4. Restart your FastAPI server.

### Automated Testing (`test_scheduler_api.py`):
We use `pytest` to guarantee system stability without clicking buttons in a browser. Run `pytest -v` to shoot dummy payloads at the logic functions to mathematically prove that large pods get rejected and small pods get accepted.

---

## 5. 🛡️ Risk Analysis & Mitigation (Viva Prep)

This section covers the core stability and reliability considerations:

### 1. Model Reliability & Drift
*   **Risk:** The ML model might become inaccurate as K8s cluster behavior changes over months.
*   **Mitigation:** We integrated **MLflow** for experiment tracking. This allows us to log every training run and compare versions. If accuracy drops, we can trigger an automated retraining pipeline on the latest telemetry.

### 2. Service Resilience (High Availability)
*   **Risk:** What happens if the Scheduler API crashes?
*   **Mitigation:** We use **Kubernetes Liveness and Readiness Probes**. K8s constantly pings `/health`. If it fails, K8s kills the container and starts a fresh one immediately. By using `replicas: 1` (scalable to more), we ensure the system is monitored by the orchestrator.

### 3. Data Integrity & Security
*   **Risk:** Malicious or broken JSON data could crash the inference engine.
*   **Mitigation:** We used **FastAPI + Pydantic**. Every incoming request is strictly validated against a schema. If a feature is missing or is the wrong type (e.g., string instead of float), the API blocks the request before it even touches the ML model.

---

## 6. 🏎️ Optimization & Scalability (Viva Prep)

Professional-grade optimizations implemented in the project:

### 1. Computational Optimization
*   **XGBoost vs. Deep Learning:** We purposefully chose XGBoost over Neural Networks. XGBoost is significantly more **computationally efficient** for tabular data. It requires less RAM and CPU power, which directly reduces the "Cost per Inference" in a cloud environment.

### 2. Network Optimization
*   **Gzip Compression:** We implemented **GzipMiddleware** in our FastAPI app. This compresses the JSON responses sent to the dashboard. In a cluster with thousands of nodes, this significantly reduces network congestion and latency.

### 3. Horizontal Scaling
*   **Stateless Architecture:** Our API is **stateless** (it doesn't save user data locally). This means we can scale from 1 container to 100 containers instantly using a Kubernetes Deployment, and a Load Balancer will distribute the scheduling requests evenly.

---

## 7. Future Expansion

1. **Real-world Webhook Integration:** Configure Kubernetes `MutatingAdmissionWebhooks` to intercept every `kubectl apply` and consult the AI before scheduling.
2. **Database Logging:** Connect a PostgreSQL database via `SQLAlchemy` to store a persistent log of every scheduling decision.
3. **Time-Series Prediction:** Swap XGBoost with an LSTM (Long Short-Term Memory Neural Network) to predict future node loads based on historical trends.
