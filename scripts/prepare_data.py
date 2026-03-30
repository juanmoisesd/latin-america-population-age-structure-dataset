import pandas as pd
import numpy as np
import os
import json

ISO3_MAP = {
    "Argentina": "ARG", "Bolivia": "BOL", "Brasil": "BRA", "Chile": "CHL",
    "Colombia": "COL", "Costa Rica": "CRI", "Cuba": "CUB", "Ecuador": "ECU",
    "El Salvador": "SLV", "Guatemala": "GTM", "Honduras": "HND", "México": "MEX",
    "Nicaragua": "NIC", "Panamá": "PAN", "Paraguay": "PRY", "Perú": "PER",
    "República Dominicana": "DOM", "Uruguay": "URY", "Venezuela": "VEN",
}

REGION_MAP = {
    "Argentina": "Sudamérica", "Bolivia": "Sudamérica", "Brasil": "Sudamérica",
    "Chile": "Sudamérica", "Colombia": "Sudamérica", "Costa Rica": "Centroamérica",
    "Cuba": "Caribe", "Ecuador": "Sudamérica", "El Salvador": "Centroamérica",
    "Guatemala": "Centroamérica", "Honduras": "Centroamérica", "México": "Norteamérica",
    "Nicaragua": "Centroamérica", "Panamá": "Centroamérica", "Paraguay": "Sudamérica",
    "Perú": "Sudamérica", "República Dominicana": "Caribe", "Uruguay": "Sudamérica",
    "Venezuela": "Sudamérica",
}

def estimate_median_age(row):
    pct_cols = [
        "Pct_0_4", "Pct_5_9", "Pct_10_14", "Pct_15_19", "Pct_20_24",
        "Pct_25_29", "Pct_30_34", "Pct_35_39", "Pct_40_44", "Pct_45_49",
        "Pct_50_54", "Pct_55_59", "Pct_60_64", "Pct_65_69", "Pct_70_mas"
    ]
    age_bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 90]
    cumulative_pct = 0
    for i, col in enumerate(pct_cols):
        val = row[col]
        if pd.isna(val) or val <= 0: continue
        if cumulative_pct + val >= 50:
            low_age, high_age = age_bins[i], age_bins[i+1]
            return round(low_age + ((50 - cumulative_pct) / val) * (high_age - low_age), 1)
        cumulative_pct += val
    return 30.0

def main():
    cols = ['País', 'Año', 'Sexo', 'Pob_Total_Millones', 'Tasa_Urbanización',
            'TFT', 'Esperanza_Vida', 'Mort_Inf_1k', 'Migr_Neta_k', 'Densidad_Poblacional', 'Ind_Dependencia',
            'Pct_0_4', 'Pct_5_9', 'Pct_10_14', 'Pct_15_19', 'Pct_20_24',
            'Pct_25_29', 'Pct_30_34', 'Pct_35_39', 'Pct_40_44', 'Pct_45_49',
            'Pct_50_54', 'Pct_55_59', 'Pct_60_64', 'Pct_65_69', 'Pct_70_mas',
            'Pob_0_4_k', 'Pob_5_9_k', 'Pob_10_14_k', 'Pob_15_19_k', 'Pob_20_24_k',
            'Pob_25_29_k', 'Pob_30_34_k', 'Pob_35_39_k', 'Pob_40_44_k', 'Pob_45_49_k',
            'Pob_50_54_k', 'Pob_55_59_k', 'Pob_60_64_k', 'Pob_65_69_k', 'Pob_70_mas_k',
            'Fuente']

    df = pd.read_csv('data/dataset.csv', header=None, skiprows=1, names=cols, encoding='utf-8', on_bad_lines='skip')
    df['Sexo'] = df['Sexo'].astype(str).str.strip().str.upper()
    df = df[df['Sexo'] == 'TOTAL'].copy()

    pct_cols = [c for c in df.columns if c.startswith('Pct_')]
    abs_cols = [c for c in df.columns if c.startswith('Pob_') and c.endswith('_k')]

    numeric_to_fix = pct_cols + abs_cols + ['Pob_Total_Millones', 'Tasa_Urbanización', 'Esperanza_Vida', 'Densidad_Poblacional', 'Año', 'TFT']
    for col in numeric_to_fix: df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['País', 'Año'])
    df['Año'] = df['Año'].astype(int)

    # Inconsistencies fix
    df['sum_pct'] = df[pct_cols].sum(axis=1)
    for col in pct_cols: df[col] = (df[col] / df['sum_pct']) * 100
    for col in pct_cols:
        abs_col = col.replace('Pct_', 'Pob_').replace('mas', 'mas_k')
        if '70_mas' in col: abs_col = 'Pob_70_mas_k'
        df[abs_col] = (df[col] / 100) * df['Pob_Total_Millones'] * 1000

    df['ISO3'] = df['País'].map(ISO3_MAP)
    df['Región'] = df['País'].map(REGION_MAP)

    pob_0_14 = df['Pob_0_4_k'] + df['Pob_5_9_k'] + df['Pob_10_14_k']
    pob_15_64 = df[abs_cols].sum(axis=1) - pob_0_14 - df['Pob_65_69_k'] - df['Pob_70_mas_k']
    pob_65_plus = df['Pob_65_69_k'] + df['Pob_70_mas_k']

    df['Tasa_Dependencia_Infantil'] = (pob_0_14 / pob_15_64) * 100
    df['Tasa_Dependencia_Vejez'] = (pob_65_plus / pob_15_64) * 100
    df['Tasa_Dependencia_Total'] = ((pob_0_14 + pob_65_plus) / pob_15_64) * 100
    df['Edad_Mediana_Estimada'] = df.apply(estimate_median_age, axis=1)

    # Enrichment: Growth rates
    df = df.sort_values(['País', 'Año'])
    df['Crecimiento_Anual_Pob'] = df.groupby('País')['Pob_Total_Millones'].pct_change() * 100

    # Enrichment: Demographic Bonus Indicator (15-64 share)
    df['Pct_Pob_Edad_Trabajar'] = (pob_15_64 / (df['Pob_Total_Millones'] * 1000)) * 100

    countries = df['País'].unique()
    all_years_df = []
    for country in countries:
        c_df = df[df['País'] == country].drop_duplicates('Año').set_index('Año').reindex(range(2000, 2024))
        num_cols = c_df.select_dtypes(include=[np.number]).columns
        c_df[num_cols] = c_df[num_cols].interpolate(method='linear', limit_direction='both').ffill().bfill()
        c_df['País'] = country
        c_df['ISO3'] = ISO3_MAP.get(country)
        c_df['Región'] = REGION_MAP.get(country)
        all_years_df.append(c_df.reset_index())

    final_df = pd.concat(all_years_df).round(2)
    final_df.to_csv('data/population_evolution_latin_america_by_age_2000_2023.csv', index=False)

    # API Generation
    os.makedirs('docs/api', exist_ok=True)
    for country in countries:
        slug = country.lower().replace(' ', '_').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á', 'a').replace('ú', 'u').replace('ñ', 'n')
        country_data = final_df[final_df['País'] == country].to_dict('records')
        with open(f'docs/api/{slug}.json', 'w', encoding='utf-8') as f:
            json.dump(country_data, f, indent=2, ensure_ascii=False)

    print("Data enrichment and API generation complete.")

if __name__ == "__main__": main()
