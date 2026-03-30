import pandas as pd
import numpy as np

ISO3_MAP = {
    "Argentina": "ARG",
    "Bolivia": "BOL",
    "Brasil": "BRA",
    "Chile": "CHL",
    "Colombia": "COL",
    "Costa Rica": "CRI",
    "Cuba": "CUB",
    "Ecuador": "ECU",
    "El Salvador": "SLV",
    "Guatemala": "GTM",
    "Honduras": "HND",
    "México": "MEX",
    "Nicaragua": "NIC",
    "Panamá": "PAN",
    "Paraguay": "PRY",
    "Perú": "PER",
    "República Dominicana": "DOM",
    "Uruguay": "URY",
    "Venezuela": "VEN",
}

def estimate_median_age(row):
    pct_cols = [
        "Pct_0_4", "Pct_5_9", "Pct_10_14", "Pct_15_19", "Pct_20_24",
        "Pct_25_29", "Pct_30_34", "Pct_35_39", "Pct_40_44", "Pct_45_49",
        "Pct_50_54", "Pct_55_59", "Pct_60_64", "Pct_65_69", "Pct_70_mas"
    ]
    age_bins = [0, 5, 10, 15, 20, 25, 30, 35, high_age_limit := 40, 45, 50, 55, 60, 65, 70, 90]

    cumulative_pct = 0
    for i, col in enumerate(pct_cols):
        val = row[col]
        if pd.isna(val) or val <= 0:
            continue
        if cumulative_pct + val >= 50:
            low_age = age_bins[i]
            high_age = age_bins[i+1]
            needed = 50 - cumulative_pct
            median_age = low_age + (needed / val) * (high_age - low_age)
            return round(median_age, 1)
        cumulative_pct += val
    return 30.0

def main():
    df = pd.read_csv('data/dataset.csv', header=None, skiprows=1, encoding='utf-8', on_bad_lines='skip')

    mapping = {
        0: 'País', 1: 'Año', 2: 'Sexo', 3: 'Pob_Total_Millones', 4: 'Tasa_Urbanización',
        5: 'TFT', 6: 'Esperanza_Vida', 7: 'Mort_Inf_1k', 8: 'Migr_Neta_k', 9: 'Densidad_Poblacional', 10: 'Ind_Dependencia',
        11: 'Pct_0_4', 12: 'Pct_5_9', 13: 'Pct_10_14', 14: 'Pct_15_19', 15: 'Pct_20_24',
        16: 'Pct_25_29', 17: 'Pct_30_34', 18: 'Pct_35_39', 19: 'Pct_40_44', 20: 'Pct_45_49',
        21: 'Pct_50_54', 22: 'Pct_55_59', 23: 'Pct_60_64', 24: 'Pct_65_69', 25: 'Pct_70_mas',
        27: 'Pob_0_4_k', 28: 'Pob_5_9_k', 29: 'Pob_10_14_k', 30: 'Pob_15_19_k', 31: 'Pob_20_24_k',
        32: 'Pob_25_29_k', 33: 'Pob_30_34_k', 34: 'Pob_35_39_k', 35: 'Pob_40_44_k', 36: 'Pob_45_49_k',
        37: 'Pob_50_54_k', 38: 'Pob_55_59_k', 39: 'Pob_60_64_k', 40: 'Pob_65_69_k', 41: 'Pob_70_mas_k'
    }

    df = df.rename(columns=mapping)
    df = df[[v for k,v in mapping.items() if v in df.columns]]

    df['Sexo'] = df['Sexo'].astype(str).str.strip().str.upper()
    df = df[df['Sexo'] == 'TOTAL'].copy()

    pct_cols = [
        "Pct_0_4", "Pct_5_9", "Pct_10_14", "Pct_15_19", "Pct_20_24",
        "Pct_25_29", "Pct_30_34", "Pct_35_39", "Pct_40_44", "Pct_45_49",
        "Pct_50_54", "Pct_55_59", "Pct_60_64", "Pct_65_69", "Pct_70_mas"
    ]

    abs_cols = [
        'Pob_0_4_k', 'Pob_5_9_k', 'Pob_10_14_k', 'Pob_15_19_k', 'Pob_20_24_k',
        'Pob_25_29_k', 'Pob_30_34_k', 'Pob_35_39_k', 'Pob_40_44_k', 'Pob_45_49_k',
        'Pob_50_54_k', 'Pob_55_59_k', 'Pob_60_64_k', 'Pob_65_69_k', 'Pob_70_mas_k'
    ]

    numeric_to_fix = pct_cols + abs_cols + ['Pob_Total_Millones', 'Tasa_Urbanización', 'Esperanza_Vida', 'Densidad_Poblacional', 'Año']
    for col in numeric_to_fix:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['País', 'Año'])
    df['Año'] = df['Año'].astype(int)

    df['sum_pct'] = df[pct_cols].sum(axis=1)
    for col in pct_cols:
        df[col] = (df[col] / df['sum_pct']) * 100

    for col in pct_cols:
        abs_col = col.replace('Pct_', 'Pob_').replace('mas', 'mas_k')
        if '70_mas' in col:
            abs_col = 'Pob_70_mas_k'
        df[abs_col] = (df[col] / 100) * df['Pob_Total_Millones'] * 1000

    df['ISO3'] = df['País'].map(ISO3_MAP)

    pob_0_14 = df['Pob_0_4_k'] + df['Pob_5_9_k'] + df['Pob_10_14_k']
    pob_15_64 = df['Pob_15_19_k'] + df['Pob_20_24_k'] + df['Pob_25_29_k'] + \
                df['Pob_30_34_k'] + df['Pob_35_39_k'] + df['Pob_40_44_k'] + \
                df['Pob_45_49_k'] + df['Pob_50_54_k'] + df['Pob_55_59_k'] + \
                df['Pob_60_64_k']
    pob_65_plus = df['Pob_65_69_k'] + df['Pob_70_mas_k']

    df['Tasa_Dependencia_Infantil'] = (pob_0_14 / pob_15_64) * 100
    df['Tasa_Dependencia_Vejez'] = (pob_65_plus / pob_15_64) * 100
    df['Tasa_Dependencia_Total'] = ((pob_0_14 + pob_65_plus) / pob_15_64) * 100

    df['Edad_Mediana_Estimada'] = df.apply(estimate_median_age, axis=1)

    countries = df['País'].unique()
    all_years_df = []

    for country in countries:
        country_df = df[df['País'] == country].copy()
        if country_df.empty: continue

        country_df = country_df.sort_values('Año').drop_duplicates('Año')
        country_df = country_df.set_index('Año').reindex(range(2000, 2024))

        numeric_cols = country_df.select_dtypes(include=[np.number]).columns
        country_df[numeric_cols] = country_df[numeric_cols].interpolate(method='linear', limit_direction='both')
        country_df[numeric_cols] = country_df[numeric_cols].ffill().bfill()

        country_df['País'] = country
        country_df['ISO3'] = ISO3_MAP.get(country)
        all_years_df.append(country_df.reset_index())

    if not all_years_df:
        print("Error: No data to concatenate.")
        return

    final_df = pd.concat(all_years_df)
    final_df = final_df.round(2)

    cols_to_keep = [
        'País', 'ISO3', 'Año', 'Pob_Total_Millones', 'Tasa_Urbanización',
        'Esperanza_Vida', 'Densidad_Poblacional', 'Tasa_Dependencia_Infantil',
        'Tasa_Dependencia_Vejez', 'Tasa_Dependencia_Total', 'Edad_Mediana_Estimada'
    ] + pct_cols

    cols_to_keep = [c for c in cols_to_keep if c in final_df.columns]
    final_df = final_df[cols_to_keep]

    output_path = 'data/population_evolution_latin_america_by_age_2000_2023.csv'
    final_df.to_csv(output_path, index=False)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    main()
