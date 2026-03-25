"""Harmonized demographic dataset: population age structure in Latin America (19 countries, 2000-2015).
DOI: https://github.com/juanmoisesd/latin-america-population-age-structure-dataset | GitHub: https://github.com/juanmoisesd/latin-america-population-age-structure-dataset"""
__version__="1.0.0"
__author__="de la Serna, Juan Moisés"
import pandas as pd,io
try:
    import requests
except ImportError:
    raise ImportError("pip install requests")

def load_data(filename=None):
    """Load dataset from Zenodo. Returns pandas DataFrame."""
    rid="https://github.com/juanmoisesd/latin-america-population-age-structure-dataset".split(".")[-1]
    meta=requests.get(f"https://zenodo.org/api/records/{rid}",timeout=30).json()
    csvs=[f for f in meta.get("files",[]) if f["key"].endswith(".csv")]
    if not csvs:raise ValueError("No CSV found")
    f=next((x for x in csvs if filename and x["key"]==filename),csvs[0])
    return pd.read_csv(io.StringIO(requests.get(f["links"]["self"],timeout=60).text))

def cite():return f'de la Serna, Juan Moisés (2025). Harmonized demographic dataset: population age structure in Latin America (19 co. Zenodo. https://github.com/juanmoisesd/latin-america-population-age-structure-dataset'
def info():print(f"Dataset: Harmonized demographic dataset: population age structure in Latin America (19 co\nDOI: https://github.com/juanmoisesd/latin-america-population-age-structure-dataset\nGitHub: https://github.com/juanmoisesd/latin-america-population-age-structure-dataset")