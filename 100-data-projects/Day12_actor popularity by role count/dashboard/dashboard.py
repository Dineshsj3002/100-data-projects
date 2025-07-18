import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="Actor Popularity Tracker", layout="wide")

@st.cache_data
def fetch_data():
    conn = psycopg2.connect(
        dbname="actor_roles_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )

    query = """
        SELECT actor_name, COUNT(*) AS total_roles
        FROM actor_roles
        GROUP BY actor_name
        ORDER BY total_roles DESC;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Clean up whitespace from actor names
    df['actor_name'] = df['actor_name'].str.strip()

    return df

data = fetch_data()

st.title("🎭 Actor Popularity by Role Count")

fig = px.bar(
    data.head(20),  # Show top 20 actors for clarity
    x="total_roles",
    y="actor_name",
    orientation="h",
    title="Top Actors by Total Roles",
    labels={"actor_name": "Actor", "total_roles": "Number of Roles"}
)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})

st.plotly_chart(fig, use_container_width=True)

st.dataframe(data)

