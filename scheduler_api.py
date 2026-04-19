from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import numpy as np
import os
import pandas as pd

from fastapi.middleware.gzip import GzipMiddleware
# Initialize our primary web server
app = FastAPI(title='AI K8s Pod Scheduler - Real Metrics Edition')
app.add_middleware(GzipMiddleware, minimum_size=1000)

MODEL_PATH = os.environ.get("MODEL_PATH", "model.pkl")
model = joblib.load(MODEL_PATH)

# Re-configured for the 6 real K8s metrics including Pod constraints
class SchedulingRequest(BaseModel):
    node_cpu_cores: float
    node_cpu_percent: float
    node_memory_mb: float
    node_memory_percent: float
    pod_req_cpu: float
    pod_req_mem: float

# ===== Serve the stunning dashboard at root =====
@app.get('/', response_class=FileResponse)
def dashboard():
    return FileResponse('static/dashboard.html')

# ===== JSON API info endpoint =====
@app.get('/api')
def api_info():
    return {
        'message': 'Welcome to AI Kubernetes Scheduler API.',
        'endpoints': {
            'dashboard': '/ (Interactive Dashboard)',
            'predict': 'POST /predict (JSON API)',
            'health': 'GET /health',
            'stats': 'GET /stats',
            'gradio_ui': '/ui (Gradio Interface)'
        }
    }

# ===== Prediction endpoint =====
@app.post('/predict')
def predict(request: SchedulingRequest):
    # Convert to DataFrame to perfectly preserve XGBoost feature names
    input_data = pd.DataFrame(
        [[request.node_cpu_cores, request.node_cpu_percent, request.node_memory_mb, request.node_memory_percent, request.pod_req_cpu, request.pod_req_mem]],
        columns=['node_cpu_cores', 'node_cpu_percent', 'node_memory_mb', 'node_memory_percent', 'pod_req_cpu', 'pod_req_mem']
    )
    prediction = model.predict(input_data)[0]

    # Class 0: High Load / Do Not Schedule
    # Class 1: Low Load / Schedule
    is_high_load = bool(prediction == 0)
    label = 'HIGH_LOAD' if is_high_load else 'LOW_LOAD'

    return {
        'node_status': label,
        'schedule_here': not is_high_load,
        'features_received': request.model_dump()
    }

# ===== Health check =====
@app.get('/health')
def health():
    return {'status': 'AI Scheduler API is running!'}

# ===== Dataset stats endpoint =====
@app.get('/stats')
def stats():
    try:
        df = pd.read_csv('k8s_metrics_v2.csv')
        return {
            'total_samples': len(df),
            'class_0_low': int(len(df[df['label'] == 0])),
            'class_1_high': int(len(df[df['label'] == 1])),
            'features': ['node_cpu_cores', 'node_cpu_percent', 'node_memory_mb', 'node_memory_percent', 'pod_req_cpu', 'pod_req_mem'],
            'cpu_cores_range': [int(df['node_cpu_cores'].min()), int(df['node_cpu_cores'].max())],
            'memory_mb_range': [int(df['node_memory_mb'].min()), int(df['node_memory_mb'].max())]
        }
    except Exception as e:
        return {'error': str(e)}

# ===== Mount static files =====
app.mount('/static', StaticFiles(directory='static'), name='static')

# ===== Embed the Gradio UI at /ui route =====
import gradio as gr
from app import iface
app = gr.mount_gradio_app(app, iface, path="/ui", root_path="/ui")
