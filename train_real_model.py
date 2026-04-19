import pandas as pd
import mlflow
import mlflow.xgboost
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load real Kubernetes data
df = pd.read_csv("k8s_metrics_v2.csv")
print(f"Total readings: {len(df)}")
print(f"Label 0 (Do Not Schedule): {len(df[df['label']==0])}")
print(f"Label 1 (Schedule): {len(df[df['label']==1])}")

# Features and target
X = df[['node_cpu_cores', 'node_cpu_percent', 'node_memory_mb', 'node_memory_percent', 'pod_req_cpu', 'pod_req_mem']]
y = df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train with MLflow tracking
mlflow.set_experiment("Real_K8s_Data_V2")

with mlflow.start_run():
    model = xgb.XGBClassifier(eval_metric='logloss', learning_rate=0.1, max_depth=5, n_estimators=150)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    mlflow.log_param("data_source", "synthetic_k8s_v2")
    mlflow.log_param("total_readings", len(df))
    mlflow.log_metric("accuracy", acc)
    mlflow.xgboost.log_model(model, "xgboost_v2_model")

    import joblib
    joblib.dump(model, "model.pkl")

    print(f"\nAccuracy: {acc}")
    print(f"\nReport:\n{classification_report(y_test, y_pred)}")
    print("\nModel saved to MLflow and exported to model.pkl!")
