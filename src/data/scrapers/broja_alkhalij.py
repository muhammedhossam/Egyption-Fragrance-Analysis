import requests
import pandas as pd
import re
import time
import random

from bs4 import BeautifulSoup
from datetime import date


BASE_URL = "https://brojalkhalij.com/en"
COLLECTION_URL = f"{BASE_URL}/collections/men"
OUTPUT = "data/raw/brojal_khalij_products_raw.csv"


# ==========================================================
# SESSION
# ==========================================================

def build_session():

    s = requests.Session()

    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
        "Referer": BASE_URL,
    })

    return s


session = build_session()

# Timeout as (connect_timeout, read_timeout). Some pages on this store
# are just slow to respond, so give the read side more room than a
# flat 30s.
REQUEST_TIMEOUT = (10, 45)

# After this many consecutive request failures (across products), the
# session gets rebuilt from scratch - helps if the store is
# fingerprinting/soft-blocking the session rather than just being slow.
SESSION_REFRESH_AFTER = 3
consecutive_failures = 0


# ==========================================================
# REQUEST JSON WITH RETRIES
# ==========================================================

def get_json(url, max_retries=6):

    global session, consecutive_failures

    for attempt in range(max_retries):

        try:

            response = session.get(
                url,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                consecutive_failures = 0
                return response.json()

            if response.status_code == 429:

                retry_after = response.headers.get(
                    "Retry-After"
                )

                if retry_after:
                    wait = int(retry_after)
                else:
                    wait = min(
                        60,
                        (2 ** attempt) +
                        random.uniform(1, 3)
                    )

                print(
                    f"429 - waiting {wait:.1f}s"
                )

                time.sleep(wait)

                continue

            response.raise_for_status()

        except requests.RequestException as e:

            consecutive_failures += 1

            if attempt == max_retries - 1:
                raise

            wait = min(
                60,
                (2 ** attempt) +
                random.uniform(1, 3)
            )

            print(f"Request error for {url}: {e}")
            print(f"Retrying in {wait:.1f}s")

            if consecutive_failures >= SESSION_REFRESH_AFTER:
                print("Too many consecutive failures - refreshing session")
                session = build_session()
                consecutive_failures = 0

            time.sleep(wait)

    raise RuntimeError(
        f"Failed to retrieve {url}"
    )


# ==========================================================
# GET HTML WITH RETRIES
# ==========================================================

def get_html(url, max_retries=6):

    global session, consecutive_failures

    for attempt in range(max_retries):

        try:

            response = session.get(
                url,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                consecutive_failures = 0
                return response.text

            if response.status_code == 429:

                retry_after = response.headers.get(
                    "Retry-After"
                )

                if retry_after:
                    wait = int(retry_after)
                else:
                    wait = min(
                        60,
                        (2 ** attempt) +
                        random.uniform(1, 3)
                    )

                print(
                    f"429 HTML - waiting {wait:.1f}s"
                )

                time.sleep(wait)

                continue

            response.raise_for_status()

        except requests.RequestException as e:

            consecutive_failures += 1

            if attempt == max_retries - 1:
                raise

            wait = min(
                60,
                (2 ** attempt) +
                random.uniform(1, 3)
            )

            print(f"HTML request error for {url}: {e}")
            print(f"Retrying in {wait:.1f}s")

            if consecutive_failures >= SESSION_REFRESH_AFTER:
                print("Too many consecutive failures - refreshing session")
                session = build_session()
                consecutive_failures = 0

            time.sleep(wait)

    raise RuntimeError(
        f"Failed to retrieve HTML: {url}"
    )


# ==========================================================
# NOTES
# ==========================================================

def extract_notes(body_html):

    soup = BeautifulSoup(
        body_html or "",
        "html.parser"
    )

    notes = {
        "top_notes": None,
        "heart_notes": None,
        "base_notes": None
    }

    for element in soup.find_all(
        ["p", "div"]
    ):

        text = element.get_text(
            " ",
            strip=True
        )

        if text.startswith("Top:"):

            notes["top_notes"] = (
                text
                .replace("Top:", "", 1)
                .strip()
            )

        elif text.startswith("Heart:"):

            notes["heart_notes"] = (
                text
                .replace("Heart:", "", 1)
                .strip()
            )

        elif text.startswith("Base:"):

            notes["base_notes"] = (
                text
                .replace("Base:", "", 1)
                .strip()
            )

    return notes


# ==========================================================
# FIND TEXT AFTER A HEADING
# ==========================================================

def extract_after_heading(
    soup,
    heading
):
    """
    Find a section containing a heading such as:

        When to use it
        Longevity
        Projection

    and extract the useful text/value following it.
    """

    text_nodes = soup.find_all(
        string=lambda text:
        text and heading in text.strip()
    )

    for node in text_nodes:

        parent = node.parent

        # Look around the heading
        candidates = []

        if parent:
            candidates.extend(
                parent.find_all_next(
                    limit=5
                )
            )

        for element in candidates:

            text = element.get_text(
                " ",
                strip=True
            )

            if (
                text
                and heading not in text
                and len(text) < 200
            ):
                return text

    return None






# ==========================================================
# IDENTITY
# ==========================================================

def parse_identity(
    product_type,
    tags
):

    if product_type == "perfume-male":
        return "For Him"

    if "رجالي" in tags:
        return "For Him"

    return None


# ==========================================================
# SIZE
# ==========================================================

def parse_size(size_raw):

    text = (
        size_raw or ""
    ).lower().strip()

    if "مل" in text or "ml" in text:
        unit = "ml"

    elif "جرام" in text:
        unit = "gram"

    else:
        unit = None

    match = re.search(
        r"(\d+(?:\.\d+)?(?:\s*[~\-]\s*\d+(?:\.\d+)?)?)",
        text
    )

    size_value = (
        match.group(1)
        if match
        else None
    )

    if "Tester" in text:

        variant_type = "tester"

    elif "Body Splash" in text:

        variant_type = "body_splash"

    elif "Half Tola" in text:

        variant_type = "half_tola"

    elif "tola" in text:

        variant_type = "tola"

    else:

        variant_type = "perfume"

    return (
        size_value,
        unit,
        variant_type
    )


# ==========================================================
# SCRAPE PRODUCT
# ==========================================================

def scrape_product(handle):

    # ------------------------------------------------------
    # 1. Shopify JSON
    # ------------------------------------------------------

    json_url = (
        f"{BASE_URL}/products/"
        f"{handle}.json"
    )

    data = get_json(
        json_url
    )

    product = data["product"]

    # ------------------------------------------------------
    # 2. Main HTML
    # ------------------------------------------------------

    html_url = (
        f"{COLLECTION_URL}/products/"
        f"{handle}"
    )

    html = get_html(
        html_url
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # ------------------------------------------------------
    # Product information
    # ------------------------------------------------------

    product_id = str(f"{product["id"]}")

    product_name = product["title"]

    vendor = product.get(
        "vendor"
    )

    product_type = product.get(
        "product_type"
    )

    tags = product.get(
        "tags",
        []
    )

    body_html = product.get(
        "body_html",
        ""
    )

    # ------------------------------------------------------
    # Fragrance information
    # ------------------------------------------------------

    identity = parse_identity(
        product_type,
        tags
    )


    # ------------------------------------------------------
    # Variants
    # ------------------------------------------------------

    rows = []

    for variant in product.get(
        "variants",
        []
    ):

        variant_id = str(f"{variant["id"]}")

        size_raw = variant.get(
            "title"
        )

        (
            size_value,
            size_unit,
            variant_type
        ) = parse_size(
            size_raw
        )

        # Price
        price = (
            float(variant["price"])
            if variant.get("price")
            else None
        )


        row = {

            "brand": vendor,

            "product_id": product_id,

            "variant_id": variant_id,

            "product_name": product_name,

            "inspired_by": product.get(
                "handle"
            ),

            "size_raw": size_raw,

            "size_value": size_value,

            "size_unit": size_unit,

            "variant_type": variant_type,

            "price": price,

            "price_currency": variant.get(
                "price_currency"
            ),

            "available": True,

            "identity": identity,

            "product_url": html_url,

            "collected_date": (
                date.today().isoformat()
            )
        }

        rows.append(row)

    return rows


# ==========================================================
# GET PRODUCT HANDLES
# ==========================================================

def get_product_handles():

    url = (
        f"{COLLECTION_URL}"
        f"/products.json?limit=250"
    )

    data = get_json(
        url
    )

    return [
        product["handle"]
        for product in data["products"]
    ]


# ==========================================================
# MAIN
# ==========================================================

def main():

    handles = get_product_handles()

    print(
        f"Found {len(handles)} products\n"
    )

    all_rows = []

    for i, handle in enumerate(
        handles,
        start=1
    ):

        print(
            f"Scraping {i}/{len(handles)}: "
            f"{handle}"
        )

        try:

            rows = scrape_product(
                handle
            )

            all_rows.extend(
                rows
            )

            print(
                f"  -> {len(rows)} variants"
            )

        except Exception as e:

            print(
                f"ERROR: {handle} "
                f"({type(e).__name__}) - skipping"
            )

            print(e)

        # Slow down requests
        wait = random.uniform(
            5,
            10
        )

        print(
            f"Waiting {wait:.1f}s..."
        )

        time.sleep(wait)

    # ------------------------------------------------------
    # DataFrame
    # ------------------------------------------------------

    df = pd.DataFrame(
        all_rows
    )

    # Keep IDs as strings
    df["product_id"] = (
        df["product_id"]
        .astype(str)
    )

    df["variant_id"] = (
        df["variant_id"]
        .astype(str)
    )

    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    df.to_csv(
        OUTPUT,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n" + "=" * 50)
    print("FINISHED")
    print("=" * 50)

    print(
        f"Rows: {len(df)}"
    )

    print(
        f"Products: "
        f"{df['product_id'].nunique()}"
    )

    print(
        f"Variants: "
        f"{df['variant_id'].nunique()}"
    )

    print(
        f"Saved to: {OUTPUT}"
    )


if __name__ == "__main__":
    main()