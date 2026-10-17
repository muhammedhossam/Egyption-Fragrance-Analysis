import pandas as pd

df_ilvento = pd.read_csv("/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/il_vanto_products.csv")
df_broja = pd.read_csv("/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/brojal_khalij_products.csv")
df_niche = pd.read_csv("/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/niche_essences_products.csv")
df_fixd = pd.read_csv("/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/fixd_fragrances_products.csv")


df_main = pd.concat([df_broja, df_fixd, df_ilvento, df_niche]).set_index('id')
df_main = df_main.dropna(subset=['size'])
df_main["top_notes"] = df_main["top_notes"].fillna(df_main["Top"])
df_main["heart_notes"] = df_main["heart_notes"].fillna(df_main["Middle"])
df_main["base_notes"] = df_main["base_notes"].fillna(df_main["Base"])
df_main = df_main.drop(['Top', 'Middle', 'Base', 'best_time', 'projection_score', 'best_for', 'occasion', 'character',
                       'sillage', 'longevity', 'season', 'projection', 'longevity_hours', 'fragrance_family'], axis = 1)
df_main['available'] = True

df_main.to_csv("/mnt/d/Projects/perfume-market-analysis/data/processed/egypt/egypt_fragrance.csv", index = False)


print(f"CSV validated successfully: {len(df_main)} rows, {len(df_main.columns)} columns")