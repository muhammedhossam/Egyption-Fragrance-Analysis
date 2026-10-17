import pandas as pd
import numpy as np
from datetime import date

DATA = "/mnt/d/Projects/perfume-market-analysis/data/raw/brojal_khalij_products_raw.csv"
OUTPUT = "/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/brojal_khalij_products.csv"


df = pd.read_csv(DATA)

df['product_name'] = df['inspired_by']= df['product_name'].str.split('|', n=1,expand=True)[0]
df['identity'] = 'male'
df.loc[df['size_unit'].isna(), 'size_unit'] = 'gram'
df['size_value'] = df['size_value'].str.split('~',expand=True)[0]
df['size_value'] = df['size_value'].str.split('-',expand=True)[0]
df['size'] = df['size_value'].astype(float)

df['price_per_unit'] = df['price'] / df['size']
df = df.drop(["price_currency", 'size_value'], axis=1)
df['collected_date'] = date.today()
df['product_name'] = df['product_name'].str.strip()
df['id'] = df.product_id

df['inspired_by'] = df['inspired_by'].str.strip()
df = df.drop(['variant_id','product_id', 'size_raw'], axis = 1 )


df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print(f"CSV validated successfully: {len(df)} rows, {len(df.columns)} columns")