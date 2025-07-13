import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.title("📉 Refund & Returns Ratio")

@st.cache_data
def load_data():
    conn = psycopg2.connect(
        dbname="returns_ratio_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )
    df = pd.read_sql_query("SELECT is_returned, COUNT(*) AS count FROM returns GROUP BY is_returned", conn)
    conn.close()
    df['is_returned'] = df['is_returned'].astype(bool)  # Ensure correct type
    return df

df = load_data()
total_orders = df['count'].sum()
returned_orders = df.loc[df['is_returned'] == True, 'count'].sum()
return_ratio = (returned_orders / total_orders * 100) if total_orders else 0

st.metric("Total Orders", total_orders)
st.metric("Returned Orders", returned_orders)
st.metric("Return Ratio (%)", f"{return_ratio:.2f}%")

fig = px.pie(
    df,
    names=df['is_returned'].map({False: "Completed", True: "Returned"}),
    values="count",
    title="Order Status Breakdown",
    color_discrete_map={"Completed": "lightgreen", "Returned": "red"}
)
st.plotly_chart(fig)
