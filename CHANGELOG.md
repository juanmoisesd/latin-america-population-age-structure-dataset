# CHANGELOG

All notable changes to this project will be documented in this file.

The format follows **Keep a Changelog** and **Semantic Versioning**.

---

## [1.1.0] - 2026-03-09

### Updated

* Dataset structure expanded to include:

  * population totals
  * percentage age structure
  * population counts by age group (thousands)
  * source metadata
* Dataset now includes the following fields:

```
País
Año
Población_Total_Millones
Pct_0_14
Pct_15_24
Pct_25_54
Pct_55_64
Pct_65_más
Pob_0_14_Miles
Pob_15_24_Miles
Pob_25_54_Miles
Pob_55_64_Miles
Pob_65_más_Miles
Fuente
```

This allows both **relative demographic analysis (percentages)** and **absolute demographic analysis (population counts)**.

---

### Added

New derived indicators supported by the pipeline:

**Demographic structure indicators**

* Aging Index
* Youth Index
* Total Dependency Ratio
* Youth Dependency Ratio
* Old-age Dependency Ratio
* Demographic Dividend Index
* Working-age Population Share
* Youth Population Share
* Elderly Population Share

**Population size indicators**

* Dependent Population (thousands)
* Working-age Population (thousands)
* Old-age Ratio (absolute population)
* Youth-to-Elderly Ratio

**Transition indicators**

* Demographic Transition Score
* Population Aging Speed
* Working-age Ratio

---

### Scripts Updated

The data processing pipeline has been adapted to the new dataset structure.

Scripts included:

```
scripts/
│
├── validate_dataset.py
│   Validates dataset structure, missing values, and percentage totals.
│
├── build_indicators.py
│   Computes all demographic indicators.
│
├── build_atlas_data.py
│   Generates atlas-ready JSON files for visualization.
│
├── generate_research_pages.py
│   Generates research-oriented HTML pages automatically.
│
├── build_site.py
│   Builds the complete static site for GitHub Pages.
│
└── run_all.py
    Executes the full pipeline automatically.
```

---

### Atlas Integration

The demographic atlas uses processed data generated automatically.

```
docs/
└── atlas/
    ├── index.html
    ├── assets/
    │   ├── atlas.js
    │   └── atlas.css
    └── data/
        ├── atlas_data.json
        └── atlas_indicators.csv
```

Atlas includes:

* country demographic profiles
* population age structure visualization
* aging comparison between countries
* demographic dividend indicators

---

### Research Outputs Automatically Generated

The pipeline generates research-oriented outputs including:

* Country demographic reports
* Cross-country comparisons
* Ranking tables
* Demographic transition analysis
* Aging dynamics analysis

Examples:

```
docs/research/
├── aging_trends.html
├── demographic_dividend.html
├── dependency_ratios.html
└── country_profiles/
```

---

### Reproducibility

The project implements a **fully reproducible research pipeline**:

```
python scripts/run_all.py
```

This automatically:

1. Validates dataset
2. Generates demographic indicators
3. Produces atlas data
4. Builds research pages
5. Generates the static website

---

### Compatibility

The generated website is compatible with:

* GitHub Pages
* static hosting
* academic data repositories
* research reproducibility workflows

---

### Data Sources

Primary demographic sources referenced in the dataset:

* CEPAL (Economic Commission for Latin America and the Caribbean)
* World Bank
* BBVA Research

---

### Citation

Dataset citation format:

```
De la Serna, J. M. (2026).
Latin America Population Age Structure Dataset (2000–2023).
Zenodo.
https://doi.org/10.5281/zenodo.18883431
```
