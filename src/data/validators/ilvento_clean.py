import pandas as pd
import numpy as np
from datetime import date


DATA = "/mnt/d/Projects/perfume-market-analysis/data/raw/il_vanto_products_raw.csv"
OUTPUT = "/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/il_vanto_products.csv"


df = pd.read_csv(DATA)


df['price']=df['price'].str.replace(',',"").astype(float)
df['product_url'] = df['url']
df['product_id'] = df['id']
df.drop(['title', 'url', 'id', 'Ingredients'], axis=1, inplace=True)
df[['inspired_by','brand_name']] = df['inspired_by'].str.split(r'\s+-\s+|\s+—\s+|\s+–', n=1, expand=True)
df['identity'] = 'male'
df['size'] = df['size_ml']
df["price_per_unit"] = df["price"].astype(float) / df["size"].astype(float)
df['collected_date'] = date.today()
df['brand_name'] = df['brand_name'].str.strip()
df['brand'] = "il_vento"
df['id'] = df.product_id
df['variant_type'] = 'perfume'
df['size_unit'] = 'ml'
df = df.drop(['product_id', 'size_ml'], axis = 1 )


df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print(f"CSV validated successfully: {len(df)} rows, {len(df.columns)} columns")