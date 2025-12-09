# streamlit_app.py
import streamlit as st
import pandas as pd
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, DEFAULT_DISPLAY_ROWS

st.set_page_config(page_title="Scraper Dashboard", layout="wide")

def get_conn():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

@st.cache_data
def load_table(table_name):
    conn = get_conn()
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name} ORDER BY scraped_at DESC", conn)
    finally:
        conn.close()
    return df

st.title("Webscraper Test Site — Dashboard")

# Choose table
table_choice = st.sidebar.selectbox("Select table to view", ("laptops", "tablets"))

df = load_table(table_choice)

st.markdown(f"### `{table_choice}` — {len(df)} rows")

# Basic filters
col1, col2 = st.columns(2)
with col1:
    min_price = st.number_input("Min price", value=0.0, step=1.0)
with col2:
    max_price = st.number_input("Max price (0 = no max)", value=0.0, step=1.0)

filtered = df.copy()
if max_price > 0:
    filtered = filtered[(filtered["price"].notna()) & (filtered["price"] >= min_price) & (filtered["price"] <= max_price)]
else:
    filtered = filtered[(filtered["price"].notna()) & (filtered["price"] >= min_price)]


st.write(f"Showing {len(filtered)} rows after filters")

# Show table
st.dataframe(filtered.head(DEFAULT_DISPLAY_ROWS))

# Details / download
if st.button("Download filtered CSV"):
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name=f"{table_choice}_export.csv", mime="text/csv")

