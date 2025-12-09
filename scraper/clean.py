# scraper/clean.py
import pandas as pd

def clean_data(raw_data):
    """
    raw_data: list of dicts with fields:
      title, price (string like '$295.99'), description, rating, link, category
    returns: pandas.DataFrame with cleaned/typed columns
    """
    df = pd.DataFrame(raw_data)

    # Ensure columns exist even if empty
    for col in ["title", "price", "description", "rating", "link", "category"]:
        if col not in df.columns:
            df[col] = None

    # Clean price string to float (e.g. "$295.99" -> 295.99)
    # remove $ and commas and whitespace, then convert; non-convertible values become NaN
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(r"[$,]", "", regex=True)
        .str.strip()
    )
    # convert to numeric, errors -> NaN
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # rating ensure int (if missing, fill with 0)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0).astype(int)

    # Optional: drop duplicates (same title & link)
    df = df.drop_duplicates(subset=["title", "link"])

    # Sort by price (NaN will be at end)
    df = df.sort_values(by="price", na_position="last").reset_index(drop=True)

    return df
