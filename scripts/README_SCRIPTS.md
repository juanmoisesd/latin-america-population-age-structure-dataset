# Scripts del micrositio demográfico

## Descripción

Scripts en Python para validar, procesar y transformar el archivo `data/dataset.csv` en un micrositio estático con indicadores demográficos, páginas comparativas y datos preparados para visualizaciones.

El dataset de entrada contiene, para cada país y año:

- población total en millones
- porcentaje de población por grandes grupos de edad
- población estimada por grupo de edad en miles
- fuente de procedencia de los datos

## Dataset de entrada

El archivo `data/dataset.csv` debe incluir las siguientes columnas:

- `País`
- `Año`
- `Población_Total_Millones`
- `Pct_0_14`
- `Pct_15_24`
- `Pct_25_54`
- `Pct_55_64`
- `Pct_65_más`
- `Pob_0_14_Miles`
- `Pob_15_24_Miles`
- `Pob_25_54_Miles`
- `Pob_55_64_Miles`
- `Pob_65_más_Miles`
- `Fuente`

## Estructura generada

Al ejecutar el pipeline completo se produce una estructura similar a esta:

```text
docs/
├── index.html
├── assets/
│   ├── style.css
│   └── app.js
├── pages/
│   ├── countries.html
│   ├── country-{pais}.html
│   ├── country-{pais}-year-{anio}.html
│   ├── years.html
│   ├── year-{anio}.html
│   ├── indicators.html
│   ├── indicator-{indicador}.html
│   ├── comparisons.html
│   ├── compare-{a}-vs-{b}-{indicador}.html
│   └── research-questions/
│       ├── index.html
│       ├── que-paises-*.html
│       └── como-*-en-{pais}.html
├── atlas/
│   └── data/
│       ├── atlas_data.json
│       ├── atlas_metadata.json
│       └── atlas_data_with_indicators.csv
└── data/
    ├── dataset_with_indicators.csv
    ├── indicators_summary_by_country.csv
    ├── indicators_summary_by_year.csv
    └── latest_snapshot.csv
