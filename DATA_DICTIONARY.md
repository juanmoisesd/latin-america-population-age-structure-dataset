# Data Dictionary

## Latin America Population Age Structure Dataset (2000-2015)

This document describes the variables included in the **Latin America Population Age Structure Dataset**.

The dataset contains demographic indicators and population age structure variables for **19 Latin American countries**, covering the period **2000-2015** at quinquennial intervals (2000, 2005, 2010, 2015).

Each row represents a **Country x Year x Sex** observation.

---

## Identification Variables

| Variable | Description | Unit | Type |
|---|---|---|---|
| `Pais` | Country name | Text | Categorical |
| `Ano` | Observation year | Year | Numeric |
| `Sexo` | Sex category (H = men, M = women, TOTAL = total population) | Category | Categorical |

---

## General Demographic Indicators

| Variable | Description | Unit | Type |
|---|---|---|---|
| `Pob_Total_Millones` | Total population | Millions of inhabitants | Numeric |
| `Pct_Urbana` | Percentage of population living in urban areas | Percent (%) | Numeric |
| `TFT` | Total fertility rate | Children per woman | Numeric |
| `Esp_Vida_Anos` | Life expectancy at birth | Years | Numeric |
| `Mort_Inf_1k` | Infant mortality rate | Deaths per 1,000 live births | Numeric |
| `Migr_Neta_k` | Net migration | Thousands of people | Numeric |
| `Dens_hab_km2` | Population density | Inhabitants per square kilometer | Numeric |
| `Ind_Dependencia` | Total dependency ratio | Ratio | Numeric |

---

## Age Structure Variables (Percentage)

These variables describe the percentage of the population in each quinquennial age group. Values sum to approximately 100% for each observation.

| Variable | Description | Unit | Type |
|---|---|---|---|
| `Pct_0_4` | Population aged 0-4 years | Percent (%) | Numeric |
| `Pct_5_9` | Population aged 5-9 years | Percent (%) | Numeric |
| `Pct_10_14` | Population aged 10-14 years | Percent (%) | Numeric |
| `Pct_15_19` | Population aged 15-19 years | Percent (%) | Numeric |
| `Pct_20_24` | Population aged 20-24 years | Percent (%) | Numeric |
| `Pct_25_29` | Population aged 25-29 years | Percent (%) | Numeric |
| `Pct_30_34` | Population aged 30-34 years | Percent (%) | Numeric |
| `Pct_35_39` | Population aged 35-39 years | Percent (%) | Numeric |
| `Pct_40_44` | Population aged 40-44 years | Percent (%) | Numeric |
| `Pct_45_49` | Population aged 45-49 years | Percent (%) | Numeric |
| `Pct_50_54` | Population aged 50-54 years | Percent (%) | Numeric |
| `Pct_55_59` | Population aged 55-59 years | Percent (%) | Numeric |
| `Pct_60_64` | Population aged 60-64 years | Percent (%) | Numeric |
| `Pct_65_69` | Population aged 65-69 years | Percent (%) | Numeric |
| `Pct_70_mas` | Population aged 70 years and older | Percent (%) | Numeric |

---

## Age Structure Variables (Population Counts)

These variables represent absolute population counts for each age group, expressed in thousands of people.

| Variable | Description | Unit | Type |
|---|---|---|---|
| `Pob_0_4_k` | Population aged 0-4 years | Thousands of people | Numeric |
| `Pob_5_9_k` | Population aged 5-9 years | Thousands of people | Numeric |
| `Pob_10_14_k` | Population aged 10-14 years | Thousands of people | Numeric |
| `Pob_15_19_k` | Population aged 15-19 years | Thousands of people | Numeric |
| `Pob_20_24_k` | Population aged 20-24 years | Thousands of people | Numeric |
| `Pob_25_29_k` | Population aged 25-29 years | Thousands of people | Numeric |
| `Pob_30_34_k` | Population aged 30-34 years | Thousands of people | Numeric |
| `Pob_35_39_k` | Population aged 35-39 years | Thousands of people | Numeric |
| `Pob_40_44_k` | Population aged 40-44 years | Thousands of people | Numeric |
| `Pob_45_49_k` | Population aged 45-49 years | Thousands of people | Numeric |
| `Pob_50_54_k` | Population aged 50-54 years | Thousands of people | Numeric |
| `Pob_55_59_k` | Population aged 55-59 years | Thousands of people | Numeric |
| `Pob_60_64_k` | Population aged 60-64 years | Thousands of people | Numeric |
| `Pob_65_69_k` | Population aged 65-69 years | Thousands of people | Numeric |
| `Pob_70_mas_k` | Population aged 70 years and older | Thousands of people | Numeric |

---

## Metadata Variable

| Variable | Description | Unit | Type |
|---|---|---|---|
| `Fuente` | Source of the demographic data | Text | Categorical |

---

## Dataset Summary

| Dimension | Value |
|---|---|
| Countries | 19 |
| Time points | 4 (2000, 2005, 2010, 2015) |
| Sex categories | 3 (H, M, TOTAL) |
| Total observations | 228 |
| Variables | 41 |
| File | data/dataset.csv |

---

## Notes

- Percentages across age groups sum approximately to 100% for each observation (tolerance: +/- 0.5%).
- Absolute population counts correspond to the same age groups expressed in thousands of inhabitants.
- The `Fuente` variable records the source identifier for each observation, enabling traceability.
- Observations are structured as Country x Year x Sex.

---

## Related Files

- [README.md](../README.md) - Repository overview and quick start
- [METHODOLOGY.md](../METHODOLOGY.md) - Data sources and harmonization process
- [DATA_PAPER.md](../DATA_PAPER.md) - Scientific dataset description
- [GLOSSARY.md](../GLOSSARY.md) - Key demographic terms
