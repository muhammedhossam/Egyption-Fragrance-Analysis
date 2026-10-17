import re
from numpy import var
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import pandas as pd
from datetime import date

BASE_URL = "https://fixdfragrances.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}


# --------------------------------
# Product page scraping
# --------------------------------

def extract_best_time(soup):
    tag = soup.find("div", class_="fixd-chip fixd-chip--worn")

    if not tag:
        return None

    text = tag.get_text(" ", strip=True)

    # Optional cleanup if the chip contains a label like "Best worn: Night"
    text = re.sub(r"(?i)^best\s*worn\s*:?\s*", "", text).strip()

    return text or None

def extract_projection_score(soup):
    projection_section = soup.find(
        lambda t: t.name in ("div", "section")
        and "projection" in t.get_text(" ", strip=True).lower()
    )

    if not projection_section:
        return None

    active_icons = projection_section.find_all("i", class_="on")

    return len(active_icons)

def extract_longevity_hours(soup):
    time_tag = soup.select_one("div.fixd-chip--time span:nth-of-type(2)")

    if not time_tag:
        return None

    text = time_tag.get_text(" ", strip=True)

    match = re.search(r"\d+", text)

    return int(match.group()) if match else None

def extract_inspired_by(soup):
    """
    Finds an element whose text starts with 'Inspired by' and pulls the
    <strong>/<b> tag inside it (or immediately after it).
    On FIXD product pages this renders as: 'Inspired by: **Name by Brand**'
    """
    tag = soup.find(
        lambda t: t.name in ("p", "div", "span", "h4", "h5", "h6")
        and t.get_text(strip=True).lower().startswith("inspired by")
    )
    if not tag:
        return None

    strong = tag.find(["strong", "b"])
    if strong:
        return strong.get_text(strip=True)

    # fallback: strip the "Inspired by" label off manually
    text = tag.get_text(" ", strip=True)
    return re.sub(r"(?i)^inspired by\s*:?\s*", "", text).strip() or None


def extract_fragrance_notes(soup):
    """
    FIXD shows notes as a Top / Heart / Base breakdown under a
    'Fragrance Notes' heading, e.g.:
        Top    -> Pink Pepper Juniper Violet
        Heart  -> Toffee Cinnamon Lavender Sage
        Base   -> Vanilla Amber Tonka Bean Suede
    Each label's value is kept as a single raw string (same convention as
    the niche_essences script, which stored the raw text after the colon).
    """
    notes = {}

    heading = soup.find(
        lambda t: t.name in ("h2", "h3", "h4", "p")
        and t.get_text(strip=True).lower() == "fragrance notes"
    )
    scope = heading.find_parent() if heading else soup

    for label in ["Top", "Heart", "Base"]:
        label_tag = scope.find(lambda t: t.get_text(strip=True) == label)
        if not label_tag:
            continue

        value_tag = label_tag.find_next_sibling()
        if value_tag is None or not value_tag.get_text(strip=True):
            value_tag = label_tag.find_next()

        if value_tag:
            notes[label.lower() + str("_notes")] = value_tag.get_text(" ", strip=True)

    return notes


def extract_review_count(soup):
    reviews_tag = soup.find("span", class_="jdgm-prev-badge__text")
    if not reviews_tag:
        return 0
    reviews_text = reviews_tag.get_text(strip=True)
    first_word = reviews_text.split(" ")[0]
    return int(first_word) if first_word.isdigit() else 0


def scrape_product(url):
    handle = urlparse(url).path.strip("/").split("/")[-1]

    # --- HTML page: name, "inspired by", notes, review count ---
    response = requests.get(url, headers=HEADERS)
    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    h1 = soup.find("h1")
    product_name = h1.get_text(strip=True) if h1 else None

    inspired_by = extract_inspired_by(soup)
    notes = extract_fragrance_notes(soup)
    review_count = extract_review_count(soup)
    best_time = extract_best_time(soup)
    projection_score = extract_projection_score(soup)
    longevity_hours = extract_longevity_hours(soup)

    if inspired_by is None:
        print(f"  [WARN] Could not find 'Inspired by' for {handle}")
    if not notes:
        print(f"  [WARN] Could not find fragrance notes for {handle}")

    # --- JSON endpoint: variants (size, price, availability, id) ---
    js_response = requests.get(url + ".js", headers=HEADERS)
    js_response.raise_for_status()
    product_json = js_response.json()

    rows = []
    for variant in product_json["variants"]:
        row = dict(notes)
        
        row["variant_id"] = f'{variant["id"]}'
        row["product_id"] = str(handle)
        row["collected_date"] = date.today().isoformat()

        row["size_ml"] = variant["title"].replace("ML", "").replace("ml", "").strip()
        row["product_name"] = product_name
        row["inspired_by"] = inspired_by

        row["price"] = variant["price"] / 100
        row["available"] = variant["available"]
        row["review_count"] = review_count

        row["best_time"] = best_time
        row["projection_score"] = projection_score
        row["longevity_hours"] = longevity_hours

        row["product_url"] = url

        rows.append(row)

    return rows


# --------------------------------
# Product URLs
# --------------------------------

def get_product_urls(collection_handle):
    """
    Primary method: Shopify's built-in /collections/<handle>/products.json
    endpoint. This works the same way regardless of theme/markup, unlike
    scraping product-card link classes (which vary per theme and which I
    could not verify against fixdfragrances.com's raw HTML).
    """
    json_url = f"{BASE_URL}/collections/{collection_handle}/products.json?limit=250"
    try:
        response = requests.get(json_url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        handles = [p["handle"] for p in data.get("products", [])]
        if handles:
            urls = [urljoin(BASE_URL, f"/products/{h}") for h in handles]
            return list(dict.fromkeys(urls))
    except Exception as e:
        print(f"products.json approach failed ({e}), falling back to HTML scrape")

    # --- Fallback: scan <a> tags for /products/ links, stopping once we
    # hit the FAQ section (the footer 'you may also like' search widget
    # sits below the FAQ and would otherwise pollute the results) ---
    collection_url = f"{BASE_URL}/collections/{collection_handle}"
    response = requests.get(collection_url, headers=HEADERS)
    print("Collection Status Code:", response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = []
    for el in soup.find_all(True):
        if el.name in ("h2", "h3") and "frequently asked questions" in el.get_text(strip=True).lower():
            break
        if el.name == "a" and el.get("href") and "/products/" in el["href"]:
            urls.append(urljoin(BASE_URL, el["href"]))

    return list(dict.fromkeys(urls))


# --------------------------------
# Scrape products
# --------------------------------

product_urls = get_product_urls("for-him")
print("Products found:", len(product_urls))

products = []

for i, url in enumerate(product_urls, start=1):
    print(f"Scraping {i}/{len(product_urls)}: {url}")
    variant_rows = scrape_product(url)
    for row in variant_rows:
        print("  ->", row["size_ml"], row["price"])
    products.extend(variant_rows)

df = pd.DataFrame(products)

print(df.shape)
print(df.head())

df.to_csv(
    "/mnt/d/Projects/perfume-market-analysis/data/raw/fixd_fragrances_products_raw.csv",
    index=False,
    encoding="utf-8-sig",
)

print("CSV saved successfully!")