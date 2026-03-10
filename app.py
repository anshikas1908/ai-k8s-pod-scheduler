import gradio as gr
import joblib

model = joblib.load("model.pkl")

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
