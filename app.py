
# gradio → creates the web interface
# joblib → loads the saved ML model
import gradio as gr
import joblib
# Loading the trained XGBoost model from model.pkl
# This model was trained and tracked using MLflow
model = joblib.load("model.pkl")
# Takes CPU usage and Memory usage of a Kubernetes node
# Returns whether the node is High Load or Low Load
def predict(feature1, feature2):
    pred = model.predict([[feature1, feature2]])
    label = "Class 1 - High Load Node" if pred[0] == 1 else "Class 0 - Low Load Node"
    return f"Predicted: {label}"

iface = gr.Interface(
    fn=predict,
    inputs=[gr.Number(label="Feature 1 - CPU Usage"), gr.Number(label="Feature 2 - Memory Usage")],
    outputs="text",
    title="AI K8s Pod Scheduler - Node Predictor",
    description="Enter node metrics to predict best scheduling class."
)
iface.launch()
