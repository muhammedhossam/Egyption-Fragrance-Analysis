import numpy as np
import pandas as pd


DATA = "/mnt/d/Projects/perfume-market-analysis/data/raw/niche_essences_products_raw.csv"
OUTPUT = "/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/niche_essences_products.csv"


df = pd.read_csv(DATA)
df = df.iloc[:, :-2]
df = df.drop([90,91])
df = df.drop(['middle_notes', 'pair_it_with', 'how_to_layer'],axis=1)
df = df.replace(["For Him", "For Her"], ["male", "female"])
df['size'] = df['size_ml'].astype(float)
df['product_name'] = df.product_name.str.split(' — ', expand=True)[0]
df['id'] = df.variant_id
df['identity'] = df['identity'].str.lower()
df['brand'] = "niche_essence"
df = df.drop(['variant_id','product_id', 'size_ml'], axis = 1 )
df['variant_type'] = 'perfume'
df['size_unit'] = 'ml'
df['price_per_unit'] = df['price'] / df['size']
brands = [
    "Maison Francis Kurkdjian",
    "Jean Paul Gaultier",
    "Yves Saint Laurent",
    "Stéphane Humbert Lucas",
    "Giardini di Toscana",
    "Parfums de Marly",
    "Emporio Armani",
    "Atyab AlSheikh",
    "Maison Crivelli",
    "Giorgio Armani Privé",
    "Louis Vuitton",
    "Orto Parisi",
    "Tom Ford",
    "Xerjoff",
    "Tiziana Terenzi",
    "Montale",
    "Mancera",
    "Kilian",
    "Chanel",
    "Dior",
    "Lattafa",
    "Nishane",
    "Byredo",
    "Ex Nihilo",
    "Creed",
    "Roja",
    "Amouage",
]
brands = sorted(brands, key=len, reverse=True)

def split_brand_product(x):
    if pd.isna(x):
        return pd.Series([None, None])

    x = str(x).strip()

    for brand in brands:
        if x.startswith(brand + " "):
            product = x[len(brand):].strip()
            return pd.Series([brand, product])

    return pd.Series([None, x])


df[['brand_name', 'inspired_by']] = (
    df['inspired_by']
    .apply(split_brand_product)
)



df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print(f"CSV validated successfully: {len(df)} rows, {len(df.columns)} columns")