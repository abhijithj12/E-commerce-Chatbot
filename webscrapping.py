import sqlite3
import re
import time
import requests
from bs4 import BeautifulSoup
from config import DB_PATH


def get_connection():
    """Get database connection"""
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)


def init_db():
    """Create products table if it doesn't exist"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            url TEXT UNIQUE,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def clear_products():
    """Clear all products from database"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM products")
    conn.commit()
    conn.close()


def insert_product(name, price, url):
    """Insert a product into database"""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT OR IGNORE INTO products (name, price, url, timestamp)
            VALUES (?, ?, ?, datetime('now'))
        """, (name, price, url))
    except Exception as e:
        print(f"Insert error: {e}")

    conn.commit()
    conn.close()


# -------------------- PRICE FILTER HELPERS --------------------
def extract_max_price(text):
    """Extract max price from query like 'laptops under 50000'"""
    match = re.search(r"(under|below)\s*₹?(\d+)", text, re.IGNORECASE)
    return int(match.group(2)) if match else None


def clean_search_text(text):
    """Remove price part from query"""
    return re.sub(r"(under|below)\s*₹?\d+", "", text, flags=re.IGNORECASE).strip()


# -------------------- SCRAPING HELPERS --------------------
def clean_price(price_text):
    """Extract price number from text"""
    match = re.search(r"₹\s?([\d,]+)", price_text)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def get_title(card):
    """Get product title from card"""
    # Try title attribute first
    tag = card.find("a", attrs={"title": True})
    if tag:
        return tag["title"].strip()

    # Try common class names
    candidates = ["_4rR01T", "s1Q9rs", "IRpwTa", "KzDlHZ", "wjcEIp", "WKTcLC"]
    for cls in candidates:
        t = card.find("div", class_=cls)
        if t:
            return t.get_text(strip=True)

    # Get longest text block as last resort
    text_blocks = [t.strip() for t in card.stripped_strings if len(t.strip()) > 10]
    return max(text_blocks, key=len) if text_blocks else None


def get_price(card):
    """Get product price from card"""
    tag = card.find(lambda t: t.name in ["div", "span"] and "₹" in t.get_text())
    return clean_price(tag.get_text()) if tag else None


def get_link(card):
    """Get product link from card"""
    a = card.find("a", href=True)
    if a:
        href = a["href"]
        return "https://www.flipkart.com" + href if href.startswith("/") else href
    return None


# -------------------- MAIN SCRAPER --------------------
def scrap(query, max_price=None, pages=2):
    """
    Scrape products from Flipkart
    NOTE: Web scraping may violate website terms of service
    Use official APIs when possible
    """

    init_db()
    clear_products()

    # Full browser-like headers to avoid 403 block
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

    # Start a session to persist cookies across requests (helps avoid blocks)
    session = requests.Session()
    session.headers.update(headers)

    # Warm up the session by visiting Flipkart homepage first
    try:
        session.get("https://www.flipkart.com", timeout=10)
        time.sleep(1)
    except Exception:
        pass

    products_found = 0

    for page in range(1, pages + 1):
        url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}&page={page}"
        print(f"Scraping page {page}...")

        try:
            resp = session.get(url, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")

            # Primary selector
            cards = soup.find_all("div", attrs={"data-id": True})

            # Fallback selectors for newer Flipkart layout
            if not cards:
                cards = soup.find_all("div", class_="_1AtVbE")
            if not cards:
                cards = soup.find_all("div", class_="tUxRFH")

            print(f"Found {len(cards)} cards on page {page}")

            for card in cards:
                name = get_title(card)
                price = get_price(card)
                link = get_link(card)

                if not (name and price and link):
                    continue

                if max_price is not None and price > max_price:
                    continue

                insert_product(name, price, link)
                products_found += 1

            # Small delay between pages to avoid rate limiting
            time.sleep(1)

        except requests.Timeout:
            print(f"Timeout on page {page}")
            continue
        except requests.RequestException as e:
            print(f"Error scraping page {page}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            continue

    print(f"Scraping completed! Found {products_found} products")
    return products_found