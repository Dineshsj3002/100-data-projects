import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

# Define path to the processed data
# This assumes the dashboard.py is in the root project directory
DATA_FILE = Path(__file__).resolve().parent / "data" / "monthly_stock_summary.csv"

# Load the summary data
df = pd.read_csv(DATA_FILE, parse_dates=["YearMonth"])

st.title("📈 Monthly Stock Price Analysis - BAJAJFINSV")

# Line chart: Closing Prices
st.subheader("Monthly Closing Price Trend")
st.line_chart(df.set_index("YearMonth")["Close"])

# Candlestick Chart
st.subheader("Monthly Candlestick Chart")
fig = go.Figure(data=[go.Candlestick(
    x=df["YearMonth"],
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"]
)])
st.plotly_chart(fig)

# Volume Chart
st.subheader("Monthly Trading Volume")
st.bar_chart(df.set_index("YearMonth")["Volume"])
