import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def main():
    input_path = 'data/population_evolution_latin_america_by_age_2000_2023.csv'
    df = pd.read_csv(input_path)

    countries = df['País'].unique()

    forecast_years = range(2024, 2031)
    # Actually, the user asked to generate population_evolution_latin_america_by_age_2000_2030_forecast.csv
    # containing 2000-2030 data.
    all_rows = [df]

    numeric_cols = df.select_dtypes(include=[np.number]).columns.drop('Año')

    for country in countries:
        country_df = df[df['País'] == country].copy()

        country_forecast = pd.DataFrame({'Año': forecast_years})
        country_forecast['País'] = country
        country_forecast['ISO3'] = country_df['ISO3'].iloc[0]

        for col in numeric_cols:
            temp_df = country_df[['Año', col]].dropna()
            if temp_df.empty:
                country_forecast[col] = 0
                continue

            X = temp_df[['Año']]
            y = temp_df[col]

            model = LinearRegression()
            model.fit(X, y)

            X_pred = pd.DataFrame({'Año': list(forecast_years)})
            y_pred = model.predict(X_pred)

            if col in ['Pob_Total_Millones', 'Tasa_Urbanización', 'Esperanza_Vida', 'Densidad_Poblacional', 'Edad_Mediana_Estimada'] or col.startswith('Pct_') or col.startswith('Tasa_'):
                y_pred = np.maximum(y_pred, 0)

            country_forecast[col] = y_pred

        all_rows.append(country_forecast)

    final_forecast_df = pd.concat(all_rows).sort_values(['País', 'Año']).reset_index(drop=True)
    final_forecast_df = final_forecast_df.round(2)

    output_path = 'data/population_evolution_latin_america_by_age_2000_2030_forecast.csv'
    final_forecast_df.to_csv(output_path, index=False)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    main()
