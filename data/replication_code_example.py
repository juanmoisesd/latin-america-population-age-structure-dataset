"""
Ejemplo de uso del dataset demográfico de América Latina

Autor: Juan Moisés de la Serna
Dataset DOI: https://doi.org/10.5281/zenodo.18883431
"""

import pandas as pd

# cargar dataset
df = pd.read_csv("dataset.csv")

# mostrar primeras filas
print("Primeras filas del dataset")
print(df.head())

# calcular promedio regional de población mayor de 65 años
aging = df.groupby("Año")["Pct65ms"].mean()

print("\nPromedio regional de población de 65 años o más:")
print(aging)

# identificar país con mayor envejecimiento en el último año disponible
latest_year = df["Año"].max()

latest = df[df["Año"] == latest_year]

max_country = latest.sort_values("Pct65ms", ascending=False).iloc[0]

print("\nPaís con mayor envejecimiento en el último año:")
print(max_country["PasAo"], max_country["Pct65ms"])
