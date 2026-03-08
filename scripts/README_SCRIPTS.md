# Scripts del micrositio demográfico

## Descripción

Scripts Python para generar el micrositio estático a partir del archivo `data/dataset.csv`.

## Estructura generada

Al ejecutar el pipeline completo se produce:

```
docs/
├── index.html                          # portada del sitio
├── assets/
│   ├── style.css
│   └── app.js
├── pages/
│   ├── countries.html                  # índice de países
│   ├── country-{país}.html             # ficha por país (11)
│   ├── country-{país}-year-{año}.html  # ficha país×año (44)
│   ├── years.html                      # índice de años
│   ├── year-{año}.html                 # ficha por año (4)
│   ├── indicators.html                 # índice de indicadores
│   ├── indicator-{ind}.html            # ficha por indicador (12)
│   ├── comparisons.html               # índice de comparaciones
│   ├── compare-{a}-vs-{b}-{ind}.html  # comparación bilateral (660)
│   └── research-questions/
│       ├── index.html                 # índice de preguntas
│       ├── que-paises-*.html          # preguntas globales (4)
│       └── como-*-en-{país}.html      # preguntas por país (33)
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
```

## Scripts

| Script | Función |
|---|---|
| `validate_dataset.py` | Valida columnas, tipos y coherencia del CSV |
| `build_indicators.py` | Calcula indicadores y genera CSVs en `data/` |
| `build_atlas_data.py` | Genera JSON para el atlas interactivo en `docs/atlas/data/` |
| `build_site.py` | Genera las páginas HTML en `docs/pages/` |
| `generate_research_pages.py` | Genera las preguntas de investigación en `docs/pages/research-questions/` |
| `run_all.py` | Ejecuta el pipeline completo en orden |
| `common.py` | Funciones compartidas (lectura, slugify, indicadores, etc.) |

## Ejecución

### Pipeline completo

```bash
python scripts/run_all.py
```

### Scripts individuales

```bash
python scripts/validate_dataset.py
python scripts/build_indicators.py
python scripts/build_atlas_data.py
python scripts/build_site.py
python scripts/generate_research_pages.py
```

## Requisitos

```
pip install -r requirements.txt
```

## Notas de diseño

- Todos los scripts leen `data/dataset.csv` por defecto (configurable con `--input`).
- El directorio de salida por defecto es `docs/` (configurable con `--docs-dir`).
- Las páginas generadas usan `assets/style.css` y `assets/app.js` del sitio real.
- La navegación de todas las páginas es consistente con la estructura `docs/pages/`.
- Las comparaciones bilaterales cubren los 11 países × 12 indicadores = 660 páginas.
