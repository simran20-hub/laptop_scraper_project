# Laptop & Tablet Web Scraper Project

A beginner-friendly Python project that scrapes laptop and tablet data from a test e-commerce website, cleans it, stores it in a MySQL database, and displays the data using a Streamlit dashboard.

---

## 📝 Project Overview
This project automatically collects product data (like name, price, description, and links) from the **WebScraper.io test e-commerce site**. The data is cleaned, structured using pandas, saved to a MySQL database, and visualized through a simple dashboard. This project is great for hands-on experience of Web scraping.

---

## ✨ Features

- Scrapes **Laptops** and **Tablets** with pagination    
- Stores cleaned data into **MySQL tables** (laptops & tablets)  
- Streamlit dashboard to:
  - View scraped data
  - Filter by price
  - Download filtered results as CSV

---

## 🛠 Tech Stack

- **Python 3.10**
- **BeautifulSoup4** – Web scraping  
- **Requests** – Fetching HTML  
- **Pandas** – Data cleaning  
- **MySQL Connector** – Database operations  
- **Streamlit** – Dashboard UI  
- **Conda** – Virtual environment

- ---

## 📁 Project Structure

laptop_scraper_project/
│
├── main.py
├── config.py # (ignored in git)
├── requirements.txt
├── streamlit_app.py
│
├── scraper/
│ ├── scrape.py
│ ├── clean.py
│ └── save_mysql.py
│
└── .gitignore

---

### ▶️ How to Run the Project

---
### Create a Virtual env using venv/conda. Activate the env and then proceed as follows:
---

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Database
```bash
CREATE DATABASE electronic_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Add your database credentials in **Config.py**
(This file is ignored in Git to keep credentials private.)

### 4. Run the scraper
```bash
python main.py
```

### 5. Start the Streamlit dashboard
```bash
streamlit run streamlit_app.py
```



