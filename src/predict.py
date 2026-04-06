import pandas as pd
import joblib
import yaml
from pathlib import Path

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def predict(ticker, config=None, return_proba=False):
    if config is None:
        config = load_config()
        
    model_dir = Path(config["model"]["save_path"])
    model_path = model_dir / f"model_{ticker}.pkl"
    processed_path = Path(config["data"]["processed_path"]) / f"{ticker}.parquet"

    if not model_path.exists():
        return {"error": f"Model for {ticker} not found. Train first."}
    
    if not processed_path.exists():
        return {"error": f"Processed data for {ticker} not found."}

    df = pd.read_parquet(processed_path)
    X = df.drop(columns=["target", "Date"])
    
    model = joblib.load(model_path)
    
    latest = X.iloc[-1:]
    
    if return_proba:
        proba = model.predict_proba(latest)[0][1]
        return proba

    pred = model.predict(latest)
    
    return "UP" if pred[0] == 1 else "DOWN"

if __name__ == "__main__":
    result = predict("AAPL")
    print(f"Prediction for AAPL: {result}")