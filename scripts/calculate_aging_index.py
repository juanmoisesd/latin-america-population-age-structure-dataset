"""
calculate_aging_index.py
Calcula el indice de envejecimiento para cada registro del dataset.
Indice de envejecimiento = (Pob_65_mas_Miles / Pob_0_14_Miles) * 100
Entrada:  data/dataset.csv
Salida:   data/dataset_with_aging_index.csv
Requiere: pandas
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

df = pd.read_csv(DATA_DIR / "dataset.csv")

df["Indice_Envejecimiento"] = (
    df["Pob_65_más_Miles"] / df["Pob_0_14_Miles"] * 100
).round(2)

out = DATA_DIR / "dataset_with_aging_index.csv"
df.to_csv(out, index=False, encoding="utf-8")
print(f"Guardado: {out}")
print(df[["País","Año","Pob_65_más_Miles","Pob_0_14_Miles","Indice_Envejecimiento"]].to_string(index=False))
