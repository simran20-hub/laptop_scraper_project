# scraper/save_mysql.py
import mysql.connector
from mysql.connector import errorcode
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

TABLE_SCHEMAS = {
    "laptops": """
        CREATE TABLE IF NOT EXISTS laptops (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            price FLOAT,
            description TEXT,
            rating INT,
            link VARCHAR(300),
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "tablets": """
        CREATE TABLE IF NOT EXISTS tablets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            price FLOAT,
            description TEXT,
            rating INT,
            link VARCHAR(300),
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
}

def _get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def save_to_mysql(df, table_name="laptops"):
    """
    Save a DataFrame to a given table name. Creates the table if necessary.
    df: pandas DataFrame with columns: title, price, description, rating, link, category (category optional)
    table_name: string, either 'laptops' or 'tablets'
    """
    if table_name not in TABLE_SCHEMAS:
        raise ValueError(f"Unknown table_name '{table_name}'. Allowed: {list(TABLE_SCHEMAS.keys())}")

    conn = _get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(TABLE_SCHEMAS[table_name])
    except mysql.connector.Error as err:
        print("Error creating table:", err)
        conn.close()
        raise

    # Prepare insert statement
    insert_sql = f"""
        INSERT INTO {table_name} (title, price, description, rating, link)
        VALUES (%s, %s, %s, %s, %s)
    """

    # Insert rows (iterate)
    rows_inserted = 0
    for _, row in df.iterrows():
        # guard: ensure title isn't null
        title = row.get("title", "")
        price = None if pd_is_nan(row.get("price")) else float(row.get("price")) if row.get("price") is not None else None
        description = row.get("description", "")
        rating = int(row.get("rating")) if row.get("rating") is not None else 0
        link = row.get("link", "")

        try:
            cursor.execute(insert_sql, (title, price, description, rating, link))
            rows_inserted += 1
        except mysql.connector.Error as err:
            print("Insert error:", err)
            # continue inserting other rows

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {rows_inserted} rows into `{table_name}`")


# Small helper to check NaN without importing pandas in the top-level (to keep dependency light)
def pd_is_nan(x):
    try:
        import math
        return x is None or (isinstance(x, float) and math.isnan(x))
    except Exception:
        return x is None
