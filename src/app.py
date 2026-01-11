from fastapi import FastAPI
import mlflow
import mlflow.sklearn

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = FastAPI()

def setup_mlflow(experiment_name: str = "wine_experiment"):
    mlflow.set_experiment(experiment_name)

def load_data():
    data = load_wine()
    return train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)

@app.get("/train")
def train():
    setup_mlflow()

    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)
    accuracy = evaluate_model(model, X_test, y_test)

    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "random_forest_model")
        mlflow.log_metric("accuracy", float(accuracy))

    return {"accuracy": float(accuracy)}


@app.get("/extract")
def extract():
    return {"message": "Data extraction endpoint"}


@app.get("/")
def home():
    return "Hello, this is the MLflow model training API!"
