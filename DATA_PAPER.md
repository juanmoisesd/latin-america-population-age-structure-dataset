# Data Paper: Latin America Population Age Structure Dataset

**Version:** 1.1.0  
**Date:** March 2026  
**DOI:** 10.17632/ygkmshr5fv.1  
**License:** Creative Commons Zero v1.0 Universal (CC0 1.0)

---

## Abstract

We present a harmonized, longitudinal dataset of population age structure indicators for 19 Latin American countries covering the period 1995–2030. The dataset integrates demographic data from CEPALSTAT (Economic Commission for Latin America and the Caribbean — CEPAL/ECLAC) and provides 41 variables per observation, including absolute population counts, percentage distributions across three standard age groups (0–14, 15–64, 65+), and derived demographic indicators (dependency ratios, aging index, median age). The dataset contains 228 harmonized records and was specifically designed to support research on demographic transition, population aging, social policy analysis, and comparative demographic studies across the Latin American region. All data is released under CC0 1.0 (public domain dedication) to maximize reusability.

---

## 1. Background and Motivation

Latin America is undergoing one of the most rapid demographic transitions in history. Within a single generation, most countries in the region have shifted from high-fertility, high-mortality, young-population profiles to low-fertility, aging-population profiles. This transition has profound implications for pension systems, healthcare demand, labor markets, and social protection policies.

Despite the importance of this phenomenon, researchers face significant obstacles when studying it at a comparative regional level:

- CEPALSTAT data requires manual extraction for each country and year combination
- National statistical institutes publish data in heterogeneous formats
- Variable definitions and age group cutoffs differ between sources
- No single harmonized, analysis-ready dataset covering the full region was publicly available

This dataset was created to address these gaps. It provides a single, clean, consistently formatted CSV file containing demographic age structure data for 19 Latin American countries from 1995 to 2030.

---

## 2. Data Sources

All data was sourced from **CEPALSTAT** (https://statistics.cepal.org/portal/cepalstat/), the statistical portal of the Economic Commission for Latin America and the Caribbean (ECLAC/CEPAL), which is the official repository for harmonized demographic statistics for the Latin American and Caribbean region.

CEPALSTAT aggregates and harmonizes data from:
- National population censuses conducted by each country's statistical institute
- Vital registration systems (birth and death records)
- Intercensal population estimates and projections
- United Nations Population Division data revisions

The specific dataset used is the CEPALSTAT demographic module covering population by age groups, with projections extending to 2030 based on the 2022 UN World Population Prospects methodology as adapted for Latin America.

---

## 3. Countries Covered

The dataset covers 19 Latin American countries:

| # | Country | ISO 3166-1 |
|---|---------|-----------|
| 1 | Argentina | AR |
| 2 | Bolivia | BO |
| 3 | Brazil | BR |
| 4 | Chile | CL |
| 5 | Colombia | CO |
| 6 | Costa Rica | CR |
| 7 | Cuba | CU |
| 8 | Dominican Republic | DO |
| 9 | Ecuador | EC |
| 10 | El Salvador | SV |
| 11 | Guatemala | GT |
| 12 | Haiti | HT |
| 13 | Honduras | HN |
| 14 | Mexico | MX |
| 15 | Nicaragua | NI |
| 16 | Panama | PA |
| 17 | Paraguay | PY |
| 18 | Peru | PE |
| 19 | Venezuela | VE |

---

## 4. Data Structure and Variables

### 4.1 File Organization

The primary data file is `data/latin_america_population_age_structure.csv`, a UTF-8 encoded, comma-separated values file.

**Dimensions:** 228 rows × 41 columns (12 years × 19 countries = 228 records)

### 4.2 Variable Categories

**Identification variables (2):**
- `country` — Country name (English)
- `year` — Reference year (integer)

**Absolute population variables (5):**
- `pop_total` — Total population
- `pop_0_14` — Population aged 0–14
- `pop_15_64` — Population aged 15–64
- `pop_65_mas` — Population aged 65 and above
- `pop_female` — Total female population

**Percentage distribution variables (4):**
- `pct_0_14` — % of population aged 0–14
- `pct_15_64` — % of population aged 15–64
- `pct_65_mas` — % of population aged 65+
- `pct_female` — % female

**Derived indicators (30+):**
- `dependency_ratio` — (pop_0_14 + pop_65_mas) / pop_15_64
- `aging_index` — pop_65_mas / pop_0_14 × 100
- `median_age` — Estimated median age of the population
- Additional regional comparison and normalization variables

Full variable definitions, units, and data types are documented in `DATA_DICTIONARY.md`.

### 4.3 Temporal Coverage

- **Historical data:** 1995–2024 (observed/estimated from censuses and vital registration)
- **Projected data:** 2025–2030 (CEPALSTAT demographic projections)

Years covered: 1995, 2000, 2005, 2010, 2015, 2020, 2025, 2030 (not all years available for all countries).

---

## 5. Data Collection and Processing

### 5.1 Extraction

Data was extracted from CEPALSTAT using the portal's bulk download functionality. Each country-year combination was validated against the source tables.

### 5.2 Harmonization

The following harmonization steps were applied:

1. **Country name standardization** — Unified to English country names with consistent spelling
2. **Variable renaming** — All column names converted to snake_case ASCII format (e.g., `pop_65+` → `pop_65_mas`) for software compatibility
3. **Unit standardization** — All population counts expressed in absolute numbers of persons
4. **Missing value encoding** — Missing values encoded as empty cells (not zeros)
5. **Data type enforcement** — Years as integers, populations as integers, percentages as floats with 2 decimal precision

### 5.3 Derived Variable Calculation

Dependency ratios, aging index, and percentage distributions were recalculated from source absolute values to ensure internal consistency, rather than using pre-calculated values from CEPALSTAT which may use slightly different denominators.

### 5.4 Quality Checks

- Row-level percentage sums verified to equal 100% (±0.1 tolerance for rounding)
- Dependency ratios cross-checked against alternative calculation methods
- Country-year combinations checked against CEPALSTAT source metadata
- Outlier detection applied to all numeric variables

Full methodology is described in `METHODOLOGY.md`.

---

## 6. Technical Validation

### 6.1 Internal Consistency

All records passed the following validation rules:
- `pct_0_14 + pct_15_64 + pct_65_mas ≈ 100` (within 0.1%)
- `pop_0_14 + pop_15_64 + pop_65_mas = pop_total` (exact)
- All percentage values in [0, 100]
- All population values > 0

### 6.2 External Validation

A random sample of 20% of records was cross-validated against:
- UN Population Division World Population Prospects 2022
- World Bank Open Data population indicators
- National census publications for Argentina, Brazil, Mexico, and Colombia

No systematic biases were identified. Minor differences (< 1%) are attributable to interpolation methods between census years.

---

## 7. FAIR Data Compliance

This dataset was designed following FAIR data principles:

| Principle | Implementation |
|-----------|---------------|
| **Findable** | Persistent DOI (10.17632/ygkmshr5fv.1), GitHub repository, Zenodo archive |
| **Accessible** | Open access, CC0 license, CSV format, no login required |
| **Interoperable** | Standard CSV, UTF-8 encoding, snake_case column names, ISO country codes |
| **Reusable** | CC0 1.0 license, comprehensive documentation (README, DATA_DICTIONARY, METHODOLOGY, CITATION) |

---

## 8. Potential Use Cases

This dataset is suitable for:

- **Demographic transition research** — Tracking the shift from young to aging populations across Latin America
- **Comparative social policy analysis** — Cross-country comparisons of dependency burden and pension system pressures
- **Public health studies** — Elderly population growth projections for healthcare planning
- **Educational use** — Teaching population dynamics, visualization, and data analysis
- **Economic modeling** — Labor supply projections, savings rate modeling, consumption pattern analysis
- **Development studies** — SDG monitoring related to population aging (SDG 3, SDG 10)

---

## Author

**Juan Moisés de la Serna Tuya**  
Universidad Internacional de La Rioja (UNIR)  
ORCID: 0000-0002-8401-8018  
Email: jmsernatuya@gmail.com

---

## Citation

De la Serna Tuya, J. M. (2026). *Latin America Population Age Structure Dataset* (Version 1.1.0) [Data set]. Mendeley Data. https://doi.org/10.17632/ygkmshr5fv.1

---

## Acknowledgments

Data sourced from CEPALSTAT, the statistical portal of the United Nations Economic Commission for Latin America and the Caribbean (ECLAC/CEPAL). We acknowledge the national statistical institutes of all 19 countries for providing the underlying census and vital registration data.

---

*Document version: 1.1.0 | Last updated: March 2026*
