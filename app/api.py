from fastapi import FastAPI, HTTPException
from src.predict import predict
import yaml

app = FastAPI(title="Stock Predictor API")

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

@app.get("/")
def home():
    return {"message": "Welcome to Stock Predictor API. Use /predict/{ticker}"}

@app.get("/predict/{ticker}")
def get_prediction(ticker: str):
    config = load_config()
    ticker = ticker.upper()
    
    if ticker not in config["data"]["tickers"]:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not in configured list.")

    result = predict(ticker, config)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return {"ticker": ticker, "prediction": result}