"""
generate_aging_trends.py
Genera graficos de linea con la evolucion del porcentaje de poblacion
de 65+ anios para cada pais entre 2000 y 2023.
Salida: figures/aging_trends/aging_trend_{pais}.png
        figures/aging_trends/aging_trends_all_countries.png
Requiere: pandas, matplotlib
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Configuración de rutas
BASE_DIR   = Path(__file__).resolve().parent.parent
FIGURE_DIR = BASE_DIR / "figures" / "aging_trends"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

DATA_PATH = BASE_DIR / "data" / "dataset.csv"

# Verificar existencia del dataset
if not DATA_PATH.exists():
    print(f"Error: No se encontró {DATA_PATH}")
    sys.exit(1)

# Cargar datos
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    print(f"Error al cargar el dataset: {e}")
    sys.exit(1)

# Verificar columnas requeridas
required_cols = {"País", "Año", "Pct_65_más"}
if not required_cols.issubset(df.columns):
    missing = required_cols - set(df.columns)
    print(f"Error: Faltan columnas requeridas: {missing}")
    sys.exit(1)

# Filtrar rango de años (2000-2023)
df = df[(df["Año"] >= 2000) & (df["Año"] <= 2023)]

if df.empty:
    print("Error: No hay datos en el rango 2000-2023")
    sys.exit(1)

paises = sorted(df["País"].unique())

# Paleta de colores por país
COLORS = {
    "Argentina": "#61dafb", "Bolivia": "#fbbf24", "Brasil": "#34d399",
    "Chile": "#8b5cf6", "Colombia": "#f87171", "Ecuador": "#fb923c",
    "México": "#a3e635", "Paraguay": "#e879f9", "Perú": "#22d3ee",
    "Uruguay": "#f472b6", "Venezuela": "#facc15"
}

# Esquema de colores UI
BG, PANEL, TEXT, MUTED, GRID = "#06111f", "#0e1a2b", "#eff6ff", "#bfd0e3", "#29405c"

print(f"Generando gráficos para {len(paises)} países...")

# Gráficos individuales por país
for pais in paises:
    datos = df[df["País"] == pais].sort_values("Año")
    
    if datos.empty:
        print(f"  Skip {pais}: sin datos")
        continue
    
    color = COLORS.get(pais, "#61dafb")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)
    
    # Línea principal
    ax.plot(datos["Año"], datos["Pct_65_más"], 
            color=color, linewidth=2.5, marker="o", markersize=7,
            markerfacecolor=color, markeredgecolor=BG, markeredgewidth=1.5)
    
    # Anotaciones de valores
    for _, row in datos.iterrows():
        ax.annotate(f"{row['Pct_65_más']:.1f}%",
                    xy=(row["Año"], row["Pct_65_más"]),
                    xytext=(0, 12), textcoords="offset points",
                    ha="center", color=color, fontsize=8,
                    fontweight='bold')
    
    # Título y etiquetas
    ax.set_title(f"Evolución 65+ — {pais} (2000-2023)", 
                 color=TEXT, fontsize=12, pad=14, fontweight='bold')
    ax.set_xlabel("Año", color=MUTED, fontsize=10)
    ax.set_ylabel("Población 65+ (%)", color=MUTED, fontsize=10)
    
    # Configuración de ejes
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.set_xticks(datos["Año"].unique())
    ax.set_ylim(bottom=0)
    
    # Estilo de bordes y grid
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.grid(color=GRID, linestyle="--", linewidth=0.5, alpha=0.6)
    
    plt.tight_layout()
    
    # Guardar
    name = pais.lower().replace(" ", "_").replace("á", "a").replace("é", "e")\
                       .replace("í", "i").replace("ó", "o").replace("ú", "u")\
                       .replace("ñ", "n")
    output_path = FIGURE_DIR / f"aging_trend_{name}.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"  ✓ {pais}")

# Gráfico comparativo de todos los países
print("Generando gráfico comparativo...")

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)

for pais in paises:
    datos = df[df["País"] == pais].sort_values("Año")
    ax.plot(datos["Año"], datos["Pct_65_más"],
            color=COLORS.get(pais, "#61dafb"),
            linewidth=2.5, marker="o", markersize=5, 
            label=pais, alpha=0.9)

ax.set_title("Evolución Población 65+ — América Latina (2000-2023)",
             color=TEXT, fontsize=14, pad=16, fontweight='bold')
ax.set_xlabel("Año", color=MUTED, fontsize=11)
ax.set_ylabel("Población 65+ (%)", color=MUTED, fontsize=11)
ax.tick_params(colors=MUTED, labelsize=10)
ax.set_xticks(sorted(df["Año"].unique()))
ax.set_ylim(bottom=0)

for spine in ax.spines.values():
    spine.set_color(GRID)
ax.grid(color=GRID, linestyle="--", linewidth=0.5, alpha=0.6)

# Leyenda mejorada
legend = ax.legend(loc="upper left", framealpha=0.9, 
                   labelcolor=TEXT, facecolor=PANEL, 
                   edgecolor=GRID, fontsize=10,
                   ncol=2, title="Países", title_fontsize=11)
legend.get_title().set_color(TEXT)

plt.tight_layout()

output_all = FIGURE_DIR / "aging_trends_all_countries.png"
fig.savefig(output_all, dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()

print(f"\n✓ Completado: {output_all}")
print(f"  Directorio de salida: {FIGURE_DIR}")
print(f"  Total de gráficos generados: {len(paises) + 1}")
