# 📦 Customer Orders Summary

Welcome to Day 1 of your 100 Mini Projects!

This project analyzes customer order data using PostgreSQL for data storage and Python (pandas + Streamlit) for analysis and visualization.

---

## 🎯 Objective

Analyze customer data from an e-commerce platform to:
- Summarize customer distribution
- Find top states & cities
- Power visual dashboards for insights
- Practice SQL + Python integration

---

## 🧰 Tech Stack

| Tool         | Purpose                              |
|--------------|---------------------------------------|
| PostgreSQL   | Relational database (via pgAdmin)     |
| Python       | Data loading, analysis, automation    |
| pandas       | DataFrames and manipulation           |
| matplotlib   | (Optional) Charting                   |
| Streamlit    | Interactive dashboard                 |
| psycopg2     | PostgreSQL connector for Python       |
| VSCode       | Code editor of choice                 |

---

## 🗃️ Folder Structure

customer_orders_summary/
│
├── data/ # CSV file
│ └── olist_customers_dataset.csv
│
├── sql/
│ └── create_customer_table.sql
│
├── scripts/
│ └── load_customers_to_postgres.py
│
├── analysis/
│ └── analyze_customers.py
│
├── dashboard/
│ └── dashboard.py
│
├── reports/
│ └── customer_summary.csv (optional output)
│
└── README.md

yaml
Copy
Edit

---

## 🚀 How to Run This Project

### 1. Set up PostgreSQL (via pgAdmin)
- Create a database: `customer_orders_db`
- Run SQL from `sql/create_customer_table.sql`

### 2. Load Data into PostgreSQL
```bash
cd scripts
python load_customers_to_postgres.py
3. Analyze in Python
bash
Copy
Edit
cd analysis
python analyze_customers.py
4. Run Streamlit Dashboard
bash
Copy
Edit
cd dashboard
streamlit run dashboard.py
📊 Output Preview
📌 Unique customers count

🗺️ Top cities and states by customer count

📈 Bar charts, dataframes, and toggleable raw data

🧠 Skills Practiced
SQL table creation + queries

ETL from CSV → PostgreSQL

Python DB connection

Real-world data wrangling

Visual storytelling with dashboards

💡 Future Enhancements
Join with orders and order_items tables

Add time-based trends and segmentation

Enable CSV/PDF export from Streamlit

Upload to GitHub for your portfolio

🤖 Author
👩‍💻 Judy | Junior Data Analyst in Training
🗓️ Project: Day 1 of #100MiniDataProjects
🔗 Inspired by real-world e-commerce analytics

yaml
Copy
Edit

---

Want this dropped into your folder automatically as a file? Or want to generate a GitHub-style project page with badges and flair? Just say the word and I’ll make it pixel-perfect. 🎨💻







Ask ChatGPT
You said:
postgresql tell the query one or two give


ChatGPT said:
Absolutely! Let’s add some real SQL muscle 💪 to your PostgreSQL side of the project. Since your customers table is already live, here are 2 practical SQL queries that make sense in this context:

🔍 1. Top 10 States by Number of Customers
sql
Copy
Edit
SELECT customer_state, COUNT(*) AS customer_count
FROM customers
GROUP BY customer_state
ORDER BY customer_count DESC
LIMIT 10;
📈 Use this to feed the Top States chart in your dashboard.
It gives you the most active customer regions — great for marketing, logistics, or just flexing your query skills.

🌆 2. Top 10 Cities by Number of Customers
sql
Copy
Edit
SELECT customer_city, COUNT(*) AS customer_count
FROM customers
GROUP BY customer_city
ORDER BY customer_count DESC
LIMIT 10;
Perfect for city-level analysis, delivery zones, or deciding where to open that imaginary warehouse. 🏢

🧠 Bonus Thought: Wanna Join With Orders?
If you later load orders into PostgreSQL, you'll be able to do cool joins like:

sql
Copy
Edit
SELECT c.customer_state, COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_state
ORDER BY total_orders DESC
LIMIT 10;
📌 You’re one table away from analyzing real order activity.

Want me to generate a SQL file with all these + bonus queries for your sql/ folder?
Say the magic words: "drop the SQL pack" and I got you.










