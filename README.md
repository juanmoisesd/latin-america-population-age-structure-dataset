# Latin America Population Age Structure Dataset

> Part of the [Open Research Collection](https://doi.org/10.5281/zenodo.19145316) by Juan Moisés de la Serna Tuya — 1,273+ datasets

[![Dataset DOI](https://img.shields.io/badge/Dataset_DOI-10.17632%2Fygkmshr5fv.1-blue?logo=mendeley)](https://doi.org/10.17632/ygkmshr5fv.1)
[![Zenodo DOI](https://img.shields.io/badge/Zenodo_DOI-10.5281%2Fzenodo.18891177-blue?logo=zenodo)](https://doi.org/10.5281/zenodo.18891177)
[![Collection DOI](https://img.shields.io/badge/Collection_DOI-10.5281%2Fzenodo.19145316-blue?logo=zenodo)](https://doi.org/10.5281/zenodo.19145316)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--8401--8018-green?logo=orcid)](https://orcid.org/0000-0002-8401-8018)
[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-GitHub_Pages-orange?logo=github)](https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/)

---

## Overview

Harmonized demographic dataset describing the **population age structure and key demographic indicators** for **19 Latin American countries** over the period **1995-2030**.

The dataset provides quinquennial observations (1995, 2000, 2005, 2010, 2015, 2020, 2025, 2030) disaggregated by sex (men, women, total), distributed across **15 five-year age groups**, and enriched with core demographic indicators. It contains **456 observations** and **42 variables**.

**Live Dashboard:** https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/

---

## Countries Covered (19)

| # | Country | # | Country |
|---|---------|---|---------|
| 1 | Argentina | 11 | Honduras |
| 2 | Bolivia | 12 | Mexico |
| 3 | Brazil | 13 | Nicaragua |
| 4 | Chile | 14 | Panama |
| 5 | Colombia | 15 | Paraguay |
| 6 | Costa Rica | 16 | Peru |
| 7 | Cuba | 17 | Dominican Republic |
| 8 | Ecuador | 18 | Uruguay |
| 9 | El Salvador | 19 | Venezuela |
| 10 | Guatemala | | |

---

## Dataset Structure

### Main File

| File | Description |
|------|-------------|
| `data/dataset.csv` | Main dataset — 456 rows x 42 columns |

### Variables

**Identification variables**

| Variable | Description | Type |
|----------|-------------|------|
| `Country` | Country name | Categorical |
| `Year` | Observation year (quinquennial: 1995-2030) | Numeric |
| `Sex` | H = men, M = women, TOTAL = total population | Categorical |

**Demographic indicators**

| Variable | Description | Unit |
|----------|-------------|------|
| `Pob_Total_Millones` | Total population | Millions |
| `Pct_Urbana` | Urban population share | % |
| `TFT` | Total fertility rate | Children per woman |
| `Esp_Vida_Anos` | Life expectancy at birth | Years |
| `Mort_Inf_1k` | Infant mortality rate | Deaths per 1,000 births |
| `Migr_Neta_k` | Net migration | Thousands |
| `Dens_hab_km2` | Population density | Inhabitants/km2 |
| `Ind_Dependencia` | Total dependency ratio | Ratio |

**Age structure (% distribution):** `Pct_0_4`, `Pct_5_9`, `Pct_10_14`, `Pct_15_19`, `Pct_20_24`, `Pct_25_29`, `Pct_30_34`, `Pct_35_39`, `Pct_40_44`, `Pct_45_49`, `Pct_50_54`, `Pct_55_59`, `Pct_60_64`, `Pct_65_69`, `Pct_70_mas`

**Age structure (absolute counts, thousands):** `Pob_0_4_k`, `Pob_5_9_k` ... `Pob_70_mas_k` (same 15 groups)

---

## Quick Start

### Python

```python
import pandas as pd

df = pd.read_csv("data/dataset.csv")

# Filter: Argentina, total population, all years
argentina = df[(df["Country"] == "Argentina") & (df["Sex"] == "TOTAL")]
print(argentina[["Year", "Pob_Total_Millones", "Pct_0_4", "Pct_65_69", "Pct_70_mas"]])
```

### R

```r
library(readr)
library(dplyr)

df <- read_csv("data/dataset.csv")

# Filter: Brazil, total population
brazil <- df %>%
  filter(Country == "Brazil", Sex == "TOTAL") %>%
    select(Year, Pob_Total_Millones, TFT)

    print(brazil)
    ```

    ---

    ## Data Sources

    - **CEPAL** - Economic Commission for Latin America and the Caribbean
    - **World Bank** - Demographic databases
    - **BBVA Research** - Demographic reports
    - **National statistical institutes** - Of Latin American countries

    ---

    ## Dataset Status

    | Field | Value |
    |-------|-------|
    | Status | Published |
    | Dataset DOI | [10.17632/ygkmshr5fv.1](https://doi.org/10.17632/ygkmshr5fv.1) |
    | Zenodo DOI | [10.5281/zenodo.18891177](https://doi.org/10.5281/zenodo.18891177) |
    | Countries | 19 |
    | Period | 1995-2030 (quinquennial) |
    | Observations | 456 |
    | Variables | 42 |
    | Last update | 2026-03-20 |
    | License | CC0 1.0 - Public Domain |

    ---

    ## How to Cite

    **APA 7:**

    > De la Serna Tuya, J. M. (2026). *Latin America Population Age Structure Dataset* (v1.0.0) [Dataset]. GitHub & Zenodo. https://doi.org/10.17632/ygkmshr5fv.1

    **BibTeX:**

    ```bibtex
    @dataset{delaserna2026_latin_america_population_age,
      author    = {De la Serna Tuya, Juan Moisés},
        title     = {Latin America Population Age Structure Dataset},
          year      = {2026},
            version   = {1.0.0},
              publisher = {GitHub and Zenodo},
                doi       = {10.17632/ygkmshr5fv.1},
                  url       = {https://github.com/juanmoisesd/latin-america-population-age-structure-dataset},
                    note      = {ORCID: 0000-0002-8401-8018}
                    }
                    ```

                    ---

                    ## Documentation

                    | File | Description |
                    |------|-------------|
                    | [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Full variable descriptions and units |
                    | [METHODOLOGY.md](METHODOLOGY.md) | Data compilation and harmonization methods |
                    | [DATA_PAPER.md](DATA_PAPER.md) | Academic data paper |
                    | [DATASET_ABSTRACT.md](DATASET_ABSTRACT.md) | Scientific abstract |
                    | [CHANGELOG.md](CHANGELOG.md) | Version history |
                    | [CITATION_GUIDE.md](CITATION_GUIDE.md) | Citation formats (APA, BibTeX, RIS) |
                    | [GLOSSARY.md](GLOSSARY.md) | Demographic terminology |

                    ---

                    ## License

                    **CC0 1.0 Universal - Public Domain Dedication.**
                    This dataset is dedicated to the public domain. You can copy, modify, distribute and perform the work, even for commercial purposes, without asking permission. See the [LICENSE](LICENSE) file.

                    ---

                    ## Author

                    **Juan Moisés de la Serna Tuya**
                    Universidad Internacional de La Rioja (UNIR)

                    | Identifier | Value |
                    |------------|-------|
                    | ORCID | [0000-0002-8401-8018](https://orcid.org/0000-0002-8401-8018) |
                    | Scopus | [26632846700](https://www.scopus.com/authid/detail.uri?authorId=26632846700) |
                    | ResearcherID | [M-8296-2019](https://www.webofscience.com/wos/author/record/M-8296-2019) |
                    | ResearchGate | [Juan_De_La_Serna_Tuya](https://www.researchgate.net/profile/Juan_De_La_Serna_Tuya) |
                    | LinkedIn | [juanmoisesdelaserna](https://linkedin.com/in/juanmoisesdelaserna) |

                    290+ scientific works · 500+ DOIs · 90+ open datasets · Top 1% Academia.edu

                    See also: [ABOUT_THE_AUTHOR.md](ABOUT_THE_AUTHOR.md) · [CITATION_GUIDE.md](CITATION_GUIDE.md) · [GLOSSARY.md](GLOSSARY.md)