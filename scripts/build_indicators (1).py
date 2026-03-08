#!/usr/bin/env python3
"""
build_indicators.py
-------------------
Enriquece el dataset demográfico de América Latina con indicadores derivados,
texto interpretativo básico y campos preparados para SEO, citación y generación
de páginas científicas.

Entradas esperadas:
    data/dataset.csv

Salidas:
    data/dataset_with_indicators.csv
    data/indicators_summary_by_country.csv
    data/indicators_summary_by_year.csv
    data/research_question_catalog.csv
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd

REQUIRED_COLUMNS = [
    "País", "Año", "Población_Total_Millones",
    "Pct_0_14", "Pct_15_24", "Pct_25_54", "Pct_55_64", "Pct_65_más",
    "Pob_0_14_Miles", "Pob_15_24_Miles", "Pob_25_54_Miles", "Pob_55_64_Miles", "Pob_65_más_Miles",
    "Fuente",
]

PCT_COLS = ["Pct_0_14", "Pct_15_24", "Pct_25_54", "Pct_55_64", "Pct_65_más"]
POP_COLS = ["Pob_0_14_Miles", "Pob_15_24_Miles", "Pob_25_54_Miles", "Pob_55_64_Miles", "Pob_65_más_Miles"]


def slugify(text: str) -> str:
    replacements = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    text = text.translate(replacements).lower()
    out = []
    for ch in text:
        out.append(ch if ch.isalnum() else "-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def validate_columns(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {missing}")


def safe_divide(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a / b.replace({0: pd.NA})).astype("float64")


def classify_transition(row: pd.Series) -> str:
    pct_old = float(row["Pct_65_más"])
    pct_young = float(row["Pct_0_14"])
    aging_index = float(row["Indice_Envejecimiento"]) if pd.notna(row["Indice_Envejecimiento"]) else math.nan

    if pct_old >= 12 or aging_index >= 60:
        return "envejecimiento avanzado"
    if pct_old >= 8 or aging_index >= 35:
        return "transición demográfica intermedia"
    return "estructura relativamente joven"


def classify_priority(row: pd.Series) -> str:
    if row["Razon_Dependencia_Total"] >= 60:
        return "alta presión demográfica"
    if row["Razon_Dependencia_Total"] >= 50:
        return "presión demográfica moderada"
    return "ventana demográfica relativamente favorable"


def narrative_change(start: float, end: float, higher_text: str, lower_text: str, neutral_text: str) -> str:
    diff = round(end - start, 2)
    if diff > 0.2:
        return higher_text.format(diff=diff, end=end, start=start)
    if diff < -0.2:
        return lower_text.format(diff=abs(diff), end=end, start=start)
    return neutral_text.format(diff=diff, end=end, start=start)


def build_country_snapshot(sub: pd.DataFrame) -> Dict[str, str]:
    sub = sub.sort_values("Año")
    first = sub.iloc[0]
    last = sub.iloc[-1]

    old_comment = narrative_change(
        float(first["Pct_65_más"]),
        float(last["Pct_65_más"]),
        "La población de 65 años o más aumentó {diff} puntos porcentuales entre {start}% y {end}%.",
        "La población de 65 años o más descendió {diff} puntos porcentuales entre {start}% y {end}%.",
        "La proporción de población de 65 años o más se mantuvo relativamente estable.",
    )
    young_comment = narrative_change(
        float(first["Pct_0_14"]),
        float(last["Pct_0_14"]),
        "La población de 0 a 14 años aumentó {diff} puntos porcentuales, lo que sugiere un mayor peso relativo de la infancia.",
        "La población de 0 a 14 años disminuyó {diff} puntos porcentuales, un patrón compatible con la caída de la fecundidad.",
        "La proporción de población de 0 a 14 años apenas cambió en el periodo analizado.",
    )
    work_comment = narrative_change(
        float(first["Pct_Edad_Laboral"]),
        float(last["Pct_Edad_Laboral"]),
        "La población en edad potencialmente activa aumentó {diff} puntos porcentuales.",
        "La población en edad potencialmente activa disminuyó {diff} puntos porcentuales.",
        "La población en edad potencialmente activa se mantuvo prácticamente estable.",
    )

    return {
        "country_slug": slugify(str(last["País"])),
        "country_transition_type": classify_transition(last),
        "country_priority_type": classify_priority(last),
        "country_summary_short": (
            f"{last['País']} presenta en {int(last['Año'])} una {classify_transition(last)} "
            f"y una {classify_priority(last)}."
        ),
        "country_summary_long": (
            f"Entre {int(first['Año'])} y {int(last['Año'])}, {last['País']} mostró un cambio en su estructura por edades. "
            f"{old_comment} {young_comment} {work_comment} "
            f"El índice de envejecimiento pasó de {round(float(first['Indice_Envejecimiento']), 2)} a "
            f"{round(float(last['Indice_Envejecimiento']), 2)}, mientras que la razón de dependencia total se situó en "
            f"{round(float(last['Razon_Dependencia_Total']), 2)} en el último año disponible."
        ),
    }


def build_question_catalog(country_summary: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, str]] = []

    for _, row in country_summary.iterrows():
        country = row["País"]
        slug = slugify(country)
        rows.append({
            "question_slug": f"como-cambio-la-estructura-por-edades-en-{slug}-entre-2000-y-2023",
            "page_type": "country_change",
            "country_a": country,
            "country_b": "",
            "question_title": f"¿Cómo cambió la estructura por edades en {country} entre 2000 y 2023?",
            "meta_title": f"{country}: estructura por edades 2000-2023 | análisis demográfico y científico",
            "meta_description": (
                f"Análisis demográfico de {country} entre 2000 y 2023 con resultados, contexto científico, "
                f"referencias bibliográficas, indicadores de envejecimiento y notas metodológicas."
            ),
            "primary_keyword": f"estructura por edades {country}",
            "secondary_keywords": (
                f"envejecimiento poblacional {country}; transición demográfica {country}; "
                f"pirámide poblacional {country}; índice de envejecimiento {country}"
            ),
        })

    return pd.DataFrame(rows)


def main() -> int:
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    input_file = data_dir / "dataset.csv"

    if not input_file.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {input_file}")

    df = pd.read_csv(input_file)
    validate_columns(df)

    df["Año"] = pd.to_numeric(df["Año"], errors="raise").astype(int)
    for col in PCT_COLS + POP_COLS + ["Población_Total_Millones"]:
        df[col] = pd.to_numeric(df[col], errors="raise")

    df["Country_Slug"] = df["País"].map(slugify)
    df["Pct_Edad_Laboral"] = (df["Pct_15_24"] + df["Pct_25_54"] + df["Pct_55_64"]).round(2)
    df["Pct_Joven_Total"] = (df["Pct_0_14"] + df["Pct_15_24"]).round(2)
    df["Pob_Edad_Laboral_Miles"] = (df["Pob_15_24_Miles"] + df["Pob_25_54_Miles"] + df["Pob_55_64_Miles"]).round(2)
    df["Pob_Dependiente_Miles"] = (df["Pob_0_14_Miles"] + df["Pob_65_más_Miles"]).round(2)

    df["Indice_Envejecimiento"] = (safe_divide(df["Pob_65_más_Miles"], df["Pob_0_14_Miles"]) * 100).round(2)
    df["Razon_Dependencia_Total"] = (safe_divide(df["Pob_Dependiente_Miles"], df["Pob_Edad_Laboral_Miles"]) * 100).round(2)
    df["Razon_Dependencia_Mayores"] = (safe_divide(df["Pob_65_más_Miles"], df["Pob_Edad_Laboral_Miles"]) * 100).round(2)
    df["Razon_Dependencia_Infantil"] = (safe_divide(df["Pob_0_14_Miles"], df["Pob_Edad_Laboral_Miles"]) * 100).round(2)
    df["Indice_Bono_Demografico"] = safe_divide(df["Pob_Edad_Laboral_Miles"], df["Pob_Dependiente_Miles"]).round(4)

    df["Suma_Pct_Grupos"] = df[PCT_COLS].sum(axis=1).round(2)
    df["Pct_Grupos_Validos"] = df["Suma_Pct_Grupos"].between(99.5, 100.5)

    # Cambios intertemporales por país
    df = df.sort_values(["País", "Año"]).copy()
    df["Cambio_Pct_65_más"] = df.groupby("País")["Pct_65_más"].diff().round(2)
    df["Cambio_Pct_0_14"] = df.groupby("País")["Pct_0_14"].diff().round(2)
    df["Cambio_Indice_Envejecimiento"] = df.groupby("País")["Indice_Envejecimiento"].diff().round(2)

    country_last = df.groupby("País", as_index=False).tail(1).copy()
    country_last["Ranking_Envejecimiento_Regional"] = country_last["Indice_Envejecimiento"].rank(method="min", ascending=False).astype(int)
    country_last["Ranking_Dependencia_Regional"] = country_last["Razon_Dependencia_Total"].rank(method="min", ascending=False).astype(int)
    country_last["Ranking_Juventud_Regional"] = country_last["Pct_0_14"].rank(method="min", ascending=False).astype(int)

    snapshots = []
    for country, sub in df.groupby("País"):
        snap = build_country_snapshot(sub)
        snapshots.append({"País": country, **snap})
    snapshot_df = pd.DataFrame(snapshots)

    country_last = country_last.merge(snapshot_df, on="País", how="left")

    year_summary = (
        df.groupby("Año", as_index=False)[
            ["Indice_Envejecimiento", "Razon_Dependencia_Total", "Indice_Bono_Demografico", "Pct_65_más", "Pct_0_14"]
        ]
        .mean(numeric_only=True)
        .round(2)
        .sort_values("Año")
    )

    country_summary = country_last[[
        "País", "Country_Slug", "Año", "Población_Total_Millones", "Pct_0_14", "Pct_65_más",
        "Indice_Envejecimiento", "Razon_Dependencia_Total", "Indice_Bono_Demografico",
        "Ranking_Envejecimiento_Regional", "Ranking_Dependencia_Regional", "Ranking_Juventud_Regional",
        "country_transition_type", "country_priority_type", "country_summary_short", "country_summary_long",
    ]].sort_values("Indice_Envejecimiento", ascending=False)

    question_catalog = build_question_catalog(country_summary)

    out_main = data_dir / "dataset_with_indicators.csv"
    out_country = data_dir / "indicators_summary_by_country.csv"
    out_year = data_dir / "indicators_summary_by_year.csv"
    out_questions = data_dir / "research_question_catalog.csv"

    df.to_csv(out_main, index=False, encoding="utf-8-sig")
    country_summary.to_csv(out_country, index=False, encoding="utf-8-sig")
    year_summary.to_csv(out_year, index=False, encoding="utf-8-sig")
    question_catalog.to_csv(out_questions, index=False, encoding="utf-8-sig")

    print(f"OK: {out_main}")
    print(f"OK: {out_country}")
    print(f"OK: {out_year}")
    print(f"OK: {out_questions}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
