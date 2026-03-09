#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

REQUIRED_COLUMNS = [
    "País",
    "Año",
    "Población_Total_Millones",
    "Pct_0_14",
    "Pct_15_24",
    "Pct_25_54",
    "Pct_55_64",
    "Pct_65_más",
    "Pob_0_14_Miles",
    "Pob_15_24_Miles",
    "Pob_25_54_Miles",
    "Pob_55_64_Miles",
    "Pob_65_más_Miles",
    "Fuente",
]

PCT_COLUMNS = [
    "Pct_0_14",
    "Pct_15_24",
    "Pct_25_54",
    "Pct_55_64",
    "Pct_65_más",
]

ABS_COLUMNS = [
    "Pob_0_14_Miles",
    "Pob_15_24_Miles",
    "Pob_25_54_Miles",
    "Pob_55_64_Miles",
    "Pob_65_más_Miles",
]

NUMERIC_COLUMNS = ["Población_Total_Millones", *PCT_COLUMNS, *ABS_COLUMNS]

ISO3_MAP = {
    "México": "MEX",
    "Brasil": "BRA",
    "Argentina": "ARG",
    "Colombia": "COL",
    "Chile": "CHL",
    "Perú": "PER",
    "Venezuela": "VEN",
    "Ecuador": "ECU",
    "Bolivia": "BOL",
    "Paraguay": "PRY",
    "Uruguay": "URY",
}

REGION_MAP = {
    "México": "Norteamérica",
    "Brasil": "Sudamérica",
    "Argentina": "Sudamérica",
    "Colombia": "Sudamérica",
    "Chile": "Sudamérica",
    "Perú": "Sudamérica",
    "Venezuela": "Sudamérica",
    "Ecuador": "Sudamérica",
    "Bolivia": "Sudamérica",
    "Paraguay": "Sudamérica",
    "Uruguay": "Sudamérica",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_input() -> Path:
    return repo_root() / "data" / "dataset.csv"


def default_docs() -> Path:
    return repo_root() / "docs"


def default_data() -> Path:
    return repo_root() / "data"


def parse_args(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input(),
        help="Ruta al dataset CSV de entrada.",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=default_docs(),
        help="Directorio docs de salida.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=default_data(),
        help="Directorio data de salida.",
    )
    return parser


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text or "item"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el dataset de entrada: {path}")

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {missing}")

    df = df.copy()
    df["País"] = df["País"].astype(str).str.strip()
    df["Fuente"] = df["Fuente"].astype(str).str.strip()
    df["Año"] = pd.to_numeric(df["Año"], errors="raise").astype(int)

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="raise")

    return df


def safe_divide(a: pd.Series, b: pd.Series) -> pd.Series:
    denominator = b.astype("float64").replace({0: pd.NA})
    return (a.astype("float64") / denominator).astype("float64")


def add_dimensions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ISO3"] = df["País"].map(ISO3_MAP).fillna("UNK")
    df["Región"] = df["País"].map(REGION_MAP).fillna("Sin clasificar")
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = add_dimensions(df)
    df = df.copy()

    # Estructura porcentual agregada
    df["Pct_Edad_Laboral"] = (
        df["Pct_15_24"] + df["Pct_25_54"] + df["Pct_55_64"]
    ).round(2)
    df["Pct_Joven_Total"] = (
        df["Pct_0_14"] + df["Pct_15_24"]
    ).round(2)

    # Estructura absoluta agregada
    df["Pob_Edad_Laboral_Miles"] = (
        df["Pob_15_24_Miles"] + df["Pob_25_54_Miles"] + df["Pob_55_64_Miles"]
    ).round(2)
    df["Pob_Dependiente_Miles"] = (
        df["Pob_0_14_Miles"] + df["Pob_65_más_Miles"]
    ).round(2)

    # Indicadores principales
    df["Indice_Envejecimiento"] = (
        safe_divide(df["Pob_65_más_Miles"], df["Pob_0_14_Miles"]) * 100
    ).round(2)

    df["Indice_Juventud"] = (
        safe_divide(df["Pob_0_14_Miles"], df["Pob_65_más_Miles"])
    ).round(2)

    df["Razon_Dependencia_Total"] = (
        safe_divide(df["Pob_Dependiente_Miles"], df["Pob_Edad_Laboral_Miles"]) * 100
    ).round(2)

    df["Razon_Dependencia_Juvenil"] = (
        safe_divide(df["Pob_0_14_Miles"], df["Pob_Edad_Laboral_Miles"]) * 100
    ).round(2)

    df["Razon_Dependencia_Vejez"] = (
        safe_divide(df["Pob_65_más_Miles"], df["Pob_Edad_Laboral_Miles"]) * 100
    ).round(2)

    df["Indice_Bono_Demografico"] = safe_divide(
        df["Pob_Edad_Laboral_Miles"], df["Pob_Dependiente_Miles"]
    ).round(4)

    df["Relacion_Jovenes_Mayores"] = safe_divide(
        df["Pob_0_14_Miles"], df["Pob_65_más_Miles"]
    ).round(2)

    df["Old_Age_Ratio"] = safe_divide(
        df["Pob_65_más_Miles"], df["Pob_Edad_Laboral_Miles"]
    ).round(4)

    # Cambios respecto al primer año disponible por país
    df["Cambio_Envejecimiento_vs_2000"] = (
        df["Indice_Envejecimiento"]
        - df.groupby("País")["Indice_Envejecimiento"].transform("first")
    ).round(2)

    df["Cambio_Pct_65_más_vs_2000"] = (
        df["Pct_65_más"]
        - df.groupby("País")["Pct_65_más"].transform("first")
    ).round(2)

    df["Cambio_Pct_0_14_vs_2000"] = (
        df["Pct_0_14"]
        - df.groupby("País")["Pct_0_14"].transform("first")
    ).round(2)

    # Validaciones internas
    df["Suma_Pct_Grupos"] = df[PCT_COLUMNS].sum(axis=1).round(2)
    df["Pct_Grupos_Validos"] = df["Suma_Pct_Grupos"].between(99.5, 100.5)

    # Clasificaciones útiles para páginas y resúmenes
    df["Clasificacion_Envejecimiento"] = pd.cut(
        df["Pct_65_más"],
        bins=[-float("inf"), 7, 14, float("inf")],
        labels=["joven", "transición", "envejecido"],
    ).astype("object")

    df["Clasificacion_Dependencia"] = pd.cut(
        df["Razon_Dependencia_Total"],
        bins=[-float("inf"), 50, 60, float("inf")],
        labels=["baja", "moderada", "alta"],
    ).astype("object")

    return df


def latest_by_country(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.sort_values(["País", "Año"])
        .groupby("País", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )


def summarize_by_country(df: pd.DataFrame) -> pd.DataFrame:
    latest = latest_by_country(df).copy()

    latest["Ranking_Envejecimiento_Regional"] = (
        latest["Indice_Envejecimiento"].rank(method="min", ascending=False).astype("Int64")
    )

    latest["country_transition_type"] = latest["Clasificacion_Envejecimiento"].map(
        {
            "joven": "estructura relativamente joven",
            "transición": "transición demográfica intermedia",
            "envejecido": "estructura demográfica más envejecida",
        }
    )

    latest["country_priority_type"] = latest["Clasificacion_Dependencia"].map(
        {
            "baja": "una relación demográfica comparativamente favorable",
            "moderada": "una presión demográfica intermedia",
            "alta": "una presión demográfica elevada",
        }
    )

    latest["country_summary_long"] = latest.apply(build_country_summary, axis=1)
    return latest


def summarize_by_year(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("Año", as_index=False)
        .agg(
            Población_Total_Millones=("Población_Total_Millones", "sum"),
            Pct_0_14=("Pct_0_14", "mean"),
            Pct_15_24=("Pct_15_24", "mean"),
            Pct_25_54=("Pct_25_54", "mean"),
            Pct_55_64=("Pct_55_64", "mean"),
            Pct_65_más=("Pct_65_más", "mean"),
            Indice_Envejecimiento=("Indice_Envejecimiento", "mean"),
            Razon_Dependencia_Total=("Razon_Dependencia_Total", "mean"),
            Indice_Bono_Demografico=("Indice_Bono_Demografico", "mean"),
            Pct_Edad_Laboral=("Pct_Edad_Laboral", "mean"),
        )
        .sort_values("Año")
        .reset_index(drop=True)
    )
    return grouped


def growth_comment(current: float, previous: float) -> str:
    diff = round(float(current) - float(previous), 2)
    if math.isclose(diff, 0.0, abs_tol=0.01):
        return "sin cambios relevantes frente al corte anterior"
    if diff > 0:
        return f"aumentó {diff} puntos respecto al corte anterior"
    return f"disminuyó {abs(diff)} puntos respecto al corte anterior"


def build_country_summary(row: pd.Series) -> str:
    country = str(row["País"])
    year = int(row["Año"])
    aging = row.get("Indice_Envejecimiento")
    dep = row.get("Razon_Dependencia_Total")
    old_pct = row.get("Pct_65_más")
    young_pct = row.get("Pct_0_14")
    transition = row.get("country_transition_type", "transición demográfica")
    priority = row.get("country_priority_type", "presión demográfica")

    return (
        f"En {year}, {country} presenta un perfil compatible con {transition}. "
        f"El porcentaje de población de 65 años o más alcanza {old_pct:.2f}%, "
        f"frente a {young_pct:.2f}% en el grupo de 0 a 14 años. "
        f"El índice de envejecimiento se sitúa en {aging:.2f} y la razón de dependencia total en {dep:.2f}. "
        f"En conjunto, el país muestra una situación caracterizada por {priority}."
    )


def save_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def nav_links(current_slug: str, items: Iterable[tuple[str, str]], prefix: str = "") -> str:
    links = []
    for slug, label in items:
        if slug == current_slug:
            continue
        href = f"{prefix}{slug}.html"
        links.append(f'<li><a href="{href}">{label}</a></li>')
    return "\n".join(links[:6])
