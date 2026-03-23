# Known Issues and Limitations

This document lists known issues, limitations, and caveats for the **Latin America Population Age Structure Dataset**. Users should be aware of these before using the data in research or analysis.

---

## 1. Population Projections (2025–2030)

**Status:** Expected behavior  
**Severity:** Low  
**Affected files:** All CSV files, rows where `year >= 2025`

Population values for years 2025 and 2030 are **projections** based on CEPALSTAT models, not census-derived counts. These values carry inherent uncertainty, especially for countries with recent political instability or limited statistical capacity.

**Impact:** Trend analyses that cross the 2024/2025 boundary should account for the shift from observed to projected data.

**Recommendation:** Filter to `year <= 2024` if your analysis requires only observed/census data.

---

## 2. Methodological Differences Between Source Countries

**Status:** Structural limitation  
**Severity:** Medium  
**Affected files:** All CSV files

CEPALSTAT aggregates demographic data from national statistical institutes (INE, DANE, IBGE, etc.), census bureaus, and vital registration systems. Each country uses different:
- Census methodologies and intervals (some countries have not had a census since 2010)
- Population projection models and base years
- Age group aggregation standards

**Impact:** Cross-country comparisons should be interpreted with caution, particularly for Bolivia, Paraguay, and Venezuela where the most recent census data is older (2012 or earlier).

**Recommendation:** Consult `METHODOLOGY.md` for source-specific details and consider using percentage variables (`pct_*`) instead of absolute counts for cross-country comparisons.

---

## 3. ASCII Encoding of Variable Names

**Status:** Design decision  
**Severity:** Low  
**Affected files:** `DATA_DICTIONARY.md`, all CSV column headers

Variable names use underscores and ASCII characters only (e.g., `pct_65_mas` instead of `pct_65+`, `pct_0_14` instead of `pct_0–14`). This was done to maximize compatibility with R, Python, SQL, and spreadsheet software.

**Impact:** The suffix `_mas` (Spanish for "plus/more") may be unfamiliar to non-Spanish-speaking users. The column `pct_65_mas` means "percentage of population aged 65 and above."

**Recommendation:** Refer to `DATA_DICTIONARY.md` for full variable definitions.

---

## 4. Venezuela Data Gaps (2016–2022)

**Status:** Source limitation  
**Severity:** Medium  
**Affected files:** All CSV files, rows where `country == "Venezuela"`

Venezuela's national statistical institute (INE) suspended regular publications between 2016 and 2022. Data for this period is based on CEPALSTAT estimates derived from the 2011 census and regional demographic models.

**Impact:** Venezuelan time-series from 2016–2022 may be less reliable than other countries in the dataset.

---

## 5. Haiti Data Availability

**Status:** Source limitation  
**Severity:** Medium  
**Affected files:** All CSV files, rows where `country == "Haiti"`

Haiti's demographic data is particularly uncertain due to the 2010 earthquake, political instability, and lack of a recent census (last census: 2003). Values are CEPALSTAT projections with higher uncertainty bands.

---

## 6. No Subnational Disaggregation

**Status:** Scope limitation  
**Severity:** Informational  

The dataset contains **national-level data only**. Regional, provincial, or municipal breakdowns are not included. Users needing subnational data should consult national statistical institutes directly.

---

## 7. Age Group Resolution

**Status:** Design constraint  
**Severity:** Low  

The dataset uses broad age groups (0–14, 15–64, 65+) following the standard CEPALSTAT classification. More granular age brackets (e.g., 5-year cohorts) are available in the original CEPALSTAT source but were out of scope for this dataset version.

**Recommendation:** If your analysis requires 5-year cohort data, access CEPALSTAT directly at https://statistics.cepal.org/portal/cepalstat/

---

## 8. Dependency Ratio Calculation

**Status:** Methodology note  
**Severity:** Low  
**Affected variable:** `dependency_ratio`

The dependency ratio is calculated as:
```
dependency_ratio = (pop_0_14 + pop_65_mas) / pop_15_64
```

This uses the standard economic dependency definition. Some alternative definitions exclude the elderly population or use different age boundaries (e.g., 15–59 instead of 15–64). Results may differ from other sources using alternative definitions.

---

## 9. CEPALSTAT Source Updates

**Status:** Ongoing  
**Severity:** Low  

CEPALSTAT periodically revises historical estimates as new census data or methodological improvements become available. This dataset represents a snapshot taken in **early 2026**. Future CEPALSTAT revisions may differ slightly from values in this dataset.

---

## Reporting New Issues

If you discover additional issues or inconsistencies, please open a GitHub Issue at:  
https://github.com/juanmoisesd/latin-america-population-age-structure-dataset/issues

Include: the affected file(s), the specific rows/values in question, and the expected vs. observed behavior.

---

*Last updated: March 2026 | Dataset version: 1.1.0*
