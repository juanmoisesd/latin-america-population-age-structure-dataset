# Scripts del micrositio demográfico

## Descripción

Scripts en Python para validar, procesar y transformar el archivo `data/dataset.csv` en un micrositio estático con indicadores demográficos, páginas comparativas y datos preparados para visualizaciones.

---

## Scripts disponibles

### `validate_dataset.py`
Valida estructura, tipos y coherencia aritmética del dataset de entrada.
- Detecta duplicados por País-Año
- - Verifica que los porcentajes sumen ~100
  - - Detecta valores negativos
    - - Comprueba coherencia entre población total y suma de grupos absolutos
      - - **No genera archivos de salida**
       
        - ### `build_indicators.py`
        - Genera los archivos JSON y CSV consumidos por el atlas interactivo.
        - - Lee `data/dataset.csv`, calcula indicadores derivados (via `common.add_indicators`)
          - - Escribe en `docs/atlas/data/`:
            -   - `atlas_data.json`
                -   - `atlas_metadata.json`
                    -   - `atlas_data_with_indicators.csv`
                     
                        - ### `build_atlas_data.py`
                        - Mismo propósito y salida que `build_indicators.py`. Genera los datos del atlas interactivo.
                        - - Escribe en `docs/atlas/data/`:
                          -   - `atlas_data.json`
                              -   - `atlas_metadata.json`
                                  -   - `atlas_data_with_indicators.csv`
                                   
                                      - ### `build_site.py`
                                      - Mismo propósito y salida que `build_indicators.py` y `build_atlas_data.py`. Genera los datos del atlas interactivo.
                                      - - Escribe en `docs/atlas/data/`:
                                        -   - `atlas_data.json`
                                            -   - `atlas_metadata.json`
                                                -   - `atlas_data_with_indicators.csv`
                                                 
                                                    - ### `generate_research_pages.py`
                                                    - Genera las páginas de preguntas de investigación demográfica bajo `docs/pages/research-questions/`.
                                                    - - Lee `data/dataset_with_indicators.csv` (o `dataset.csv` como fallback)
                                                      - - Lee opcionalmente `data/indicators_summary_by_country.csv` y `data/research_question_catalog.csv`
                                                        - - Escribe en `docs/pages/research-questions/`:
                                                          -   - `index.html`
                                                              -   - Una página por país: `como-cambio-la-estructura-por-edades-en-{pais}-entre-{anio_ini}-y-{anio_fin}.html`
                                                                  - - Usa `page_shell()` con `nav_html()` y `footer_html()` correctamente interpoladas
                                                                   
                                                                    - ### `common.py`
                                                                    - Módulo compartido con utilidades usadas por todos los demás scripts.
                                                                    - - Constantes: columnas requeridas, mapas ISO3 y región
                                                                      - - Funciones: `slugify`, `read_dataset`, `add_indicators`, `summarize_by_country`, `summarize_by_year`, `latest_by_country`, `nav_links`, `save_json`, `ensure_dir`, `parse_args`
                                                                       
                                                                        - ### `run_all.py`
                                                                        - Ejecuta el pipeline completo en orden:
                                                                        - 1. `validate_dataset.py`
                                                                          2. 2. `build_indicators.py`
                                                                             3. 3. `build_atlas_data.py`
                                                                                4. 4. `build_site.py`
                                                                                   5. 5. `generate_research_pages.py`
                                                                                     
                                                                                      6. ---
                                                                                     
                                                                                      7. ## ⚠️ Páginas sin generador activo
                                                                                     
                                                                                      8. Las siguientes páginas existen en `docs/pages/` como archivos estáticos pero **ningún script activo las regenera**:
                                                                                     
                                                                                      9. - `countries.html`, `country-{pais}.html`, `country-{pais}-year-{anio}.html`
                                                                                         - - `years.html`, `year-{anio}.html`
                                                                                           - - `indicators.html`, `indicator-{indicador}.html`
                                                                                             - - `comparisons.html`, `compare-{a}-vs-{b}-{indicador}.html`
                                                                                              
                                                                                               - Estas páginas tienen un bug: contienen literales `{nav(css_prefix)}`, `{footer()}` y `{html.escape(title)}` sin interpolar, por lo que se muestran sin cabecera ni pie de página.
                                                                                              
                                                                                               - ---

                                                                                               ## Dataset de entrada

                                                                                               El archivo `data/dataset.csv` debe incluir las siguientes columnas:

                                                                                               - `País`
                                                                                               - - `Año`
                                                                                                 - - `Población_Total_Millones`
                                                                                                   - - `Pct_0_14`, `Pct_15_24`, `Pct_25_54`, `Pct_55_64`, `Pct_65_más`
                                                                                                     - - `Pob_0_14_Miles`, `Pob_15_24_Miles`, `Pob_25_54_Miles`, `Pob_55_64_Miles`, `Pob_65_más_Miles`
                                                                                                       - - `Fuente`
                                                                                                        
                                                                                                         - ---
                                                                                                         
                                                                                                         ## Estructura generada
                                                                                                         
                                                                                                         ```text
                                                                                                         docs/
                                                                                                         ├── index.html
                                                                                                         ├── assets/
                                                                                                         │   ├── style.css
                                                                                                         │   └── app.js
                                                                                                         ├── pages/
                                                                                                         │   ├── countries.html                         ← sin generador activo
                                                                                                         │   ├── country-{pais}.html                    ← sin generador activo
                                                                                                         │   ├── country-{pais}-year-{anio}.html        ← sin generador activo
                                                                                                         │   ├── years.html                             ← sin generador activo
                                                                                                         │   ├── year-{anio}.html                       ← sin generador activo
                                                                                                         │   ├── indicators.html                        ← sin generador activo
                                                                                                         │   ├── indicator-{indicador}.html             ← sin generador activo
                                                                                                         │   ├── comparisons.html                       ← sin generador activo
                                                                                                         │   ├── compare-{a}-vs-{b}-{indicador}.html   ← sin generador activo
                                                                                                         │   └── research-questions/                    ← generado por generate_research_pages.py
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
                                                                                                         ```
