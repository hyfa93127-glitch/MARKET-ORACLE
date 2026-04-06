# Stock Predictor

A robust end-to-end Machine Learning platform for stock price movement prediction using Technical Analysis and Random Forest.

## Features

- **Automated Ingestion**: Fetch historical data from Yahoo Finance.
- **Advanced Feature Engineering**: RSI, MACD, Bollinger Bands, and more via `ta` library.
- **Experiment Tracking**: Integrated with MLflow for tracking parameters and performance metrics.
- **Interactive Dashboard**: Streamlit interface with Plotly charts and technical indicator insights.
- **REST API**: FastAPI endpoints for real-time predictions.
- **Orchestration**: Single-command pipeline management.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure**:
   Edit `config.yaml` to add/remove tickers or change model hyperparameters.

## Usage

### Run the Pipeline
Execute the full ML workflow (Ingest -> Process -> Train -> Evaluate):
```bash
python pipeline.py
```

### Start the API
```bash
uvicorn app.api:app --reload
```

### Launch the Dashboard
```bash
streamlit run app.dashboard.py
```

## Project Structure

- `app/`: Web and API implementations.
- `src/`: Core ML pipeline components.
- `data/`: Storage for raw and processed datasets.
- `models/`: Trained model serialization.
- `config.yaml`: Centralized configuration management.
- `pipeline.py`: Orchestration script.
