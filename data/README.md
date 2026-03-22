# Latin America Population Age Structure Dataset — Data Directory

**Author:** Juan Moisés de la Serna Tuya
**ORCID:** 0000-0002-8401-8018
**DOI:** https://doi.org/10.17632/ygkmshr5fv.1
**License:** CC0 1.0 Universal — Public Domain Dedication

---

## Description

This directory contains the main dataset and derived data files for the **Latin America Population Age Structure Dataset**.

The dataset provides harmonized demographic information describing the population age structure of **19 Latin American countries** over the period **1995–2030**, at quinquennial intervals.

---

## Coverage

| Field | Value |
|-------|-------|
| Countries | 19 |
| Period | 1995–2030 |
| Frequency | Quinquennial (1995, 2000, 2005, 2010, 2015, 2020, 2025, 2030) |
| Unit of observation | Country x Year x Sex |
| Observations | 456 |
| Variables | 42 |

---

## Files

| File | Description |
|------|-------------|
| `dataset.csv` | Main dataset (456 rows x 42 columns) |
| `indicators_summary_by_country.csv` | Aggregate indicators by country |
| `indicators_summary_by_year.csv` | Aggregate indicators by year |
| `latest_snapshot.csv` | Most recent year snapshot |

---

## Main Variables

**Identification:** `Country`, `Year`, `Sex` (H, M, TOTAL)

**Demographic indicators:** `Pob_Total_Millones`, `Pct_Urbana`, `TFT`, `Esp_Vida_Años`, `Mort_Inf_1k`, `Migr_Neta_k`, `Dens_hab_km2`, `Ind_Dependencia`

**Age structure (% distribution):** `Pct_0_4` through `Pct_70_mas` (15 quinquennial groups)

**Age structure (absolute counts, thousands):** `Pob_0_4_k` through `Pob_70_mas_k` (15 quinquennial groups)

For full variable descriptions, see [DATA_DICTIONARY.md](../DATA_DICTIONARY.md).

---

## Data Sources

- CEPAL (Economic Commission for Latin America and the Caribbean)
- World Bank
- BBVA Research
- National statistical institutes of Latin American countries

---

## How to Cite

> De la Serna Tuya, J. M. (2026). *Latin America Population Age Structure Dataset* (v1.0.0) [Dataset]. GitHub & Zenodo. https://doi.org/10.17632/ygkmshr5fv.1

---

## License

**CC0 1.0 Universal — Public Domain Dedication.**
No rights reserved. See https://creativecommons.org/publicdomain/zero/1.0/
