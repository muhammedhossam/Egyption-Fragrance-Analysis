import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

BASE_URL = "https://il-vanto.com"
COLLECTION_URL = f"{BASE_URL}/collections/men"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
session.headers.update(HEADERS)


def get_product_urls():
    response = session.get(COLLECTION_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    product_urls = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/products/" in href:
            product_url = urljoin(BASE_URL, href)
            product_urls.add(product_url.split("?")[0])

    return list(product_urls)


def scrape_product(product_url):
    product = {
        "url": product_url
    }

    # -----------------------------
    # Product HTML
    # -----------------------------
    response = session.get(product_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Title
    h1 = soup.find("h1")

    if h1:
        title = h1.get_text(" ", strip=True)
        product["title"] = title.split("-")[0]

        # Example: Devils Litchi - 50 ML
        if "-" in title:
            size = title.rsplit("-", 1)[1].strip()

            if "ML" in size.upper():
                product["size_ml"] = (
                    size.upper()
                    .replace("ML", "")
                    .strip()
                )

    # Price
    sale_price = soup.find("sale-price").contents[-1].get_text(strip = True)

    if sale_price:
        product["price"] = float(sale_price)
    # Rating
    rating = soup.find("a", class_="rating")

    if rating:
        product["rate"] = rating.get_text(
            " ",
            strip=True
        )

    # -----------------------------
    # Metafields
    # -----------------------------
    dd = soup.find_all(
        "div",
        class_="metafield-rich_text_field"
    )

    if len(dd) > 1:

        paragraphs = dd[1].find_all("p")

        for paragraph in paragraphs:

            br = paragraph.find("br")

            if not br:
                continue

            contents = paragraph.contents

            if not contents:
                continue

            key = contents[0].get_text(strip=True)

            key = (
                key
                .replace(":", "")
                .replace(" ", "")
            )

            if br.next_sibling:
                value = str(br.next_sibling).strip()

                value = [
                    x.strip()
                    for x in value.split(",")
                    if x.strip()
                ]

                product[key] = value

    # -----------------------------
    # Shopify .js endpoint
    # -----------------------------
    js_url = product_url.rstrip("/") + ".js"

    js_response = session.get(js_url)
    js_response.raise_for_status()

    product_json = js_response.json()

    product["id"] = str(product_json.get("id"))
    product["inspired_by"] = product_json.get("vendor")
    product["product_name"] = product_json.get("handle")

    return product


# ==========================================
# Get all product URLs
# ==========================================

product_urls = get_product_urls()

print(f"Found {len(product_urls)} products")


# ==========================================
# Scrape products
# ==========================================

products = []

for i, product_url in enumerate(product_urls, start=1):

    try:
        print(
            f"[{i}/{len(product_urls)}] "
            f"{product_url}"
        )

        product = scrape_product(product_url)
        products.append(product)

        time.sleep(0.5)

    except Exception as e:
        print(
            f"ERROR: {product_url}\n"
            f"{e}"
        )


# ==========================================
# Pandas DataFrame
# ==========================================

df = pd.DataFrame(products)

print("\nDataFrame:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# Save CSV
# ==========================================

df.to_csv(
    "/mnt/d/Projects/perfume-market-analysis/data/raw/il_vanto_products_raw.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nSaved {len(df)} products to "
    f"il_vanto_men_products.csv"
)
