
# gradio → creates the web interface
# joblib → loads the saved ML model
import os
import gradio as gr
import joblib

MODEL_PATH = os.environ.get("MODEL_PATH", "model.pkl")
PORT = int(os.environ.get("APP_PORT", 7860))

# Loading the trained XGBoost model from model.pkl
# This model was trained and tracked using MLflow
model = joblib.load(MODEL_PATH)
import pandas as pd

# Takes real metrics of a Kubernetes node: cpu_cores, cpu_percent, memory_mb, memory_percent
# Returns whether the node is High Load or Low Load based on 1022 real samples!
def predict(cpu_cores, cpu_percent, memory_mb, memory_percent):
    # XGBoost trained on a DataFrame expects a DataFrame back to ensure features map flawlessly!
    input_data = pd.DataFrame([[cpu_cores, cpu_percent, memory_mb, memory_percent]], 
                             columns=['cpu_cores', 'cpu_percent', 'memory_mb', 'memory_percent'])
    
    pred = model.predict(input_data)
    if pred[0] == 1:
        return "❌ CLASS 1: HIGH LOAD. Do not schedule."
    else:
        return "✅ CLASS 0: LOW LOAD. Recommended for Pod Scheduling."

iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="CPU Cores (e.g., 250)"), 
        gr.Number(label="CPU Percentage (e.g., 15)"),
        gr.Number(label="Memory MB (e.g., 512)"),
        gr.Number(label="Memory Percentage (e.g., 40)")
    ],
    outputs="text",
    title="AI K8s Pod Scheduler - Node Predictor",
    description="🤖 AI Scheduler Interface – Trained on 1,022 real Kubernetes Node Metrics!"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=PORT)
