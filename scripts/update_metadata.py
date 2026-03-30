import json
import pandas as pd

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')

    fields = []
    descriptions = {
        "País": "Nombre oficial del país.",
        "ISO3": "Código ISO-3166-1 alpha-3.",
        "Año": "Año de referencia o proyección.",
        "Pob_Total_Millones": "Población total estimada en millones de habitantes.",
        "Tasa_Urbanización": "Porcentaje de la población residente en zonas urbanas.",
        "Esperanza_Vida": "Esperanza de vida al nacer estimada (años).",
        "Tasa_Dependencia_Total": "Razón de dependencia total ((0-14 + 65+) / 15-64) * 100.",
        "Edad_Mediana_Estimada": "Edad mediana calculada mediante interpolación lineal de grupos quinquenales."
    }

    for col in df.columns:
        fields.append({
            "name": col,
            "type": "string" if col in ['País', 'ISO3', 'Región'] else "integer" if col == 'Año' else "number",
            "description": descriptions.get(col, f"Indicador demográfico: {col}")
        })

    datapackage = {
        "name": "latin-america-population-2030-ultimate",
        "title": "Conjunto de Datos Demográficos de América Latina (2000-2030) - Versión 3.0",
        "description": "Datos refinados, enriquecidos y proyectados hasta 2030 para 19 países latinoamericanos. Incluye bono demográfico, dependencia y estructura por edad completa.",
        "version": "3.0.0",
        "profile": "tabular-data-package",
        "licenses": [{"name": "CC0-1.0", "title": "CC0 1.0 Universal", "path": "https://creativecommons.org/publicdomain/zero/1.0/"}],
        "resources": [
            {
                "name": "population-evolution-forecast",
                "path": "data/population_evolution_latin_america_by_age_2000_2030_forecast.csv",
                "format": "csv",
                "mediatype": "text/csv",
                "schema": {"fields": fields}
            }
        ],
        "keywords": ["demografía", "latam", "envejecimiento", "proyecciones", "bono-demográfico", "opendata"]
    }

    with open('datapackage.json', 'w', encoding='utf-8') as f:
        json.dump(datapackage, f, indent=2, ensure_ascii=False)

    print("SEO and Frictionless Metadata updated (v3.0.0).")

if __name__ == "__main__": main()
