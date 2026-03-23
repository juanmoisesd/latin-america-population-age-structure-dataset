# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] - 2026-03-23

### Added
- KNOWN_ISSUES.md: new file documenting 9 known limitations (projections, methodology differences, Venezuela/Haiti data gaps, encoding conventions, dependency ratio definition)

### Improved
- README.md: complete rewrite with 19-country table, Quick Start Python/R examples, badges, Known Limitations section, Dataset Status table
- DATA_PAPER.md: complete rewrite with 8 sections, FAIR compliance table, 19 countries, proper abstract and validation
- DATASET_ABSTRACT.md: aligned to 228 records, 41 variables, v1.1.0, DOI, CC0
- CITATION_GUIDE.md: updated to 19 countries, DOI, APA/BibTeX/RIS/Vancouver/MLA formats, v1.1.0
- codemeta.json: 19 countries, 1995-2030, v1.1.0, CC0, expanded keywords and metadata
- .zenodo.json: 19 countries, 1995-2030, v1.1.0, expanded keywords/subjects
- datapackage.json: 19 countries, 1995-2030, v1.1.0, added resources field with CSV path
- metadata.xml: 19 countries, 1995-2030, v1.1.0, DataCite schema with affiliation
- schema_org.jsonld: 19 countries, 1995-2030, v1.1.0, DOI, spatialCoverage, temporalCoverage
- VERSION: bumped 1.0.0 -> 1.1.0
- VERSION.md: aligned to v1.1.0 history

### Fixed
- Inconsistent version/country/period references across all metadata files (all now v1.1.0, 19 countries, 1995-2030)

### Removed
- docs_public/social_media_posts.md: inappropriate for scientific repository
- press_release.md: non-standard file for scientific dataset repository

---

## [1.0.1] - 2026-03-22

### Improved
- README.md: Quick Start code examples (Python/R), improved country table, corrected citation year to 2026
- data/README.md: unified license (CC0 1.0), corrected coverage (19 countries, 1995-2030)
- CITATION.cff: added DOI field, expanded to 12 keywords, corrected abstract (19 countries), version 1.1.0
- CITATION.bib: corrected year 2025->2026, version 1.1.0, added abstract/keywords/license fields

### Fixed
- License inconsistency: data/README.md erroneously stated CC BY 4.0 — corrected to CC0 1.0
- Year in APA citation corrected from 2025 to 2026
- Country count unified across all files (19 countries)

### Removed
- METHODOLOGY.md, (file with trailing comma in filename): deleted

---

## [1.0.0] - 2026-03-20

### Added
- Initial release of the Latin America Population Age Structure Dataset
- Main dataset: `data/latin_america_population_age_structure.csv` (228 records, 41 variables, 19 countries, 1995-2030)
- Full documentation: DATA_DICTIONARY.md, METHODOLOGY.md, DATA_PAPER.md, DATASET_ABSTRACT.md
- Scientific metadata: CITATION.cff, CITATION.bib, codemeta.json, datapackage.json, ro-crate-metadata.json, PROV.json
- Processing pipeline: scripts/run_all.py, scripts/validate_dataset.py and supporting scripts
- Static microsite deployed on GitHub Pages
- License: CC0 1.0 Universal (Public Domain)
- DOI registered: 10.17632/ygkmshr5fv.1 (Mendeley Data)
