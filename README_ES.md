# Repositorio de Estructura de Edad de la Población de América Latina

> Parte de la [Colección de Investigación Abierta](https://doi.org/10.5281/zenodo.19145316) por Juan Moisés de la Serna Tuya — Más de 1,273 conjuntos de datos

[![DOI del Dataset](https://img.shields.io/badge/Dataset_DOI-10.17632%2Fygkmshr5fv.1-blue?logo=mendeley)](https://doi.org/10.17632/ygkmshr5fv.1)
[![Licencia: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Dashboard en Vivo](https://img.shields.io/badge/Live_Dashboard-GitHub_Pages-orange?logo=github)](https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/)

[English Version (README.md)](README.md)

---

## Descripción General

Conjunto de datos demográficos armonizados que describen la **estructura por edad de la población** para **19 países latinoamericanos** durante el periodo **2000–2030**. Esta versión incluye indicadores refinados, corrección de inconsistencias y proyecciones hasta 2030.

## Características Principales

- **Datos Refinados**: Corrección de inconsistencias matemáticas en grupos de edad.
- **Proyecciones**: Proyecciones basadas en regresión lineal hasta 2030 para los 19 países.
- **Indicadores Avanzados**:
  - Códigos ISO-3166-1 alpha-3.
  - Tasas de Dependencia (Infantil, Vejez, Total).
  - Edad Mediana Estimada.
  - Tasa de Urbanización, Esperanza de Vida y Densidad Poblacional.
- **Visualizaciones**: Pirámides poblacionales interactivas y gráficas de tendencias.
- **Pipeline Reproducible**: Script de procesamiento completo (`main.py`) y CLI para consultas.

---

## Estructura del Conjunto de Datos

### Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `data/population_evolution_latin_america_by_age_2000_2023.csv` | Datos históricos con indicadores refinados |
| `data/population_evolution_latin_america_by_age_2000_2030_forecast.csv` | Datos históricos + Proyecciones a 2030 |

### Variables Clave

| Variable | Descripción |
|----------|-------------|
| `País` | Nombre del país |
| `Año` | Año de referencia |
| `ISO3` | Código ISO-3166-1 alpha-3 |
| `Pob_Total_Millones` | Población total (millones) |
| `Tasa_Dependencia_Total` | (pob 0-14 + pob 65+) / pob 15-64 * 100 |
| `Edad_Mediana_Estimada` | Edad mediana estimada |

Más detalles en [CODEBOOK.md](CODEBOOK.md)

---

## Inicio Rápido

### Consulta CLI

```bash
python3 cli.py --country Mexico --indicator Esperanza_Vida
```

### Reproducir Todo

```bash
make all
```

---

## Documentación

| Archivo | Descripción |
|---------|-------------|
| [CODEBOOK.md](CODEBOOK.md) | Definiciones detalladas de variables |
| [ADVANCED_INSIGHTS_ES.md](ADVANCED_INSIGHTS_ES.md) | Perspectivas sobre transición y bono demográfico |
| [METHODOLOGY.md](METHODOLOGY.md) | Metodología de recolección y armonización |

---

## Autor

**Juan Moisés de la Serna Tuya**
ORCID: [0000-0002-8401-8018](https://orcid.org/0000-0002-8401-8018)
