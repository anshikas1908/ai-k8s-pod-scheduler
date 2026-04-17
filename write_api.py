with open("scheduler_api.py", "w") as f:
    lines = [
        "from fastapi import FastAPI\n",
        "from pydantic import BaseModel\n",
        "import joblib\n",
        "import numpy as np\n",
        "\n",
        "model = joblib.load('model.pkl')\n",
        "\n",
        "app = FastAPI(title='AI K8s Pod Scheduler')\n",
        "\n",
        "class NodeMetrics(BaseModel):\n",
        "    cpu_percent: float\n",
        "    memory_percent: float\n",
        "\n",
        "@app.post('/predict')\n",
        "def predict(metrics: NodeMetrics):\n",
        "    features = np.array([[metrics.cpu_percent, metrics.memory_percent]])\n",
        "    prediction = model.predict(features)[0]\n",
        "    label = 'HIGH_LOAD' if prediction == 1 else 'LOW_LOAD'\n",
        "    return {'node_status': label, 'schedule_here': bool(prediction == 0)}\n",
        "\n",
        "@app.get('/health')\n",
        "def health():\n",
        "    return {'status': 'AI Scheduler is running!'}\n",
    ]
    f.writelines(lines)
print("Done!")