from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load('model.pkl')

app = FastAPI(title='AI K8s Pod Scheduler')

class NodeMetrics(BaseModel):
    cpu_percent: float
    memory_percent: float

@app.post('/predict')
def predict(metrics: NodeMetrics):
    features = np.array([[metrics.cpu_percent, metrics.memory_percent]])
    prediction = model.predict(features)[0]
    label = 'HIGH_LOAD' if prediction == 1 else 'LOW_LOAD'
    return {'node_status': label, 'schedule_here': bool(prediction == 0)}

@app.get('/health')
def health():
    return {'status': 'AI Scheduler is running!'}
