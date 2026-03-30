import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def slugify(text):
    return text.lower().replace(' ', '_').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á', 'a').replace('ú', 'u').replace('ñ', 'n')

def generate_pyramid(df, country, year, output_path):
    subset = df[(df['País'] == country) & (df['Año'] == year)]
    if subset.empty:
        return False
    c_df = subset.iloc[0]

    age_groups = [
        "0-4", "5-9", "10-14", "15-19", "20-24",
        "25-29", "30-34", "35-39", "40-44", "45-49",
        "50-54", "55-59", "60-64", "65-69", "70+"
    ]
    pct_cols = [
        "Pct_0_4", "Pct_5_9", "Pct_10_14", "Pct_15_19", "Pct_20_24",
        "Pct_25_29", "Pct_30_34", "Pct_35_39", "Pct_40_44", "Pct_45_49",
        "Pct_50_54", "Pct_55_59", "Pct_60_64", "Pct_65_69", "Pct_70_mas"
    ]

    values = [c_df[col] for col in pct_cols]

    plt.figure(figsize=(10, 8))
    sns.barplot(x=values, y=age_groups, hue=age_groups, palette='Blues_d', legend=False)
    plt.title(f'Estructura de Edad - {country} ({year})')
    plt.xlabel('Porcentaje (%)')
    plt.ylabel('Grupo de Edad')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return True

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    assets_dir = 'docs/assets'
    os.makedirs(assets_dir, exist_ok=True)

    # 1. Dependency Trend
    countries = sorted(df['País'].unique())
    major_countries = ['Brasil', 'México', 'Argentina', 'Colombia', 'Chile']
    plt.figure(figsize=(10, 6))
    for country in major_countries:
        c_df = df[df['País'] == country]
        plt.plot(c_df['Año'], c_df['Tasa_Dependencia_Total'], label=country)
    plt.title('Tasa de Dependencia Total (2000-2030)')
    plt.xlabel('Año')
    plt.ylabel('Tasa de Dependencia (%)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{assets_dir}/dependency_trend.png')
    plt.close()

    # 2. Aging Bar Chart
    df_2023 = df[df['Año'] == 2023].copy()
    df_2023['Pct_65_mas_total'] = df_2023['Pct_65_69'] + df_2023['Pct_70_mas']
    df_2023 = df_2023.sort_values('Pct_65_mas_total', ascending=False)

    plt.figure(figsize=(12, 8))
    sns.barplot(data=df_2023, x='Pct_65_mas_total', y='País', hue='País', palette='viridis', legend=False)
    plt.title('Porcentaje de Población 65+ por País (2023)')
    plt.xlabel('% de la Población Total')
    plt.ylabel('País')
    plt.savefig(f'{assets_dir}/aging_regional_bar.png')
    plt.close()

    # 3. Population Pyramids for ALL countries (2000 vs 2023)
    for country in countries:
        slug = slugify(country)
        generate_pyramid(df, country, 2000, f'{assets_dir}/pyramid_{slug}_2000.png')
        generate_pyramid(df, country, 2023, f'{assets_dir}/pyramid_{slug}_2023.png')

    # 4. Dependency Trend for EACH country
    for country in countries:
        slug = slugify(country)
        c_df = df[df['País'] == country]
        plt.figure(figsize=(8, 5))
        plt.plot(c_df['Año'], c_df['Tasa_Dependencia_Total'], label='Total')
        plt.plot(c_df['Año'], c_df['Tasa_Dependencia_Infantil'], label='Infantil', linestyle='--')
        plt.plot(c_df['Año'], c_df['Tasa_Dependencia_Vejez'], label='Vejez', linestyle='--')
        plt.title(f'Tendencia de Dependencia - {country} (2000-2030)')
        plt.xlabel('Año')
        plt.ylabel('Tasa (%)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{assets_dir}/dependency_{slug}.png')
        plt.close()

    print(f"Visualizations generated in {assets_dir}/")

if __name__ == "__main__":
    main()
