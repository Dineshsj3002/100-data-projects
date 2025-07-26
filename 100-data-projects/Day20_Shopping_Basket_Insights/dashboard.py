import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Set Streamlit page config
st.set_page_config(page_title="🛍️ Shopping Basket Insights", layout="wide")

# Connect to PostgreSQL using SQLAlchemy
engine = create_engine("postgresql+psycopg2://postgres:root123@localhost/shopping_db")
df = pd.read_sql("SELECT * FROM shopping_data;", engine)

# Title
st.title("🛒 Shopping Basket Insights Dashboard")

# Metrics Summary
total_sales = df['total_amount'].sum()
avg_spend = df['total_amount'].mean()
total_customers = df['customer_id'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"₹{total_sales:,.2f}")
col2.metric("📊 Avg Spend", f"₹{avg_spend:,.2f}")
col3.metric("🧑‍🤝‍🧑 Total Customers", total_customers)

# Section: Top Categories
st.subheader("📦 Top 5 Product Categories by Revenue")
top_categories = df.groupby('category')['total_amount'].sum().sort_values(ascending=False).head(5)

fig1, ax1 = plt.subplots()
sns.barplot(
    x=top_categories.values,
    y=top_categories.index,
    hue=top_categories.index,
    palette="coolwarm",
    legend=False,
    ax=ax1
)
ax1.set_xlabel("Revenue")
ax1.set_ylabel("Category")
st.pyplot(fig1)

# Section: Gender-based Revenue
st.subheader("🚻 Revenue by Gender")
gender_rev = df.groupby('gender')['total_amount'].sum()

fig2, ax2 = plt.subplots()
sns.barplot(
    x=gender_rev.index,
    y=gender_rev.values,
    hue=gender_rev.index,
    palette="viridis",
    legend=False,
    ax=ax2
)
ax2.set_ylabel("Revenue")
st.pyplot(fig2)

# Section: Monthly Sales Trend
st.subheader("📅 Monthly Revenue Trend")
df['month'] = pd.to_datetime(df['shopping_date']).dt.to_period('M')
monthly_rev = df.groupby('month')['total_amount'].sum()

fig3, ax3 = plt.subplots()
monthly_rev.plot(kind='line', marker='o', ax=ax3)
ax3.set_title("Monthly Revenue Trend")
ax3.set_ylabel("Revenue")
ax3.set_xlabel("Month")
st.pyplot(fig3)

# Optional Raw Data
if st.checkbox("🔍 Show Raw Data"):
    st.dataframe(df)
