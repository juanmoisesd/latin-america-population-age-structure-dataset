# A Harmonized Dataset of Population Age Structure in Latin America (2000-2015)

## Abstract

This paper presents a harmonized dataset describing the population age structure and key demographic indicators for **19 Latin American countries** between **2000 and 2015** at quinquennial intervals (2000, 2005, 2010, 2015). The dataset provides observations of demographic structure disaggregated by sex and distributed across fifteen five-year age groups. In addition to age distribution, the dataset includes indicators such as total population size, fertility rates, life expectancy, infant mortality, migration balance, urbanization levels, population density, and dependency ratios. The dataset contains **228 country-year-sex observations** and **41 variables**, enabling comparative analysis of demographic transition, population aging, and demographic dividend dynamics across the region.

---

## 1. Background and Rationale

Demographic change represents one of the most important structural transformations affecting societies worldwide. Over the past decades, Latin America has experienced profound demographic transitions characterized by declining fertility rates, increasing life expectancy, changes in migration patterns, and progressive population aging. These dynamics have important implications for labor markets, economic development, health systems, social protection, and public policy design.

Although demographic information is widely available through international organizations and national statistical offices, researchers frequently face difficulties when conducting comparative analyses across countries and time periods. Differences in data formats, variable definitions, age group classifications, and temporal coverage often limit the comparability of demographic datasets.

To address these limitations, this project compiles and harmonizes demographic data from multiple international sources to provide a consistent dataset describing the population age structure of 19 Latin American countries between 2000 and 2015.

---

## 2. Methods

### 2.1 Data Sources

The dataset was constructed by compiling demographic information from:

- **CEPAL** - Comision Economica para America Latina y el Caribe (primary source)
- **World Bank** - demographic databases
- **BBVA Research** - regional demographic reports
- **National statistical institutes** - CONAPO (Mexico), DANE (Colombia), INDEC (Argentina), and others

### 2.2 Data Harmonization

The harmonization process involved:

1. Standardizing age classifications into 15 quinquennial age groups (0-4 through 70+)
2. Aligning temporal observations to quinquennial intervals: 2000, 2005, 2010, 2015
3. Harmonizing variable names, units, and encoding across sources
4. Ensuring consistency between population totals and age group distributions
5. Encoding sex categories uniformly as H (men), M (women), TOTAL

### 2.3 Unit of Observation

Each observation corresponds to a unique combination of **Country x Year x Sex**.

---

## 3. Data Records

### 3.1 Countries Covered (19)

Argentina, Bolivia, Brasil, Chile, Colombia, Costa Rica, Cuba, Ecuador, El Salvador, Guatemala, Honduras, Mexico, Nicaragua, Panama, Paraguay, Peru, Republica Dominicana, Uruguay, Venezuela.

### 3.2 Temporal Coverage

- **Period:** 2000-2015
- **Time points:** 2000, 2005, 2010, 2015
- **Frequency:** Quinquennial

### 3.3 Dataset Size

| Dimension | Value |
|---|---|
| Countries | 19 |
| Time points | 4 (2000, 2005, 2010, 2015) |
| Sex categories | 3 (H, M, TOTAL) |
| Total observations | 228 |
| Variables | 41 |

### 3.4 Variables

**Identification variables:** Pais, Ano, Sexo

**Demographic indicators (8):** Pob_Total_Millones, Pct_Urbana, TFT, Esp_Vida_Anos, Mort_Inf_1k, Migr_Neta_k, Dens_hab_km2, Ind_Dependencia

**Age structure - percentage distribution (15):** Pct_0_4 through Pct_70_mas

**Age structure - absolute counts in thousands (15):** Pob_0_4_k through Pob_70_mas_k

---

## 4. Technical Validation

Automated validation was applied using scripts/validate_dataset.py. Results for the current version:

| Validation check | Result |
|---|---|
| Total records | 228 |
| Countries | 19 |
| Years | 2000, 2005, 2010, 2015 |
| Duplicate Country x Year x Sex | None found |
| Rows where age percentages sum outside [99.5, 100.5] | None found |
| Negative values in numeric columns | None found |
| Population total vs. age group mismatch (>0.2M) | None found |
| **Overall validation status** | PASS |

---

## 5. Usage Notes

The dataset can support a wide range of demographic and socioeconomic analyses, including: demographic transition studies, population aging analysis, demographic dividend estimation, dependency ratio analysis, cross-country comparisons, and population pyramid visualization.

The CSV format allows direct import into Python (pandas), R (readr), Stata, SPSS, and any spreadsheet application.

Quick Start (Python):

    import pandas as pd
    df = pd.read_csv("data/dataset.csv")
    print(df.shape)  # (228, 41)

---

## 6. Derived Datasets

The repository also includes derived datasets with computed indicators:

| File | Description |
|---|---|
| data/dataset_with_indicators.csv | Main dataset + computed demographic indicators |
| data/indicators_summary_by_country.csv | Indicators aggregated by country |
| data/indicators_summary_by_year.csv | Indicators aggregated by year |

---

## 7. Data Availability

The dataset is publicly available through:

- **Mendeley Data:** https://doi.org/10.17632/ygkmshr5fv.1
- **Zenodo:** https://doi.org/10.5281/zenodo.18891177
- **GitHub:** https://github.com/juanmoisesd/latin-america-population-age-structure-dataset

All files are distributed under **CC0 1.0 Universal - Public Domain Dedication**.

---

## 8. Author Information

Juan Moises de la Serna Tuya
Universidad Internacional de La Rioja (UNIR)
ORCID: https://orcid.org/0000-0002-8401-8018
Email: juanmoises.delaserna@unir.net
