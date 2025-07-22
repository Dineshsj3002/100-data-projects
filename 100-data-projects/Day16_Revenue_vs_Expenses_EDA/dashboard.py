import streamlit as st
import pandas as pd
import plotly.express as px

# Load and process data
df = pd.read_csv(
    r'C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day16_Revenue_vs_Expenses_EDA\data\Superstore.csv',
    parse_dates=['Order Date'],
    encoding='latin1'
)

# Ensure 'Order Date' is datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
df['Expenses'] = df['Sales'] - df['Profit']
monthly = df.groupby('Month')[['Sales', 'Profit', 'Expenses']].sum().reset_index()
monthly.rename(columns={'Sales': 'Revenue'}, inplace=True)

st.title("💰 Superstore: Revenue vs Expenses Dashboard")
st.markdown("Monthly trend analysis for Revenue, Expenses, and Profit.")

# Plot
fig = px.line(monthly, x='Month', y=['Revenue', 'Expenses', 'Profit'], markers=True,
              title='Monthly Financial Trends')
st.plotly_chart(fig)

# Cumulative Metrics
st.subheader("📌 Summary Metrics")
st.metric("Total Revenue", f"${monthly['Revenue'].sum():,.2f}")
st.metric("Total Expenses", f"${monthly['Expenses'].sum():,.2f}")
st.metric("Total Profit", f"${monthly['Profit'].sum():,.2f}")

# Data Table
st.subheader("📋 Data Table")
st.dataframe(monthly)
