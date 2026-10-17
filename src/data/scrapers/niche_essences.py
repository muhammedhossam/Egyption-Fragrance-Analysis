import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import pandas as pd
from datetime import date


def scrape_product(url):
    handle = urlparse(url).path.strip("/").split("/")[-1]

    # --- HTML page: name, "inspired by", notes, review count ---
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    product_name = soup.find("h1").get_text(strip=True)

    inspired_by_tag = soup.find("strong")
    inspired_by = inspired_by_tag.get_text(strip=True) if inspired_by_tag else None

    reviews_tag = soup.find("span", class_="jdgm-prev-badge__text")
    if reviews_tag:
        reviews_text = reviews_tag.get_text(strip=True)
        first_word = reviews_text.split(" ")[0]
        review_count = int(first_word) if first_word.isdigit() else 0
    else:
        review_count = 0

    notes = {}
    scent_notes_raw = soup.find_all("div", class_="accordion__content prose")
    for section in scent_notes_raw:
        for p in section.find_all("p"):
            text = p.get_text(" ", strip=True)
            if ":" not in text:
                continue
            key, value = text.split(":", 1)
            key = key.strip().lower().replace(" ", "_")
            notes[key] = value.strip()

    # --- JSON endpoint: variants (size, price, availability, id) ---
    js_response = requests.get(url + ".js", headers={"User-Agent": "Mozilla/5.0"})
    js_response.raise_for_status()
    product_json = js_response.json()

    rows = []
    for variant in product_json["variants"]:
        row = dict(notes)  # copy so each variant gets its own dict
        row["product_id"] = str(handle)
        row["variant_id"] = f'{variant["id"]}'
        row["collected_date"] = date.today().isoformat()
        row["size_ml"] = variant["title"].replace("ml", "").strip()
        row["product_name"] = product_name
        row["inspired_by"] = inspired_by
        row["price"] = variant["price"] / 100
        row["available"] = variant["available"]
        row["review_count"] = review_count
        row["product_url"] = url
        rows.append(row)

    return rows


# --------------------------------
# Product URLs
# --------------------------------

BASE_URL = "https://nicheessences.com"


def get_product_urls(collection_url):
    response = requests.get(collection_url, headers={"User-Agent": "Mozilla/5.0"})
    print("Collection Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    product_links = soup.find_all("a", class_="product-card__media", href=True)

    product_urls = [urljoin(BASE_URL, link["href"]) for link in product_links]

    return list(dict.fromkeys(product_urls))


# --------------------------------
# Scrape products
# --------------------------------

page_1 = get_product_urls("https://nicheessences.com/collections/men?page=1")
page_2 = get_product_urls("https://nicheessences.com/collections/men?page=2")

product_urls = list(dict.fromkeys(page_1 + page_2))
print("Products found:", len(product_urls))

products = []

for i, url in enumerate(product_urls, start=1):
    print(f"Scraping {i}/{len(product_urls)}")
    variant_rows = scrape_product(url)
    for row in variant_rows:
        print("  ->", row["size_ml"], row["price"])
    products.extend(variant_rows)

df = pd.DataFrame(products)

print(df.shape)
print(df.head())

df.to_csv(
    "/mnt/d/Projects/perfume-market-analysis/data/raw/niche_essences_products_raw.csv",
    index=False,
    encoding="utf-8-sig",
)

print("CSV saved successfully!")