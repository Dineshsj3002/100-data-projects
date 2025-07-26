import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Set page config
st.set_page_config(page_title="Real Estate Fraud Detector", layout="centered")

st.title("🏠 Real Estate Fraud Detection Dashboard")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="fraud_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

# Load data
df = pd.read_sql("SELECT * FROM fraud_transactions;", conn)

# Summary
total = len(df)
fraud_count = df['fraud_indicator'].sum()
non_fraud = total - fraud_count
fraud_percent = round((fraud_count / total) * 100, 2)

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", total)
col2.metric("Fraudulent", fraud_count, f"{fraud_percent}%")
col3.metric("Non-Fraudulent", non_fraud, f"{round(100 - fraud_percent, 2)}%")

# Plot bar chart
st.subheader("📊 Fraud vs Non-Fraud Transactions")
plot_df = df['fraud_indicator'].value_counts().rename(index={0: 'Not Fraud', 1: 'Fraud'})

fig, ax = plt.subplots()
sns.barplot(x=plot_df.index, y=plot_df.values, palette="Set2", ax=ax)
ax.set_title("Fraud Detection Summary")
ax.set_xlabel("Transaction Type")
ax.set_ylabel("Count")
st.pyplot(fig)

conn.close()
