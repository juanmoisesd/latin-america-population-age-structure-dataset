# Latin America Population Age Structure Dataset

> Part of the [Open Research Collection](https://doi.org/10.5281/zenodo.19145316) by Juan Moisés de la Serna Tuya — 1,273+ datasets

[![Dataset DOI](https://img.shields.io/badge/Dataset_DOI-10.17632%2Fygkmshr5fv.1-blue?logo=mendeley)](https://doi.org/10.17632/ygkmshr5fv.1)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-GitHub_Pages-orange?logo=github)](https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/)

[Versión en Español (README_ES.md)](README_ES.md)

---

## Overview

Harmonized demographic dataset describing the **population age structure** for **19 Latin American countries** over the period **2000–2030**. This version includes refined indicators, corrected inconsistencies, and projections to 2030.

## Key Features

- **Refined Data**: Corrected mathematical inconsistencies in age groups.
- **Projections**: Linear regression-based projections up to 2030 for all 19 countries.
- **Advanced Indicators**:
  - ISO-3166-1 alpha-3 codes.
  - Dependency Ratios (Child, Old-age, Total).
  - Estimated Median Age.
  - Urbanization Rate, Life Expectancy, and Population Density.
- **Visualizations**: Interactive population pyramids and trend charts.
- **Reproducible Pipeline**: Full processing script (`main.py`) and CLI for queries.

---

## Dataset Structure

### Main Files

| File | Description |
|------|-------------|
| `data/population_evolution_latin_america_by_age_2000_2023.csv` | Historical data with refined indicators |
| `data/population_evolution_latin_america_by_age_2000_2030_forecast.csv` | Historical + Forecast data to 2030 |

### Key Variables

| Variable | Description |
|----------|-------------|
| `País` | Country name |
| `Año` | Reference year |
| `ISO3` | ISO-3166-1 alpha-3 code |
| `Pob_Total_Millones` | Total population (millions) |
| `Tasa_Dependencia_Total` | (pop 0-14 + pop 65+) / pop 15-64 * 100 |
| `Edad_Mediana_Estimada` | Estimated median age |

Full details in [CODEBOOK.md](CODEBOOK.md)

---

## Quick Start

### CLI Query

```bash
python3 cli.py --country Mexico --indicator Esperanza_Vida
```

### Reproduce Everything

```bash
make all
```

---

## Documentation

| File | Description |
|------|-------------|
| [CODEBOOK.md](CODEBOOK.md) | Detailed variable definitions |
| [ADVANCED_INSIGHTS.md](ADVANCED_INSIGHTS.md) | Demographic transition and bonus insights |
| [METHODOLOGY.md](METHODOLOGY.md) | Collection and harmonization methodology |

---

## Author

**Juan Moisés de la Serna Tuya**  
ORCID: [0000-0002-8401-8018](https://orcid.org/0000-0002-8401-8018)
