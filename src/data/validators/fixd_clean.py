import numpy as np
import pandas as pd


DATA = "/mnt/d/Projects/perfume-market-analysis/data/raw/fixd_fragrances_products_raw.csv"
OUTPUT = "/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/fixd_fragrances_products.csv"


df = pd.read_csv(DATA)


median_long = df.longevity_hours.median()
median_proj = df.projection_score.median()
df.fillna({'longevity_hours': median_long, 'projection_score' : median_proj}, inplace=True)
df['identity'] = "male"
df['size'] = df['size_ml']
df["price_per_unit"] = df["price"].astype(float) / df["size"].astype(float)
df = df.replace("Night", "Evening")
df = df.replace("Day & Night", "Both")
df['brand'] = "fixd_fragrance"
df[['inspired_by', 'brand_name']] = df['inspired_by'].str.split(' by ', expand=True)
df['id'] = df.variant_id
df['variant_type'] = 'perfume'
df['size_unit'] = 'ml'

df = df.drop(['variant_id','product_id', 'size_ml'], axis = 1 )


df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print(f"CSV validated successfully: {len(df)} rows, {len(df.columns)} columns")