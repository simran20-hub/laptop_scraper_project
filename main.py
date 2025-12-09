# main.py
from scraper.scrape import scrape_laptops, scrape_tablets
from scraper.clean import clean_data
from scraper.save_mysql import save_to_mysql

def run_category(scrape_fn, table_name):
    print(f"Scraping {table_name}...")
    raw = scrape_fn()

    print("Cleaning data...")
    df = clean_data(raw)
    print(f"Found {len(df)} items in {table_name}.")
    # optionally print top rows
    print(df.head(5).to_dict(orient="records"))

    print(f"Saving to MySQL table `{table_name}`...")
    save_to_mysql(df, table_name)
    print("Saved.\n")

if __name__ == "__main__":
    # run laptops
    run_category(scrape_laptops, "laptops")
    # run tablets
    run_category(scrape_tablets, "tablets")

    print("✔ Project Completed Successfully!")
