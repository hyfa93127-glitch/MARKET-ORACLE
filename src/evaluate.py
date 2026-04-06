import pandas as pd
import yaml
import joblib
import mlflow
import os
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from pathlib import Path

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def evaluate_model(file_path, ticker, config):
    df = pd.read_parquet(file_path)

    # Use a hold-out set (e.g., the last 20% of data) to simulate future data
    test_size = int(len(df) * config["model"]["test_size"])
    train_df = df.iloc[:-test_size]
    test_df = df.iloc[-test_size:]

    X_test = test_df.drop(columns=["target", "Date"])
    y_test = test_df["target"]

    model_dir = Path(config["model"]["save_path"])
    model_path = model_dir / f"model_{ticker}.pkl"
    
    if not os.path.exists(model_path):
        print(f"Model for {ticker} not found, skipping evaluation")
        return

    model = joblib.load(model_path)
    preds = model.predict(X_test)

    print(f"--- Evaluation for {ticker} ---")
    print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, preds))
    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    # Log metrics to MLflow for current active run if any
    # Since we call it separately, we could start a new run or just print.
    # For now, we'll focus on the printed results.

if __name__ == "__main__":
    config = load_config()
    processed_path = config["data"]["processed_path"]
    
    for file in os.listdir(processed_path):
        if file.endswith(".parquet"):
            ticker = file.replace(".parquet", "")
            evaluate_model(Path(processed_path) / file, ticker, config)