import pandas as pd
import yaml
import joblib
import mlflow
import os
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from pathlib import Path

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def train_model(file_path, ticker, config):
    df = pd.read_parquet(file_path)
    
    # Filter only labeled historical data for training
    df.dropna(subset=['target'], inplace=True)
    df['target'] = df['target'].astype(int)

    # Prepare data
    X = df.drop(columns=["target", "Date"])
    y = df["target"]

    tscv = TimeSeriesSplit(n_splits=5)
    
    # MLflow Setup
    mlflow.set_experiment(config["mlflow"]["experiment_name"])
    
    with mlflow.start_run(run_name=f"Train_{ticker}"):
        model_params = {
            "n_estimators": config["model"]["n_estimators"],
            "random_state": config["model"]["random_state"]
        }
        mlflow.log_params(model_params)
        
        accuracies = []
        f1_scores = []
        
        model = RandomForestClassifier(**model_params)

        for train_idx, test_idx in tscv.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
            acc = accuracy_score(y_test, preds)
            f1 = f1_score(y_test, preds)
            
            accuracies.append(acc)
            f1_scores.append(f1)
            
            print(f"Fold Accuracy: {acc:.4f}, F1: {f1:.4f}")

        # Log average metrics
        avg_acc = sum(accuracies) / len(accuracies)
        avg_f1 = sum(f1_scores) / len(f1_scores)
        
        mlflow.log_metric("avg_accuracy", avg_acc)
        mlflow.log_metric("avg_f1", avg_f1)
        
        print(f"Average Accuracy: {avg_acc:.4f}")

        # Final fit on all available data for this ticker
        model.fit(X, y)
        
        # Save model
        model_dir = Path(config["model"]["save_path"])
        os.makedirs(model_dir, exist_ok=True)
        model_path = model_dir / f"model_{ticker}.pkl"
        joblib.dump(model, model_path)
        
        mlflow.sklearn.log_model(model, "model")
        print(f"Model saved to {model_path}")

if __name__ == "__main__":
    config = load_config()
    processed_path = config["data"]["processed_path"]
    
    for file in os.listdir(processed_path):
        if file.endswith(".parquet"):
            ticker = file.replace(".parquet", "")
            train_model(Path(processed_path) / file, ticker, config)