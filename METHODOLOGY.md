# Methodology

## Latin America Population Age Structure Dataset (2000–2015)

This document describes the methodological procedures used to compile, harmonize, and validate the **Latin America Population Age Structure Dataset**.

The objective of the dataset is to provide a **consistent and comparable demographic database** describing population age structure and key demographic indicators for Latin American countries.

---

## 1. Study Scope

The dataset covers **19 countries in Latin America** and provides demographic information for the period **2000–2015**.

Observations are reported at **quinquennial intervals**:

- 2000
- 2005
- 2010
- 2015

Each observation corresponds to a unique combination of:

**Country × Year × Sex**

Sex categories included in the dataset are:

- `H` — Men
- `M` — Women
- `TOTAL` — Total population

This structure yields a maximum of **228 observations** (19 countries × 4 years × 3 sex categories).

---

## 2. Countries Covered (19)

Argentina, Bolivia, Brasil, Chile, Colombia, Costa Rica, Cuba, Ecuador, El Salvador, Guatemala, Honduras, México, Nicaragua, Panamá, Paraguay, Perú, República Dominicana, Uruguay, Venezuela.

---

## 3. Data Sources

The dataset was constructed using demographic data obtained from the following international and regional statistical sources:

- **CEPAL** — Comisión Económica para América Latina y el Caribe (primary source)
- **World Bank** — demographic databases
- **BBVA Research** — regional demographic reports
- **National statistical institutes** — e.g., CONAPO (Mexico), DANE (Colombia), INDEC (Argentina)

Source identifiers are recorded in the `Fuente` variable in the dataset for traceability.

---

## 4. Variables

The dataset includes three groups of variables:

### 4.1 Identification Variables

| Variable | Description |
|---|---|
| `País` | Country name |
| `Año` | Observation year |
| `Sexo` | Sex category (H, M, TOTAL) |

### 4.2 Demographic Indicators

| Variable | Description | Unit |
|---|---|---|
| `Pob_Total_Millones` | Total population | Millions |
| `Pct_Urbana` | Urban population share | % |
| `TFT` | Total fertility rate | Children/woman |
| `Esp_Vida_Años` | Life expectancy at birth | Years |
| `Mort_Inf_1k` | Infant mortality rate | Deaths/1,000 live births |
| `Migr_Neta_k` | Net migration | Thousands |
| `Dens_hab_km2` | Population density | Inhabitants/km² |
| `Ind_Dependencia` | Dependency ratio | Ratio |

### 4.3 Age Structure Variables

Age structure is represented through **15 quinquennial age groups** (0–4, 5–9, ..., 65–69, 70+), provided in two complementary forms:

- **Percentage distribution** (`Pct_0_4` through `Pct_70_mas`): share of total population in each group
- **Absolute counts in thousands** (`Pob_0_4_k` through `Pob_70_mas_k`): population in each group

---

## 5. Harmonization Process

Because the original sources present demographic data in different formats and classification schemes, the data were harmonized to ensure cross-country and cross-year comparability. The harmonization process included:

1. **Standardizing age group classifications** into 15 quinquennial groups (0–4 through 70+)
2. **Aligning temporal observations** to 5-year intervals (2000, 2005, 2010, 2015)
3. **Harmonizing variable names and units** across sources
4. **Ensuring consistency** between percentage distributions and absolute population counts
5. **Encoding sex categories** uniformly as H / M / TOTAL

---

## 6. Data Validation

The dataset was validated using automated checks implemented in `scripts/validate_dataset.py`:

| Check | Description |
|---|---|
| **No duplicates** | Each Country × Year × Sex combination is unique |
| **Percentage sums** | Age group percentages sum to ~100% per observation (tolerance: ±0.5%) |
| **Population consistency** | Absolute age group counts are consistent with reported total population (tolerance: ±0.2M) |
| **No negative values** | All numeric variables are non-negative |

---

## 7. Format and Interoperability

The dataset is distributed in **CSV format (UTF-8 encoding)**, compatible with:

- Python (pandas, polars)
- R (readr, data.table)
- Stata, SPSS, Matlab
- Any spreadsheet or data visualization tool

---

## 8. Limitations

- Coverage is limited to **4 time points** (2000, 2005, 2010, 2015); annual estimates are not included.
- For some countries and years, certain demographic indicators may be estimated rather than directly observed.
- Population counts are expressed in **thousands** and rounded; small rounding discrepancies may occur.

---

## 9. License

This dataset is released under [CC0 1.0 Universal — Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/).

---

## 10. Contact

Juan Moisés de la Serna Tuya
ORCID: [0000-0002-8401-8018](https://orcid.org/0000-0002-8401-8018)
Email: juanmoises.delaserna@unir.net
