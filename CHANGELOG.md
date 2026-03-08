# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on *Keep a Changelog* and semantic versioning.

---

## [1.0.0] - 2026-03-08

### Added
- Initial demographic dataset for Latin America (2000, 2010, 2020, 2023).
- Scripts pipeline for dataset processing:
  - `validate_dataset.py`
  - `build_indicators.py`
  - `build_atlas_data.py`
  - `generate_research_pages.py`
  - `build_site.py`
  - `run_all.py`
- Automatic generation of:
  - demographic indicators
  - atlas JSON data
  - country pages
  - comparison pages
  - research question pages
- Static site compatible with GitHub Pages.
- Atlas interactive structure in `docs/atlas`.
- Reproducible research pipeline.

### Indicators Implemented
- Aging Index
- Total Dependency Ratio
- Demographic Dividend Index
- Youth Population Share
- Working-age Population Share

### Infrastructure
- Python-based reproducible pipeline
- Dataset validation script
- Automatic HTML generation for research outputs

