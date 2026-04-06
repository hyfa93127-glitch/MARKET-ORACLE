import yfinance as yf
import pandas as pd
import os
import yaml
from pathlib import Path

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def fetch_data(tickers, period="2y", raw_path="data/raw/"):
    os.makedirs(raw_path, exist_ok=True)

    for ticker in tickers:
        try:
            print(f"Fetching data for {ticker}...")
            df = yf.download(ticker, period=period)
            
            if df.empty:
                print(f"Warning: No data found for {ticker}")
                continue
                
            # Flatten MultiIndex columns if necessary (common in yfinance >=1.0)
            if isinstance(df.columns, pd.MultiIndex):
                # We expect (Price, Ticker) format. Let's drop the ticker level
                df.columns = df.columns.get_level_values(0)

            df.reset_index(inplace=True)

            file_path = Path(raw_path) / f"{ticker}.parquet"
            df.to_parquet(file_path)

            print(f"Saved {ticker} data to {file_path}")
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

if __name__ == "__main__":
    config = load_config()
    tickers = config["data"]["tickers"]
    period = config["data"]["period"]
    raw_path = config["data"]["raw_path"]
    
    fetch_data(tickers, period, raw_path)