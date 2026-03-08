# Scripts 10/10 para el dataset demográfico

Este paquete sustituye tus scripts mínimos por un pipeline reproducible y mantenible.

## Qué incluye

- `scripts/validate_dataset.py`: valida estructura, duplicados y coherencia aritmética.
- `scripts/build_indicators.py`: calcula indicadores derivados y genera resúmenes.
- `scripts/build_atlas_data.py`: construye el JSON/CSV para el atlas.
- `scripts/generate_research_pages.py`: crea páginas automáticas de investigación con rankings.
- `scripts/build_site.py`: genera el sitio HTML estático con índice, perfiles por país y comparativas.
- `scripts/run_all.py`: ejecuta todo en el orden correcto.
- `scripts/common.py`: utilidades compartidas, mapeo ISO3 y regiones.

## Estructura esperada del repositorio

```text
repo/
├─ data/
│  └─ dataset.csv
├─ docs/
│  └─ assets/atlas.css
└─ scripts/
   ├─ common.py
   ├─ validate_dataset.py
   ├─ build_indicators.py
   ├─ build_atlas_data.py
   ├─ generate_research_pages.py
   ├─ build_site.py
   └─ run_all.py
```

## Ejecución rápida

```bash
python scripts/run_all.py
```

## Ejecución paso a paso

```bash
python scripts/validate_dataset.py
python scripts/build_indicators.py
python scripts/build_atlas_data.py
python scripts/generate_research_pages.py
python scripts/build_site.py
```

## Archivos generados

### En `data/`
- `dataset_with_indicators.csv`
- `indicators_summary_by_country.csv`
- `indicators_summary_by_year.csv`
- `latest_snapshot.csv`

### En `docs/atlas/data/`
- `atlas_data.json`
- `atlas_metadata.json`
- `atlas_data_with_indicators.csv`

### En `docs/`
- `index.html`
- `countries/*.html`
- `compare/*.html`
- `research-questions/*.html`

## Mejora real frente a tus scripts originales

- ya no hay placeholders
- ya no depende de edición manual
- separa validación, indicadores, atlas y sitio
- añade ISO3 y región
- genera resúmenes y rankings
- deja un pipeline reproducible para GitHub Pages
