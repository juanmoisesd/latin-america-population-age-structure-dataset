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

Harmonized demographic dataset describing the **population age structure** for **19 Latin American countries** over the period **1995–2030**.

The dataset contains **228 country-year records** and **41 variables**: absolute population counts by three standard age groups (0–14, 15–64, 65+), percentage distributions, dependency ratio, aging index, and estimated median age.

**Source:** CEPALSTAT/ECLAC | **License:** CC0 1.0 | **DOI:** [10.17632/ygkmshr5fv.1](https://doi.org/10.17632/ygkmshr5fv.1) | **Version:** 1.1.0

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
| 8 | Ecuador | 18 | Haiti |
| 9 | El Salvador | 19 | Venezuela |
| 10 | Guatemala | | |

---

## Dataset Structure

### Main File

| File | Description |
|------|-------------|
| `data/latin_america_population_age_structure.csv` | Main dataset — 228 rows × 41 columns |

### Key Variables

| Variable | Description |
|----------|-------------|
| `country` | Country name (English) |
| `year` | Reference year (1995–2030) |
| `pop_total` | Total population |
| `pop_0_14` | Population aged 0–14 |
| `pop_15_64` | Population aged 15–64 |
| `pop_65_mas` | Population aged 65+ |
| `pct_0_14` | % aged 0–14 |
| `pct_15_64` | % aged 15–64 |
| `pct_65_mas` | % aged 65+ |
| `dependency_ratio` | (pop 0-14 + pop 65+) / pop 15-64 |
| `aging_index` | pop_65+ / pop_0-14 × 100 |
| `median_age` | Estimated median age |

Full variable list: [DATA_DICTIONARY.md](DATA_DICTIONARY.md)

---

## Quick Start

### Python

```python
import pandas as pd

url = "https://raw.githubusercontent.com/juanmoisesd/latin-america-population-age-structure-dataset/main/data/latin_america_population_age_structure.csv"
df = pd.read_csv(url)

print(df.shape)        # (228, 41)
print(df['country'].unique())  # 19 countries
print(df.groupby('country')['pct_65_mas'].last().sort_values(ascending=False))
```

### R

```r
url <- "https://raw.githubusercontent.com/juanmoisesd/latin-america-population-age-structure-dataset/main/data/latin_america_population_age_structure.csv"
df <- read.csv(url)

dim(df)               # 228 × 41
unique(df$country)    # 19 countries
library(dplyr)
df %>% group_by(country) %>% summarise(latest_pct_65 = last(pct_65_mas)) %>% arrange(desc(latest_pct_65))
```

---

## Dataset Status

| Property | Value |
|----------|-------|
| Version | 1.1.0 |
| Records | 228 country-year pairs |
| Variables | 41 |
| Countries | 19 |
| Period | 1995–2030 |
| Source | CEPALSTAT/ECLAC |
| License | CC0 1.0 (Public Domain) |
| DOI | 10.17632/ygkmshr5fv.1 |

---

## How to Cite

### APA (Recommended)

> de la Serna Tuya, J. M. (2026). *Latin America Population Age Structure Dataset* (Version 1.1.0) [Data set]. Mendeley Data. https://doi.org/10.17632/ygkmshr5fv.1

### BibTeX

```bibtex
@dataset{delaserna2026,
  author    = {de la Serna Tuya, Juan Moisés},
  title     = {Latin America Population Age Structure Dataset},
  year      = {2026},
  version   = {1.1.0},
  publisher = {Mendeley Data},
  doi       = {10.17632/ygkmshr5fv.1},
  url       = {https://doi.org/10.17632/ygkmshr5fv.1}
}
```

See [CITATION_GUIDE.md](CITATION_GUIDE.md) for more formats.

---

## Documentation

| File | Description |
|------|-------------|
| [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Variable definitions, types, units |
| [METHODOLOGY.md](METHODOLOGY.md) | Data collection and harmonization |
| [DATA_PAPER.md](DATA_PAPER.md) | Full scientific data paper (8 sections) |
| [KNOWN_ISSUES.md](KNOWN_ISSUES.md) | Known limitations and caveats |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CITATION_GUIDE.md](CITATION_GUIDE.md) | Citation formats |

---

## Known Limitations

- Values for **2025 and 2030** are projections, not observed data
- Venezuela data (2016–2022) is estimated
- Cross-country comparisons should account for differing census intervals
- See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for full details

---

## License

Released under **[CC0 1.0 Universal (Public Domain)](https://creativecommons.org/publicdomain/zero/1.0/)** — free to copy, modify, distribute and use, even commercially, without asking permission.

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
| LinkedIn | [juanmoisesdelaserna](https://www.linkedin.com/in/juanmoisesdelaserna) |
