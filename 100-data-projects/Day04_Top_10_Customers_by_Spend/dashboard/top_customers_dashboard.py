import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="Top 10 Customers", layout="wide")
st.title("💰 Top 10 Customers by Spend")

@st.cache_data
def load_data():
    try:
        conn = psycopg2.connect(
            dbname="monthly_revenue_db",
            user="postgres",
            password="root123",  # 🔐 Consider using environment variables later
            host="localhost",
            port="5432"
        )
        query = """
        SELECT customer, ROUND(SUM(amount), 2) AS total_spend
        FROM customer_spending
        GROUP BY customer
        ORDER BY total_spend DESC
        LIMIT 10;
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()  # return empty df if something fails

# 🚀 Load and show
data = load_data()

if not data.empty:
    fig = px.bar(
        data,
        x='total_spend',
        y='customer',
        orientation='h',
        title='Top 10 Customers by Total Spend',
        color='total_spend',
        labels={'total_spend': 'Total Spend ($)', 'customer': 'Customer'},
        height=500
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(data, use_container_width=True)
else:
    st.warning("No data found. Make sure the table has been loaded.")
