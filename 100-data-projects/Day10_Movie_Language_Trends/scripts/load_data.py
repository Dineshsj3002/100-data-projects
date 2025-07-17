# scripts/load_data.py (Revised)

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DB_NAME = "netflix_db"
DB_USER = "postgres"
DB_PASSWORD = "root123"
DB_HOST = "localhost"
DB_PORT = "5432"

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'netflix_titles.csv')

def load_data():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()
        print("Successfully connected to the database.")

# scripts/load_data.py (Revised Data Cleaning Section)

# ... inside the load_data() function, after reading the CSV ...

        df = pd.read_csv(CSV_PATH)
        df.rename(columns={'cast': '"cast"'}, inplace=True)
        
        # Convert 'date_added' to datetime, creating NaT for errors
        df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')

        # --- THIS IS THE FIX ---
        # Convert the entire DataFrame to use Python objects, then replace
        # all forms of "not found" (NaN, NaT) with Python's None.
        # This is a very reliable way to clean data before SQL insertion.
        df = df.astype(object).where(pd.notnull(df), None)
        # --- END OF FIX ---

        # The columns list MUST match the order in your revised table
        cols = ['show_id', 'type', 'title', 'director', '"cast"', 'country', 'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description']
        tuples = [tuple(x) for x in df[cols].to_numpy()]

# ... the rest of the script remains the same ...
        query = """
            INSERT INTO netflix_titles (show_id, type, title, director, "cast", country, date_added, release_year, rating, duration, listed_in, description)
            VALUES %s
            ON CONFLICT (show_id) DO NOTHING;
        """
        execute_values(cursor, query, tuples)
        conn.commit()
        print(f"{cursor.rowcount} rows were successfully inserted or skipped.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    load_data()