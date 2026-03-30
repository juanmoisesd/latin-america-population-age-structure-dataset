import json
import pandas as pd

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')

    fields = []
    for col in df.columns:
        if col in ['País', 'ISO3']:
            col_type = 'string'
        elif col == 'Año':
            col_type = 'integer'
        else:
            col_type = 'number'
        fields.append({"name": col, "type": col_type})

    datapackage = {
        "name": "latin-america-population-demographics-refined",
        "title": "Latin America Population Demographics (2000-2030) - Refined and Forecasted",
        "description": "Refined demographic data for Latin America with corrected age group inconsistencies and projections to 2030. Includes dependency ratios, life expectancy, and median age.",
        "version": "2.0.0",
        "profile": "tabular-data-package",
        "licenses": [
            {
                "name": "CC0-1.0",
                "title": "CC0 1.0 Universal",
                "path": "https://creativecommons.org/publicdomain/zero/1.0/"
            }
        ],
        "resources": [
            {
                "name": "population-evolution-historical",
                "path": "data/population_evolution_latin_america_by_age_2000_2023.csv",
                "format": "csv",
                "mediatype": "text/csv",
                "schema": {"fields": fields}
            },
            {
                "name": "population-evolution-forecast",
                "path": "data/population_evolution_latin_america_by_age_2000_2030_forecast.csv",
                "format": "csv",
                "mediatype": "text/csv",
                "schema": {"fields": fields}
            }
        ],
        "keywords": ["latin-america", "population", "aging", "demographics", "forecast", "projections"]
    }

    with open('datapackage.json', 'w', encoding='utf-8') as f:
        json.dump(datapackage, f, indent=2, ensure_ascii=False)

    print("Updated datapackage.json to Frictionless Data v2 schema with full column definitions.")

if __name__ == "__main__":
    main()
