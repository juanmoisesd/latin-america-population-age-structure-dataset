import pandas as pd
import sys

def main():
    try:
        df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    print("Running Data Quality Checks...")

    # Check 1: Percentages sum to 100
    pct_cols = [c for c in df.columns if c.startswith('Pct_') and 'Trabajar' not in c]
    sums = df[pct_cols].sum(axis=1)
    if not ((sums > 99.8) & (sums < 100.2)).all():
        print("Warning: Some age groups do not sum to 100%. Check data consistency.")
    else:
        print("OK: Age group percentages are consistent.")

    # Check 2: No negative values for key metrics
    metrics = ['Pob_Total_Millones', 'Esperanza_Vida', 'Tasa_Urbanización', 'Edad_Mediana_Estimada']
    if (df[metrics] < 0).any().any():
        print("Error: Negative values found in key demographic metrics.")
        sys.exit(1)
    else:
        print("OK: No negative values found in key metrics.")

    # Check 3: Year range
    if df['Año'].min() != 2000 or df['Año'].max() != 2030:
        print(f"Warning: Unexpected year range ({df['Año'].min()} to {df['Año'].max()}). Expected 2000-2030.")
    else:
        print("OK: Year range is correct (2000-2030).")

    print("Data quality checks complete.")

if __name__ == "__main__":
    main()
