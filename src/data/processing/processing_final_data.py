import pandas as pd

path = "/mnt/d/Projects/perfume-market-analysis/data/processed/"
df_egy = pd.read_csv(path + "egypt/egypt_fragrance.csv")
df_frag = pd.read_csv(path + "fragrantica/fra_cleaned.csv", encoding="cp1252", sep=";", engine="python")

df_frag['Rating Value'] = df_frag['Rating Value'].str.replace(',', '.').astype(float)
df_frag = df_frag[df_frag['Rating Value'] >= 3.79]
df_frag = df_frag[df_frag['Rating Count'] >= 160]
df_frag = df_frag[df_frag['Gender'] != 'women']
df_frag = df_frag[df_frag['Perfume'].str.len() != 1]
df_frag = df_frag[df_frag['Perfume'].str.len() != 2]
df_frag = df_frag[df_frag['Perfume'].str.lower() != 'intense']
df_frag = df_frag[df_frag['Perfume'].str.lower() != 'uomo']
df_frag = df_frag[df_frag['Perfume'].str.lower() != 'homme']
df_frag = df_frag[df_frag['Perfume'].str.lower() != 'l-homme']
df_frag = df_frag[df_frag['Perfume'].str.lower() != 'oud']
df_frag = df_frag[df_frag['Perfume'].str.lower() != 'noir']




df_egy['inspired_by_key'] = df_egy['inspired_by'].str.replace(r'[^a-zA-Z0-9]+', "-",regex=True).str.lower()
df_merge = df_egy.merge(df_frag[['Perfume','Brand','Top','Middle', 'Base', 'Perfumer1', 'mainaccord1', 'mainaccord2', 'mainaccord3']],
                how='left',
                left_on='inspired_by_key',
                right_on='Perfume')



df_merge.loc[~df_merge['Top'].isna(), 'matched_type'] = 'exact'

for i, row in df_merge[df_merge['matched_type'].isnull()].iterrows():
    matches_rows = df_frag[df_frag['Perfume'].apply(lambda x: x.lower() in row['inspired_by_key'].lower())]
    # print(matches_rows['Perfume'])
    if not matches_rows.empty:
        df_merge.loc[i, 'matched_type'] = 'partial'
        df_merge.loc[i, 'Perfume'] = matches_rows['Perfume'].values[0]
        df_merge.loc[i, 'Brand'] = matches_rows['Brand'].values[0]
        df_merge.loc[i, 'Top'] = matches_rows['Top'].values[0]
        df_merge.loc[i, 'Middle'] = matches_rows['Middle'].values[0]
        df_merge.loc[i, 'Base'] = matches_rows['Base'].values[0]
        df_merge.loc[i, 'Perfumer1'] = matches_rows['Perfumer1'].values[0]
        df_merge.loc[i, 'mainaccord1'] = matches_rows['mainaccord1'].values[0]
        df_merge.loc[i, 'mainaccord2'] = matches_rows['mainaccord2'].values[0]
        df_merge.loc[i, 'mainaccord3'] = matches_rows['mainaccord3'].values[0]



df_merge['local_brand'] = df_merge['brand']
df_merge = df_merge.drop(['brand_name', 'brand', 'top_notes', 'heart_notes', 'base_notes'], axis=1)

df_merge.to_csv(path + "egypt/egypt_fragrance_merged.csv", index=False)