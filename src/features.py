import pandas as pd
import os
import yaml
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
from pathlib import Path

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def create_features(file_path):
    df = pd.read_parquet(file_path)

    # Returns
    df["return_1"] = df["Close"].pct_change()
    df["return_5"] = df["Close"].pct_change(5)

    # Rolling stats
    df["volatility"] = df["return_1"].rolling(10).std()

    # Moving averages
    df["ma_10"] = df["Close"].rolling(10).mean()
    df["ma_20"] = df["Close"].rolling(20).mean()

    # RSI
    rsi_indicator = RSIIndicator(close=df["Close"], window=14)
    df["rsi"] = rsi_indicator.rsi()

    # MACD
    macd_indicator = MACD(close=df["Close"])
    df["macd"] = macd_indicator.macd()
    df["macd_signal"] = macd_indicator.macd_signal()

    # Bollinger Bands
    bbands = BollingerBands(close=df["Close"], window=20, window_dev=2)
    df["bb_high"] = bbands.bollinger_hband()
    df["bb_low"] = bbands.bollinger_lband()

    # Target (next day movement)
    df["target"] = (df["Close"].shift(-1) > df["Close"])
    df.loc[df["Close"].shift(-1).isna(), "target"] = float('nan')

    # Drop rows where indicators are NaN (usually the beginning of the file)
    # But keep the last row which has the latest features for tomorrow's prediction
    feature_cols = [c for c in df.columns if c not in ["target", "Date"]]
    df.dropna(subset=feature_cols, inplace=True)
    
    return df

def process_all(raw_path, processed_path):
    os.makedirs(processed_path, exist_ok=True)

    for file in os.listdir(raw_path):
        if file.endswith(".parquet"):
            try:
                print(f"Processing {file}...")
                df = create_features(Path(raw_path) / file)
                df.to_parquet(Path(processed_path) / file)
                print(f"Processed {file} successfully")
            except Exception as e:
                print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    config = load_config()
    raw_path = config["data"]["raw_path"]
    processed_path = config["data"]["processed_path"]
    
    process_all(raw_path, processed_path)