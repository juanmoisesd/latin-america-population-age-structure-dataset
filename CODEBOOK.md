# CODEBOOK - Latin America Population Dataset

## Variable Definitions

| Variable | Type | Description |
|----------|------|-------------|
| `País` | String | Country Name |
| `ISO3` | String | ISO-3166-1 alpha-3 code |
| `Año` | Integer | Reference Year (2000–2030) |
| `Pob_Total_Millones` | Float | Total population (millions) |
| `Tasa_Urbanización` | Float | Percentage of population living in urban areas (%) |
| `Esperanza_Vida` | Float | Life expectancy at birth (years) |
| `Densidad_Poblacional` | Float | Population density (inhabitants per km²) |
| `Tasa_Dependencia_Infantil` | Float | Population aged 0–14 relative to 15–64 (%) |
| `Tasa_Dependencia_Vejez` | Float | Population aged 65+ relative to 15–64 (%) |
| `Tasa_Dependencia_Total` | Float | (pop 0-14 + pop 65+) / pop 15-64 (%) |
| `Edad_Mediana_Estimada` | Float | Estimated median age of the population (years) |
| `Pct_X_Y` | Float | Percentage of population in the age group X-Y (%) |

## Age Groups

The dataset includes 5-year age groups from `Pct_0_4` up to `Pct_70_mas`.

## Projections

Data from 2024 to 2030 are estimated using **Simple Linear Regression** for each indicator based on historical trends (2000-2023).

## Data Sources

- Primary: CEPALSTAT/ECLAC
- Refined: Harmonization and indicator calculation by the repository author.
