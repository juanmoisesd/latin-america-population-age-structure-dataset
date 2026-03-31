import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def slugify(text):
    return text.lower().replace(' ', '_').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á', 'a').replace('ú', 'u').replace('ñ', 'n')

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    assets_dir = 'docs/assets'
    os.makedirs(assets_dir, exist_ok=True)

    # Existing charts...
    major_countries = ['Brasil', 'México', 'Argentina', 'Colombia', 'Chile']

    # Life Expectancy
    plt.figure(figsize=(10, 6))
    for country in major_countries:
        c_df = df[df['País'] == country]
        plt.plot(c_df['Año'], c_df['Esperanza_Vida'], label=country, marker='o', markersize=3)
    plt.title('Esperanza de Vida (2000-2030)')
    plt.legend(); plt.grid(True); plt.savefig(f'{assets_dir}/life_expectancy_trend.png'); plt.close()

    # Demographic Bonus
    plt.figure(figsize=(10, 6))
    for country in major_countries:
        c_df = df[df['País'] == country]
        share = c_df['Pct_15_19'] + c_df['Pct_20_24'] + c_df['Pct_25_29'] + \
                c_df['Pct_30_34'] + c_df['Pct_35_39'] + c_df['Pct_40_44'] + \
                c_df['Pct_45_49'] + c_df['Pct_50_54'] + c_df['Pct_55_59'] + \
                c_df['Pct_60_64']
        plt.plot(c_df['Año'], share, label=country)
    plt.title('Bono Demográfico (15-64 %)'); plt.legend(); plt.grid(True); plt.savefig(f'{assets_dir}/demographic_bonus_trend.png'); plt.close()

    # New: Stacked Area Charts for Age Groups evolution for ALL countries
    for country in df['País'].unique():
        slug = slugify(country)
        c_df = df[df['País'] == country].sort_values('Año')

        # Calculate groups
        p0_14 = c_df['Pct_0_4'] + c_df['Pct_5_9'] + c_df['Pct_10_14']
        p65_plus = c_df['Pct_65_69'] + c_df['Pct_70_mas']
        p15_64 = 100 - p0_14 - p65_plus

        plt.figure(figsize=(10, 6))
        plt.stackplot(c_df['Año'], p0_14, p15_64, p65_plus, labels=['0-14', '15-64', '65+'], colors=['#3498db', '#2ecc71', '#e74c3c'], alpha=0.8)
        plt.title(f'Evolución Grupos de Edad - {country}')
        plt.xlabel('Año'); plt.ylabel('Porcentaje (%)'); plt.legend(loc='upper left'); plt.grid(True, axis='y', alpha=0.3)
        plt.savefig(f'{assets_dir}/evolution_groups_{slug}.png')
        plt.close()

        # Existing Dependency
        plt.figure(figsize=(8, 5))
        plt.plot(c_df['Año'], c_df['Tasa_Dependencia_Total'], label='Total')
        plt.plot(c_df['Año'], c_df['Tasa_Dependencia_Infantil'], label='Infantil', linestyle='--')
        plt.plot(c_df['Año'], c_df['Tasa_Dependencia_Vejez'], label='Vejez', linestyle='--')
        plt.title(f'Dependencia - {country}'); plt.legend(); plt.grid(True); plt.savefig(f'{assets_dir}/dependency_{slug}.png'); plt.close()

        # Pyramid 2023
        r = c_df[c_df['Año'] == 2023].iloc[0]
        age_groups = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70+"]
        pct_cols = ["Pct_0_4", "Pct_5_9", "Pct_10_14", "Pct_15_19", "Pct_20_24", "Pct_25_29", "Pct_30_34", "Pct_35_39", "Pct_40_44", "Pct_45_49", "Pct_50_54", "Pct_55_59", "Pct_60_64", "Pct_65_69", "Pct_70_mas"]
        plt.figure(figsize=(6, 8)); plt.barh(age_groups, [r[col] for col in pct_cols], color='teal'); plt.title(f'{country} (2023)'); plt.tight_layout(); plt.savefig(f'{assets_dir}/pyramid_{slug}_2023.png'); plt.close()

    print("Expanded visualization portfolio complete.")

if __name__ == "__main__": main()
