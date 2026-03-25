"""Harmonized demographic dataset: population age structure in Latin America (19 co
DOI:https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/"""
__version__="1.0.0"
import pandas as pd,io,requests
def load_data(f=None):
  rid="https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/".split(".")[-1];m=requests.get("https://zenodo.org/api/records/"+rid,timeout=30).json();csvs=[x for x in m.get("files",[]) if x["key"].endswith(".csv")]
  if not csvs:raise ValueError("No CSV")
  tgt=next((x for x in csvs if f and x["key"]==f),csvs[0]);return pd.read_csv(io.StringIO(requests.get(tgt["links"]["self"],timeout=60).text))
def cite():return "de la Serna, Juan Moisés (2025). Harmonized demographic dataset: population age structure in "
def info():print("DOI: https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/\nGitHub: https://github.com/juanmoisesd/latin-america-population-age-structure-dataset")
