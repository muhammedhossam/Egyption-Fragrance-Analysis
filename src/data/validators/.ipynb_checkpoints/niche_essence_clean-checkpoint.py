import pandas as pd

DATA = "/mnt/d/Projects/perfume-market-analysis/data/raw/niche_essences_products_raw.csv"
OUTPUT = "/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/niche_essences_products.csv"

df = pd.read_csv(DATA)

# -------------------------
# 1. Basic validation
# -------------------------

required_columns = [    
    "product_id",
    "variant_id",
    "product_name",
    "size_ml",
    "price",
    "product_url",
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")


# -------------------------
# 2. Remove completely empty columns
# -------------------------

df = df.dropna(axis=1, how="all")


# -------------------------
# 3. Remove rows with no fragrance information
# -------------------------

fragrance_columns = [
    "fragrance_family",
    "top_notes",
    "heart_notes",
    "base_notes",
]

existing_fragrance_columns = [
    col for col in fragrance_columns if col in df.columns
]

if existing_fragrance_columns:
    df = df.dropna(
        subset=existing_fragrance_columns,
        how="all"
    )


# -------------------------
# 4. Convert numeric fields
# -------------------------

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["size_ml"] = pd.to_numeric(df["size_ml"], errors="coerce")


# -------------------------
# 5. Validate numeric values
# -------------------------

if (df["price"] <= 0).any():
    print("WARNING: Found non-positive prices")

if (df["size_ml"] <= 0).any():
    print("WARNING: Found non-positive sizes")


# -------------------------
# 6. Price per ml
# -------------------------

df["price_per_ml"] = df["price"] / df["size_ml"]


# -------------------------
# 7. Add source/brand
# -------------------------

df["brand"] = "niche_essence"


# -------------------------
# 8. Final validation
# -------------------------

if df["product_id"].isna().any():
    print("WARNING: Missing product IDs")

if df["product_name"].isna().any():
    print("WARNING: Missing product names")

if df["product_url"].isna().any():
    print("WARNING: Missing product URLs")

if df["price_per_ml"].isna().any():
    print("WARNING: Some rows have invalid price/size")


# -------------------------
# 9. Save
# -------------------------

df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print(f"CSV validated successfully: {len(df)} rows, {len(df.columns)} columns")