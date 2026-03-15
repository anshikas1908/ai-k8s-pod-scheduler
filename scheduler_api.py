from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.xgboost
import numpy as np

RUN_ID = "2ced8893b6594929868cbaab2273ecfe"
model = mlflow.xgboost.load_model(f"runs:/{RUN_ID}/xgboost_real_model")

app = FastAPI(title="AI K8s Pod Scheduler")

class NodeMetrics(BaseModel):
    cpu_cores: int
    cpu_percent: int
    memory_mb: int
    memory_percent: int

@app.post("/predict")
def predict(metrics: NodeMetrics):
    features = np.array([[metrics.cpu_cores, metrics.cpu_percent, metrics.memory_mb, metrics.memory_percent]])
    prediction = model.predict(features)[0]
    label = "HIGH_LOAD" if prediction == 1 else "LOW_LOAD"
    return {"node_status": label, "schedule_here": bool(prediction == 0)}

@app.get("/health")
def health():
    return {"status": "AI Scheduler is running!"}