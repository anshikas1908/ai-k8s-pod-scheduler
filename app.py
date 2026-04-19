
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

# Takes 6 real metrics including Pod constraints
def predict(node_cpu_cores, node_cpu_percent, node_memory_mb, node_memory_percent, pod_req_cpu, pod_req_mem):
    # XGBoost trained on a DataFrame expects a DataFrame back to ensure features map flawlessly!
    input_data = pd.DataFrame(
        [[node_cpu_cores, node_cpu_percent, node_memory_mb, node_memory_percent, pod_req_cpu, pod_req_mem]], 
        columns=['node_cpu_cores', 'node_cpu_percent', 'node_memory_mb', 'node_memory_percent', 'pod_req_cpu', 'pod_req_mem']
    )
    
    pred = model.predict(input_data)
    if pred[0] == 0:
        return "❌ CLASS 0: HIGH LOAD. Node overloaded or Pod too large. Do not schedule."
    else:
        return "✅ CLASS 1: LOW LOAD. Excellent fit. Recommended for Pod Scheduling."

iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="Node CPU Cores (e.g., 250)"), 
        gr.Number(label="Node CPU Percentage (e.g., 15)"),
        gr.Number(label="Node Memory MB (e.g., 512)"),
        gr.Number(label="Node Memory Percentage (e.g., 40)"),
        gr.Number(label="Pod Required CPU (e.g., 100)"),
        gr.Number(label="Pod Required Memory MB (e.g., 256)"),
    ],
    outputs="text",
    title="AI K8s Pod Scheduler - Node Predictor",
    description="🤖 AI Scheduler Engine – Trained on variable realistic cluster data!"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=PORT)
