# Demographic Atlas – Latin America Population Age Structure Dataset

This directory contains the interactive demographic atlas for the project:

Latin America Population Age Structure Dataset (2000–2023)

The atlas provides a visual exploration of the dataset through interactive charts and demographic indicators derived from the population age structure.

It is designed as a lightweight static visualization tool that can be published directly using GitHub Pages.

---

# Contents

The atlas directory is organized as follows:

atlas/
├── index.html
├── assets/
│   ├── atlas.css
│   └── atlas.js
├── data/
│   ├── atlas_data.json
│   └── atlas_indicators.csv
└── README.md

---

### index.html

Main entry point of the interactive atlas.

It loads the visualization interface and renders demographic charts using the data stored in the data/ directory.

---

### assets/

Contains the front-end resources used by the atlas.

atlas.css – styles for layout, typography, and charts  
atlas.js – JavaScript logic for loading data and rendering visualizations

---

### data/

Contains processed datasets specifically prepared for the atlas visualizations.

atlas_data.json  
Main data source used by the browser and optimized for JavaScript visualizations.

atlas_indicators.csv  
Dataset including demographic indicators derived from the base dataset.

---

# Data source

The atlas is derived from the main dataset located in the repository:

data/dataset.csv

This dataset includes demographic information on the population age structure of selected Latin American countries for the years:

- 2000  
- 2010  
- 2020  
- 2023  

---

# Indicators included in the atlas

The atlas visualizations may include indicators such as:

- population age distribution
- youth population share
- elderly population share
- aging index
- demographic structure trends

These indicators are calculated using scripts located in the scripts/ directory.

---

# Regenerating the atlas data

Atlas data files are generated using Python scripts.

Typical workflow:

python scripts/calculate_aging_index.py
python scripts/build_atlas_data.py

This process produces:

atlas/data/atlas_data.json  
atlas/data/atlas_indicators.csv

---

# Publishing

The atlas is designed to work as a static web application.

Once deployed, the atlas can be accessed via:

/atlas/index.html

---

# License

Creative Commons Attribution 4.0 International (CC BY 4.0)

---

# Author

Juan Moisés de la Serna  
ORCID: https://orcid.org/0000-0002-8401-8018
