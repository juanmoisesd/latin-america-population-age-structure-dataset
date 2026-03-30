import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    stats_dir = 'docs/assets/stats'
    os.makedirs(stats_dir, exist_ok=True)

    # Filter for 2023 data for cross-sectional analysis
    df_2023 = df[df['Año'] == 2023].copy()

    # 1. Correlation Matrix
    cols_for_corr = ['Pob_Total_Millones', 'Tasa_Urbanización', 'Esperanza_Vida',
                     'Densidad_Poblacional', 'Tasa_Dependencia_Total', 'Edad_Mediana_Estimada']
    corr = df_2023[cols_for_corr].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Matriz de Correlación de Indicadores (2023)')
    plt.tight_layout()
    plt.savefig(f'{stats_dir}/correlation_matrix.png')
    plt.close()

    # 2. Indicator Distributions (Boxplots)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_2023[['Esperanza_Vida', 'Edad_Mediana_Estimada']])
    plt.title('Distribución Regional: Esperanza de Vida y Edad Mediana (2023)')
    plt.savefig(f'{stats_dir}/distributions_box.png')
    plt.close()

    # 3. Growth rate analysis
    df_growth = df[df['Año'] <= 2023].copy()
    df_growth['Crecimiento'] = df_growth.groupby('País')['Pob_Total_Millones'].pct_change() * 100

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_growth, x='Año', y='Crecimiento', hue='País', legend=False, alpha=0.5)
    plt.title('Variación Anual de la Población (2000-2023)')
    plt.ylabel('% Cambio Anual')
    plt.savefig(f'{stats_dir}/growth_trends.png')
    plt.close()

    print(f"Statistical analysis generated in {stats_dir}/")

if __name__ == "__main__":
    main()
