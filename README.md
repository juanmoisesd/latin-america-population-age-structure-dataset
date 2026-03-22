# Latin America Population Age Structure Dataset

[![Dataset DOI](https://img.shields.io/badge/Dataset_DOI-10.17632%2Fygkmshr5fv.1-blue?logo=mendeley)](https://doi.org/10.17632/ygkmshr5fv.1)
[![Zenodo DOI](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.18891177-blue?logo=zenodo)](https://doi.org/10.5281/zenodo.18891177)
[![Collection DOI](https://img.shields.io/badge/Collection_DOI-10.5281%2Fzenodo.19145316-blue?logo=zenodo)](https://doi.org/10.5281/zenodo.19145316)
[![License: CC0 1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Author ORCID](https://img.shields.io/badge/ORCID-0000--0002--8401--8018-green?logo=orcid)](https://orcid.org/0000-0002-8401-8018)
[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-GitHub_Pages-blue?logo=github)](https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/)

> Part of the **Open Research Collection** by Juan Moisés de la Serna Tuya — 1,273+ datasets | [DOI: 10.5281/zenodo.19145316](https://doi.org/10.5281/zenodo.19145316)

---

## Overview

Harmonized demographic dataset covering **population age structure** for **19 Latin American countries** across **4 time points (2000, 2005, 2010, 2015)**. Each observation is structured as **Country × Year × Sex** and includes 15 quinquennial age groups plus key demographic indicators.

| Field | Value |
|---|---|
| **Countries** | 19 (see list below) |
| **Period** | 2000–2015 (quinquennial: 2000, 2005, 2010, 2015) |
| **Unit of observation** | Country × Year × Sex |
| **Total records** | 228 (19 × 4 × 3) |
| **Variables** | 41 |
| **Format** | CSV (UTF-8) |
| **License** | CC0 1.0 Universal — Public Domain |
| **Dataset DOI** | [10.17632/ygkmshr5fv.1](https://doi.org/10.17632/ygkmshr5fv.1) |
| **Last update** | 2026-03-20 |

🌐 **[Open Interactive Dashboard](https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/)**

---

## Countries Included (19)

Argentina · Bolivia · Brasil · Chile · Colombia · Costa Rica · Cuba · Ecuador · El Salvador · Guatemala · Honduras · México · Nicaragua · Panamá · Paraguay · Perú · República Dominicana · Uruguay · Venezuela

---

## Repository Structure

```
latin-america-population-age-structure-dataset/
├── data/
│   ├── dataset.csv                       # Main dataset (228 records × 41 variables)
│   ├── dataset_with_indicators.csv       # Dataset + computed demographic indicators
│   ├── indicators_summary_by_country.csv # Indicators aggregated by country
│   └── indicators_summary_by_year.csv    # Indicators aggregated by year
├── docs/                                 # GitHub Pages static microsite
├── scripts/
│   ├── validate_dataset.py               # Structural and arithmetic validation
│   ├── build_indicators.py               # Computes derived indicators
│   ├── build_site.py                     # Builds the static microsite
│   ├── run_pipeline.py                   # Runs the full pipeline
│   └── common.py                         # Shared utilities and column definitions
├── DATA_DICTIONARY.md                    # Full variable descriptions
├── METHODOLOGY.md                        # Data sources and harmonization methods
├── DATA_PAPER.md                         # Scientific dataset description paper
├── CHANGELOG.md                          # Version history
├── CITATION.cff                          # Machine-readable citation (CFF format)
├── CITATION.bib                          # BibTeX citation
└── LICENSE                               # CC0 1.0 Public Domain
```

---

## Variables Summary

Full descriptions in [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

**Identification (3 variables)**

| Variable | Description | Type |
|---|---|---|
| `País` | Country name | Categorical |
| `Año` | Observation year | Numeric |
| `Sexo` | Sex category (H = men, M = women, TOTAL) | Categorical |

**Demographic indicators (8 variables)**

| Variable | Description | Unit |
|---|---|---|
| `Pob_Total_Millones` | Total population | Millions |
| `Pct_Urbana` | Urban population share | % |
| `TFT` | Total fertility rate | Children/woman |
| `Esp_Vida_Años` | Life expectancy at birth | Years |
| `Mort_Inf_1k` | Infant mortality rate | Deaths/1,000 births |
| `Migr_Neta_k` | Net migration | Thousands |
| `Dens_hab_km2` | Population density | Inhabitants/km² |
| `Ind_Dependencia` | Dependency ratio | Ratio |

**Age structure — percentages (15 variables):** `Pct_0_4` · `Pct_5_9` · `Pct_10_14` · ... · `Pct_65_69` · `Pct_70_mas`

**Age structure — absolute counts in thousands (15 variables):** `Pob_0_4_k` · `Pob_5_9_k` · ... · `Pob_65_69_k` · `Pob_70_mas_k`

---

## Quick Start

### Python

```python
import pandas as pd

df = pd.read_csv("data/dataset.csv")

print(df.shape)            # (228, 41)
print(df["País"].nunique())  # 19
print(df["Año"].unique())  # [2000, 2005, 2010, 2015]

# Population pyramid data for Mexico, 2015, total population
mexico_2015 = df[
    (df["País"] == "México") &
    (df["Año"] == 2015) &
    (df["Sexo"] == "TOTAL")
]
pct_cols = [c for c in df.columns if c.startswith("Pct_")]
print(mexico_2015[pct_cols].T)
```

### R

```r
library(readr)
library(dplyr)

df <- read_csv("data/dataset.csv")

# Aging trend for Argentina (total population)
argentina_aging <- df %>%
  filter(País == "Argentina", Sexo == "TOTAL") %>%
  select(Año, Pob_Total_Millones, Pct_65_69, Pct_70_mas, Ind_Dependencia) %>%
  arrange(Año)

print(argentina_aging)
```

---

## Data Sources

Data compiled and harmonized from:

- **CEPAL** (Comisión Económica para América Latina y el Caribe)
- **World Bank** demographic databases
- **BBVA Research** demographic reports
- **National statistical institutes** (e.g., CONAPO for México)

---

## Validation

The dataset passes automated structural and arithmetic validation on every push to `main`:

- Percentage distributions across age groups sum to ~100% per observation
- Absolute population counts are consistent with reported total population
- No duplicate Country × Year × Sex combinations
- No negative values in numeric columns

Run validation locally:

```bash
pip install -r requirements.txt
python scripts/validate_dataset.py
# Expected output:
# Registros: 228
# Países: 19
# Años: [2000, 2005, 2010, 2015]
# VALIDACIÓN OK: dataset coherente a nivel estructural y aritmético.
```

---

## Citation

**APA 7:**

> De la Serna Tuya, J. M. (2026). *Latin America Population Age Structure Dataset* [Dataset]. GitHub. https://github.com/juanmoisesd/latin-america-population-age-structure-dataset

**BibTeX:**

```bibtex
@dataset{delaserna2026_latin_america_population_age,
  author    = {De la Serna Tuya, Juan Moisés},
  title     = {Latin America Population Age Structure Dataset},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/juanmoisesd/latin-america-population-age-structure-dataset},
  doi       = {10.17632/ygkmshr5fv.1},
  note      = {ORCID: 0000-0002-8401-8018}
}
```

Please also cite the archived dataset: [https://doi.org/10.17632/ygkmshr5fv.1](https://doi.org/10.17632/ygkmshr5fv.1)

See also: [CITATION.cff](CITATION.cff) · [CITATION.bib](CITATION.bib) · [CITATION_GUIDE.md](CITATION_GUIDE.md)

---

## Dataset Status

| Field | Value |
|---|---|
| Status | 🟢 Published |
| Dataset DOI | [10.17632/ygkmshr5fv.1](https://doi.org/10.17632/ygkmshr5fv.1) |
| Zenodo DOI | [10.5281/zenodo.18891177](https://doi.org/10.5281/zenodo.18891177) |
| Last update | 2026-03-20 |
| License | CC0 1.0 Universal |

---

## Author

**Juan Moisés de la Serna Tuya**
Universidad Internacional de La Rioja (UNIR)

| Profile | Link |
|---|---|
| Website | [juanmoisesdelaserna.es](https://juanmoisesdelaserna.es) |
| Email | juanmoises.delaserna@unir.net |
| ORCID | [0000-0002-8401-8018](https://orcid.org/0000-0002-8401-8018) |
| LinkedIn | [juanmoisesdelaserna](https://linkedin.com/in/juanmoisesdelaserna) |
| Scopus | [26632846700](https://www.scopus.com/authid/detail.uri?authorId=26632846700) |
| ResearcherID | M-8296-2019 |
| ResearchGate | [Juan_De_La_Serna_Tuya](https://www.researchgate.net/profile/Juan_De_La_Serna_Tuya) |

290+ scientific works · 500+ DOIs · 90+ open datasets · Top 1% Academia.edu

---

## License

[CC0 1.0 Universal — Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/)

This dataset is released into the public domain. You may copy, modify, distribute, and use the data, even for commercial purposes, without asking permission.

---

## Related Documentation

| File | Description |
|---|---|
| [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Full variable descriptions with units and types |
| [METHODOLOGY.md](METHODOLOGY.md) | Data sources, harmonization process, and decisions |
| [DATA_PAPER.md](DATA_PAPER.md) | Scientific dataset description paper |
| [GLOSSARY.md](GLOSSARY.md) | Key demographic terms and definitions |
| [ABOUT_THE_AUTHOR.md](ABOUT_THE_AUTHOR.md) | Extended author profile |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md) | Data sources acknowledgment |
