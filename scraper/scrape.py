# scraper/scrape.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
from config import LAPTOPS_URL, TABLETS_URL

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def _scrape_category_pages(base_url: str, category_name: str) -> List[Dict]:
    """
    Generic pagination scraper: appends ?page=N to the base_url and iterates pages
    until no products are found on a page.
    """
    page = 1
    collected = []

    while True:
        # Many simple test-sites accept ?page=N — we'll try page query param and stop when no products found
        url = f"{base_url}?page={page}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            # try base_url without page param for page 1
            if page == 1:
                resp = requests.get(base_url, headers=HEADERS, timeout=15)
                if resp.status_code != 200:
                    break
            else:
                break

        soup = BeautifulSoup(resp.text, "html.parser")
        products = soup.find_all("div", class_="thumbnail")

        if not products:
            # no more products — stop
            break

        for product in products:
            # Some fields can be missing; use safe gets
            a_title = product.find("a", class_="title")
            title = a_title.get_text(strip=True) if a_title else ""

            price_tag = product.find("h4", class_="price")
            price = price_tag.get_text(strip=True) if price_tag else ""

            desc_tag = product.find("p", class_="description")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            rating = len(product.find_all("span", class_="glyphicon glyphicon-star"))

            link = ""
            if a_title and a_title.get("href"):
                link = urljoin("https://webscraper.io", a_title.get("href"))

            collected.append({
                "title": title,
                "price": price,
                "description": description,
                "rating": rating,
                "link": link,
                "category": category_name
            })

        page += 1

    return collected

def scrape_laptops():
    """Scrape all laptop pages (paginated)."""
    return _scrape_category_pages(LAPTOPS_URL, "laptops")

def scrape_tablets():
    """Scrape all tablets pages (paginated)."""
    return _scrape_category_pages(TABLETS_URL, "tablets")
