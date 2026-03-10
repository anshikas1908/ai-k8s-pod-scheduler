import mlflow
import mlflow.xgboost
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = {'feature1': list(range(1, 11)), 'feature2': list(range(11, 21)), 'target': [0,0,0,0,1,1,1,1,1,1]}
df = pd.DataFrame(data)
X = df[['feature1', 'feature2']]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
mlflow.set_experiment("Demo_Local_Run")
with mlflow.start_run():
    model = xgb.XGBClassifier(eval_metric='logloss')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("model_type", "XGBoost")
    mlflow.log_metric("accuracy", acc)
    mlflow.xgboost.log_model(model, "xgboost_model")
    print(f"Accuracy: {acc}")
    print("Run complete!")
