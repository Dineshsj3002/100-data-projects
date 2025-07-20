import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="COVID Spread by Country", layout="wide")

@st.cache_data
def fetch_data():
    conn = psycopg2.connect(
        dbname="covid_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )
    query = "SELECT * FROM covid_stats;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

data = fetch_data()

st.title("🌍 Country-wise COVID Spread Dashboard")

# ----------------------
# 🦠 Top 10 by Confirmed
# ----------------------
top_confirmed = data.sort_values("confirmed", ascending=False).head(10)

fig1 = px.bar(
    top_confirmed,
    x="confirmed",
    y="country",
    orientation="h",
    title="Top 10 Countries by Confirmed Cases"
)
fig1.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig1, use_container_width=True)

# --------------------------------
# 📈 Weekly % Increase Bubble Chart
# --------------------------------
# Convert negative values to zero for size
data["week_change_clean"] = data["week_change"].apply(lambda x: max(x, 0))

fig2 = px.scatter(
    data,
    x="country",
    y="week_percent_increase",
    size="week_change_clean",
    color="who_region",
    title="📈 Weekly % Increase by Country",
    hover_name="country",
)
st.plotly_chart(fig2, use_container_width=True)

# ----------
# 🧾 Raw Data
# ----------
st.subheader("📋 Full Dataset")
st.dataframe(data)
