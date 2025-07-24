import pandas as pd
import psycopg2
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="school_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

# Load data
df = pd.read_sql("SELECT * FROM attendance", conn)
conn.close()

# Clean and preprocess
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.to_period('M').astype(str)
df['attendance_pct'] = df['present'] / df['enrolled'] * 100

# Streamlit layout
st.title("📊 School Attendance Heatmap (Monthly %)")
selected_school = st.selectbox("Choose a school:", df['school_dbn'].unique())

filtered_df = df[df['school_dbn'] == selected_school]

# Check for empty data
if filtered_df.empty:
    st.warning("No data available for this school.")
else:
    pivot = filtered_df.pivot_table(
        index='month',
        values='attendance_pct',
        aggfunc='mean'
    ).sort_index()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot.T, cmap='YlGnBu', linewidths=0.5, linecolor='gray', annot=True, fmt=".1f", ax=ax)
    plt.title(f"Average Monthly Attendance % for {selected_school}")
    st.pyplot(fig)
