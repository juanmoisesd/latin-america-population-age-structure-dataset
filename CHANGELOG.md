# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] - 2026-03-22

### Improved
- README.md: complete rewrite with countries table, Quick Start code examples (Python/R), unified metadata, corrected citations to 2026
- data/README.md: unified license (CC0 1.0), corrected coverage (19 countries, 1995-2030)
- CHANGELOG.md: added real version history entries
- Removed erroneous file `METHODOLOGY.md,` (with trailing comma); correct `METHODOLOGY.md` preserved

### Fixed
- License inconsistency: data/README.md erroneously stated CC BY 4.0 — corrected to CC0 1.0 to match LICENSE file and all other metadata
- Year in APA citation corrected from 2025 to 2026
- Country count unified across all files (19 countries, consistent with DATA_DICTIONARY and DATA_PAPER)

---

## [1.0.1] - 2026-03-21

### Added
- Google Scholar and Dublin Core citation metatags in index.html
- Collection DOI badge in README (10.5281/zenodo.19145316)
- FUNDING.yml with support and visibility links
- _config.yml with Jekyll/GitHub Pages configuration and SEO metadata
- robots.txt updated to point to sitemap and allow full indexing
- sitemap.xml updated with GitHub Pages URLs
- seo.json updated with full Schema.org Dataset and author identifiers
- CITATION.cff updated to reference collection DOI

---

## [1.0.0] - 2026-03-20

### Added
- Initial release of the Latin America Population Age Structure Dataset
- Main dataset: `data/dataset.csv` (456 observations, 42 variables, 19 countries, 1995-2030)
- Derived datasets: `indicators_summary_by_country.csv`, `indicators_summary_by_year.csv`, `latest_snapshot.csv`
- Full documentation: DATA_DICTIONARY.md, METHODOLOGY.md, DATA_PAPER.md, DATASET_ABSTRACT.md
- Scientific metadata: CITATION.cff, CITATION.bib, codemeta.json, datapackage.json, ro-crate-metadata.json, PROV.json
- Processing pipeline: scripts/run_all.py, scripts/validate_dataset.py and supporting scripts
- Static microsite with 907 pages deployed on GitHub Pages
- License: CC0 1.0 Universal (Public Domain)
- DOI registered: 10.17632/ygkmshr5fv.1 (Mendeley Data) and 10.5281/zenodo.18891177 (Zenodo)