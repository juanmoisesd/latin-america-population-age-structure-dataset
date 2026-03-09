# Scripts del micrositio demográfico

## Descripción

Conjunto de scripts en Python para validar, procesar y transformar el archivo `data/dataset.csv` en un micrositio estático con indicadores demográficos, páginas analíticas y datos preparados para visualizaciones.

---

## Scripts disponibles

### `validate_dataset.py`
Valida la estructura, los tipos y la coherencia aritmética del dataset de entrada.

Funciones principales:
- Detecta duplicados por combinación País-Año
- Verifica que los porcentajes sumen aproximadamente 100
- Detecta valores negativos
- Comprueba la coherencia entre población total y grupos de edad
- No genera archivos de salida

---

### `build_indicators.py`
Calcula indicadores demográficos derivados a partir del dataset principal.

Funciones principales:
- Lee `data/dataset.csv`
- Aplica transformaciones mediante `common.add_indicators()`
- Genera tablas derivadas para análisis comparativos y series resumidas

Archivos de salida:
- `data/dataset_with_indicators.csv`
- `data/indicators_summary_by_country.csv`
- `data/indicators_summary_by_year.csv`
- `data/latest_snapshot.csv`

---

### `build_atlas_data.py`
Prepara los archivos consumidos por el atlas interactivo.

Funciones principales:
- Lee `data/dataset_with_indicators.csv` si existe, o `data/dataset.csv` como base alternativa
- Estructura los datos para visualizaciones geográficas e interactivas
- Genera metadatos descriptivos del atlas

Archivos de salida:
- `docs/atlas/data/atlas_data.json`
- `docs/atlas/data/atlas_metadata.json`
- `docs/atlas/data/atlas_data_with_indicators.csv`

---

### `build_site.py`
Genera las páginas HTML del micrositio demográfico.

Funciones principales:
- Construye la portada del sitio
- Genera índices temáticos y páginas analíticas
- Crea páginas por país, año, indicador y comparación
- Ensambla navegación, cabecera y pie de página

Salida esperada:
- `docs/index.html`
- `docs/pages/countries.html`
- `docs/pages/years.html`
- `docs/pages/indicators.html`
- `docs/pages/comparisons.html`
- páginas específicas dentro de `docs/pages/`

> Nota: si este script no genera actualmente estas páginas, el comportamiento implementado debe revisarse para alinearlo con esta documentación.

---

### `generate_research_pages.py`
Genera páginas de preguntas de investigación demográfica en `docs/pages/research-questions/`.

Funciones principales:
- Lee `data/dataset_with_indicators.csv` (o `data/dataset.csv` como alternativa)
- Lee opcionalmente `data/indicators_summary_by_country.csv`
- Lee opcionalmente `data/research_question_catalog.csv`
- Genera una página índice y páginas temáticas por país

Archivos de salida:
- `docs/pages/research-questions/index.html`
- una página por país con formato:
  - `como-cambio-la-estructura-por-edades-en-{pais}-entre-{anio_ini}-y-{anio_fin}.html`

---

### `common.py`
Módulo compartido con utilidades usadas por el resto de scripts.

Incluye:
- constantes de columnas requeridas
- mapas ISO3 y región
- funciones auxiliares de lectura, normalización y exportación

Funciones destacadas:
- `slugify()`
- `read_dataset()`
- `add_indicators()`
- `summarize_by_country()`
- `summarize_by_year()`
- `latest_by_country()`
- `nav_links()`
- `save_json()`
- `ensure_dir()`
- `parse_args()`

---

### `run_all.py`
Ejecuta el pipeline completo en orden.

Secuencia:
1. `validate_dataset.py`
2. `build_indicators.py`
3. `build_atlas_data.py`
4. `build_site.py`
5. `generate_research_pages.py`

---

## Estado actual y limitaciones

En algunas versiones del proyecto pueden existir páginas HTML estáticas en `docs/pages/` que no estén siendo regeneradas automáticamente por los scripts activos.

Ejemplos posibles:
- `countries.html`
- `country-{pais}.html`
- `country-{pais}-year-{anio}.html`
- `years.html`
- `year-{anio}.html`
- `indicators.html`
- `indicator-{indicador}.html`
- `comparisons.html`
- `compare-{a}-vs-{b}-{indicador}.html`

Si esto ocurre, conviene revisar `build_site.py` para asegurar que toda la arquitectura del sitio sea reproducible desde el pipeline.

También puede haber páginas con errores de interpolación, mostrando literales como:
- `{nav(css_prefix)}`
- `{footer()}`
- `{html.escape(title)}`

Estos casos indican fallos en la generación de plantillas HTML.

---

## Dataset de entrada

El archivo `data/dataset.csv` debe contener las columnas requeridas por `common.py`.

> Importante: los nombres exactos de las columnas deben verificarse en el dataset real y en las constantes definidas en `common.py`, ya que pueden variar entre versiones del proyecto.

Ejemplos habituales de columnas:
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

---

## Estructura de salida esperada

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
