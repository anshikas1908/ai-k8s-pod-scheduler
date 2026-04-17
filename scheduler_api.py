from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import numpy as np
import os
import pandas as pd

# Initialize our primary web server
app = FastAPI(title='AI K8s Pod Scheduler - Real Metrics Edition')

MODEL_PATH = os.environ.get("MODEL_PATH", "model.pkl")
model = joblib.load(MODEL_PATH)

# Re-configured for the 4 real K8s metrics
class NodeMetrics(BaseModel):
    cpu_cores: float
    cpu_percent: float
    memory_mb: float
    memory_percent: float

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
def predict(metrics: NodeMetrics):
    # Convert to DataFrame to perfectly preserve XGBoost feature names
    input_data = pd.DataFrame(
        [[metrics.cpu_cores, metrics.cpu_percent, metrics.memory_mb, metrics.memory_percent]],
        columns=['cpu_cores', 'cpu_percent', 'memory_mb', 'memory_percent']
    )
    prediction = model.predict(input_data)[0]

    # Class 0: Low Load / Free
    # Class 1: High Load / Busy
    is_high_load = bool(prediction == 1)
    label = 'HIGH_LOAD' if is_high_load else 'LOW_LOAD'

    return {
        'node_status': label,
        'schedule_here': not is_high_load,
        'features_received': metrics.model_dump()
    }

# ===== Health check =====
@app.get('/health')
def health():
    return {'status': 'AI Scheduler API is running!'}

# ===== Dataset stats endpoint =====
@app.get('/stats')
def stats():
    try:
        df = pd.read_csv('k8s_metrics.csv')
        return {
            'total_samples': len(df),
            'class_0_low': int(len(df[df['label'] == 0])),
            'class_1_high': int(len(df[df['label'] == 1])),
            'features': ['cpu_cores', 'cpu_percent', 'memory_mb', 'memory_percent'],
            'cpu_cores_range': [int(df['cpu_cores'].min()), int(df['cpu_cores'].max())],
            'memory_mb_range': [int(df['memory_mb'].min()), int(df['memory_mb'].max())]
        }
    except Exception as e:
        return {'error': str(e)}

# ===== Mount static files =====
app.mount('/static', StaticFiles(directory='static'), name='static')

# ===== Embed the Gradio UI at /ui route =====
import gradio as gr
from app import iface
app = gr.mount_gradio_app(app, iface, path="/ui", root_path="/ui")
