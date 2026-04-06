import streamlit as st
import pandas as pd
import yaml
import plotly.graph_objects as go
import yfinance as yf
from src.predict import predict
from src.allocator import calculate_allocation
from pathlib import Path

st.set_page_config(page_title="Stock Predictor", layout="wide")

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
tickers = config["data"]["tickers"]

st.sidebar.title("Stock Predictor")
selected_ticker = st.sidebar.selectbox("Choose a Ticker", tickers)

st.title(f"Stock Analysis: {selected_ticker}")

# Load Data
processed_file = Path(config["data"]["processed_path"]) / f"{selected_ticker}.parquet"

if processed_file.exists():
    df = pd.read_parquet(processed_file)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sidebar Date Filter
    st.sidebar.markdown("---")
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )
    
    st.sidebar.markdown("---")
    with st.sidebar.form("budget_form"):
        budget = st.number_input("Investment Budget ($)", min_value=0, value=1000, step=100)
        submitted = st.form_submit_button("Calculate Portfolio")
    
    # Filter Data
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
    else:
        df_filtered = df

    # Visualizations
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if not df_filtered.empty:
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df_filtered['Date'],
                            open=df_filtered['Open'],
                            high=df_filtered['High'],
                            low=df_filtered['Low'],
                            close=df_filtered['Close'], name='Market Data'))
            
            # Add MAs
            fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['ma_10'], line=dict(color='orange', width=1), name='MA 10'))
            fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['ma_20'], line=dict(color='blue', width=1), name='MA 20'))
            
            fig.update_layout(title=f"{selected_ticker} Price History", yaxis_title="Price (USD)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data for the selected date range.")
        
    with col2:
        st.subheader("Prediction")
        if st.button("Get Prediction"):
            prediction = predict(selected_ticker, config)
            if isinstance(prediction, str):
                color = "green" if prediction == "UP" else "red"
                st.markdown(f"### Next Day: <span style='color:{color}'>{prediction}</span>", unsafe_allow_html=True)
            else:
                st.error(prediction.get("error", "Error getting prediction."))
        
        st.subheader("Latest Info")
        latest = df.iloc[-1]
        st.metric("Current Price", f"${latest['Close']:.2f}")
        st.metric("RSI", f"{latest['rsi']:.2f}")
        st.metric("Volatility", f"{latest['volatility']:.4f}")
        
    # Technical Indicators Tab
    tab1, tab2, tab3, tab4 = st.tabs(["Technical Data", "Raw Data", "Upcoming Events", "Portfolio Allocator"])
    with tab1:
        st.write(df_filtered[['Date', 'Close', 'rsi', 'macd', 'bb_high', 'bb_low']].tail(20))
    with tab2:
        st.write(df_filtered.tail(20))
    with tab3:
        st.subheader(f"Upcoming Events for {selected_ticker}")
        ticker_data = yf.Ticker(selected_ticker)
        try:
            cal = ticker_data.calendar
            if cal:
                # Display nicely
                col_a, col_b = st.columns(2)
                
                # Earnings Info
                with col_a:
                    st.write("### Earnings & Revenue")
                    if 'Earnings Date' in cal:
                        st.info(f"**Next Earnings Date:** {', '.join([str(d) for d in cal['Earnings Date']])}")
                    st.write(f"**Average Estimate:** ${cal.get('Earnings Average', 'N/A')}")
                    st.write(f"**Revenue Average:** ${cal.get('Revenue Average', 0):,.0f}")
                
                # Dividend Info
                with col_b:
                    st.write("### Dividends")
                    st.write(f"**Dividend Date:** {cal.get('Dividend Date', 'N/A')}")
                    st.write(f"**Ex-Dividend Date:** {cal.get('Ex-Dividend Date', 'N/A')}")
            else:
                st.info(f"No upcoming scheduled events found for {selected_ticker}.")
        except Exception:
            st.error("Failed to fetch calendar data from Yahoo Finance.")
            
    with tab4:
        st.subheader("Portfolio Recommendations")
        
        if budget > 0:
            with st.spinner("Analyzing all tickers and calculating best allocation..."):
                st.write(f"Based on your budget of **${budget:,.2f}**, we suggest the following allocation among stocks predicted to move UP:")
                
                # Collect data for ALL tickers
                all_ticker_data = []
                for t in tickers:
                    # Current Price (from processed file, latest close)
                    t_file = Path(config["data"]["processed_path"]) / f"{t}.parquet"
                    if t_file.exists():
                        t_df = pd.read_parquet(t_file)
                        latest_p = float(t_df.iloc[-1]['Close'])
                        # Confidence
                        conf = predict(t, config, return_proba=True)
                        if isinstance(conf, float):
                            all_ticker_data.append({'ticker': t, 'price': latest_p, 'confidence': conf})
                
                if all_ticker_data:
                    recs, total_spent = calculate_allocation(budget, all_ticker_data)
                    
                    if recs:
                        st.table(pd.DataFrame(recs))
                        st.success(f"**Total Invested:** ${total_spent:,.2f} | **Remaining Cash:** ${(budget - total_spent):,.2f}")
                    else:
                        st.warning("No bullish (UP) investment opportunities found among configured tickers at this time.")
                else:
                    st.error("Could not fetch data for any tickers.")
        else:
            st.info("Please enter an investment budget in the sidebar to generate recommendations.")

else:
    st.warning(f"No processed data found for {selected_ticker}. Please run the pipeline first.")