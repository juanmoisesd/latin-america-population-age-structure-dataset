# Data Dictionary

## Latin America Population Age Structure Dataset (1995–2030)

This document describes the variables included in the dataset **Latin America Population Age Structure Dataset (1995–2030)**. The dataset contains demographic indicators and population age structure variables for 19 Latin American countries.

Each row represents a **Country × Year × Sex** observation.

---

# Identification Variables

| Variable | Description | Unit | Type |
|--------|-------------|------|------|
| Country | Country name | Text | Categorical |
| Year | Observation year | Year | Numeric |
| Sex | Sex category (H = men, M = women, TOTAL = total population) | Category | Categorical |

---

# General Demographic Indicators

| Variable | Description | Unit | Type |
|--------|-------------|------|------|
| Pob_Total_Millones | Total population | Millions of inhabitants | Numeric |
| Pct_Urbana | Percentage of population living in urban areas | Percent (%) | Numeric |
| TFT | Total fertility rate | Children per woman | Numeric |
| Esp_Vida_Años | Life expectancy at birth | Years | Numeric |
| Mort_Inf_1k | Infant mortality rate | Deaths per 1,000 live births | Numeric |
| Migr_Neta_k | Net migration | Thousands of people | Numeric |
| Dens_hab_km2 | Population density | Inhabitants per square kilometer | Numeric |
| Ind_Dependencia | Total dependency ratio | Ratio | Numeric |

---

# Age Structure Variables (Percentage)

These variables describe the **percentage of the population in each quinquennial age group**.

| Variable | Description | Unit | Type |
|--------|-------------|------|------|
| Pct_0_4 | Population aged 0–4 years | Percent (%) | Numeric |
| Pct_5_9 | Population aged 5–9 years | Percent (%) | Numeric |
| Pct_10_14 | Population aged 10–14 years | Percent (%) | Numeric |
| Pct_15_19 | Population aged 15–19 years | Percent (%) | Numeric |
| Pct_20_24 | Population aged 20–24 years | Percent (%) | Numeric |
| Pct_25_29 | Population aged 25–29 years | Percent (%) | Numeric |
| Pct_30_34 | Population aged 30–34 years | Percent (%) | Numeric |
| Pct_35_39 | Population aged 35–39 years | Percent (%) | Numeric |
| Pct_40_44 | Population aged 40–44 years | Percent (%) | Numeric |
| Pct_45_49 | Population aged 45–49 years | Percent (%) | Numeric |
| Pct_50_54 | Population aged 50–54 years | Percent (%) | Numeric |
| Pct_55_59 | Population aged 55–59 years | Percent (%) | Numeric |
| Pct_60_64 | Population aged 60–64 years | Percent (%) | Numeric |
| Pct_65_69 | Population aged 65–69 years | Percent (%) | Numeric |
| Pct_70_mas | Population aged 70 years and older | Percent (%) | Numeric |

---

# Age Structure Variables (Population Counts)

These variables represent **absolute population counts for each age group**.

Values are expressed in **thousands of people**.

| Variable | Description | Unit | Type |
|--------|-------------|------|------|
| Pob_0_4_k | Population aged 0–4 years | Thousands of people | Numeric |
| Pob_5_9_k | Population aged 5–9 years | Thousands of people | Numeric |
| Pob_10_14_k | Population aged 10–14 years | Thousands of people | Numeric |
| Pob_15_19_k | Population aged 15–19 years | Thousands of people | Numeric |
| Pob_20_24_k | Population aged 20–24 years | Thousands of people | Numeric |
| Pob_25_29_k | Population aged 25–29 years | Thousands of people | Numeric |
| Pob_30_34_k | Population aged 30–34 years | Thousands of people | Numeric |
| Pob_35_39_k | Population aged 35–39 years | Thousands of people | Numeric |
| Pob_40_44_k | Population aged 40–44 years | Thousands of people | Numeric |
| Pob_45_49_k | Population aged 45–49 years | Thousands of people | Numeric |
| Pob_50_54_k | Population aged 50–54 years | Thousands of people | Numeric |
| Pob_55_59_k | Population aged 55–59 years | Thousands of people | Numeric |
| Pob_60_64_k | Population aged 60–64 years | Thousands of people | Numeric |
| Pob_65_69_k | Population aged 65–69 years | Thousands of people | Numeric |
| Pob_70_mas_k | Population aged 70 years and older | Thousands of people | Numeric |

---

# Metadata Variable

| Variable | Description | Unit | Type |
|--------|-------------|------|------|
| Fuente | Source of the demographic data | Text | Categorical |

---

# Notes

- Percentages across age groups sum approximately to **100% for each observation**.
- Absolute population counts correspond to the **same age groups expressed in thousands of inhabitants**.
- The dataset includes **42 variables and 456 observations**.
- Observations are structured as **Country × Year × Sex**.
