#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

import pandas as pd

from common import add_indicators, ensure_dir, parse_args, read_dataset, save_json


COLUMN_ALIASES = {
    # Español -> estándar interno
    "País": "country",
    "Pais": "country",
    "Año": "year",
    "Ano": "year",
    "Población_Total_Millones": "population_total_millions",
    "Poblacion_Total_Millones": "population_total_millions",
    "Pct_0_14": "pct_0_14",
    "Pct_15_24": "pct_15_24",
    "Pct_25_54": "pct_25_54",
    "Pct_55_64": "pct_55_64",
    "Pct_65_más": "pct_65_plus",
    "Pct_65_mas": "pct_65_plus",
    "Pob_0_14_Miles": "pop_0_14_thousands",
    "Pob_15_24_Miles": "pop_15_24_thousands",
    "Pob_25_54_Miles": "pop_25_54_thousands",
    "Pob_55_64_Miles": "pop_55_64_thousands",
    "Pob_65_Miles": "pop_65_plus_thousands",
    "Pob_65_más_Miles": "pop_65_plus_thousands",
    "Pob_65_mas_Miles": "pop_65_plus_thousands",
    "Fuente": "source",
    # Inglés -> estándar interno
    "Country": "country",
    "Year": "year",
    "Population_Total_Millions": "population_total_millions",
    "Pct_65_plus": "pct_65_plus",
    "Pop_0_14": "pop_0_14_thousands",
    "Pop_15_24": "pop_15_24_thousands",
    "Pop_25_54": "pop_25_54_thousands",
    "Pop_55_64": "pop_55_64_thousands",
    "Pop_65_plus": "pop_65_plus_thousands",
    "Source": "source",
}

REQUIRED_COLUMNS = [
    "country",
    "year",
    "population_total_millions",
    "pct_0_14",
    "pct_15_24",
    "pct_25_54",
    "pct_55_64",
    "pct_65_plus",
    "pop_0_14_thousands",
    "pop_15_24_thousands",
    "pop_25_54_thousands",
    "pop_55_64_thousands",
    "pop_65_plus_thousands",
    "source",
]


def safe_float(value: Any) -> float | None:
    return None if pd.isna(value) else float(value)


def safe_int(value: Any) -> int | None:
    return None if pd.isna(value) else int(value)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = df.rename(columns={c: COLUMN_ALIASES.get(c, c) for c in df.columns})

    missing = [col for col in REQUIRED_COLUMNS if col not in renamed.columns]
    if missing:
        raise KeyError(
            "Faltan columnas requeridas tras normalizar el dataset: "
            + ", ".join(missing)
            + "\nColumnas detectadas: "
            + ", ".join(map(str, df.columns))
        )

    return renamed


def build_record(row: pd.Series) -> dict[str, Any]:
    record = {
        "country": row["country"],
        "year": safe_int(row["year"]),
        "population_total_millions": safe_float(row["population_total_millions"]),
        "pct_0_14": safe_float(row["pct_0_14"]),
        "pct_15_24": safe_float(row["pct_15_24"]),
        "pct_25_54": safe_float(row["pct_25_54"]),
        "pct_55_64": safe_float(row["pct_55_64"]),
        "pct_65_plus": safe_float(row["pct_65_plus"]),
        "pop_0_14_thousands": safe_float(row["pop_0_14_thousands"]),
        "pop_15_24_thousands": safe_float(row["pop_15_24_thousands"]),
        "pop_25_54_thousands": safe_float(row["pop_25_54_thousands"]),
        "pop_55_64_thousands": safe_float(row["pop_55_64_thousands"]),
        "pop_65_plus_thousands": safe_float(row["pop_65_plus_thousands"]),
        "source": row["source"],
    }

    # Indicadores derivados, solo si existen tras add_indicators()
    optional_fields = [
        "aging_index",
        "old_age_dependency_ratio",
        "youth_dependency_ratio",
        "total_dependency_ratio",
        "demographic_bonus_proxy",
        "working_age_share",
        "median_age_proxy",
    ]
    for field in optional_fields:
        if field in row.index:
            record[field] = safe_float(row[field])

    return record


def main() -> int:
    parser = parse_args("Genera los archivos consumidos por el atlas interactivo.")
    args = parser.parse_args()

    raw_df = read_dataset(args.input)
    df = normalize_columns(raw_df)
    df = add_indicators(df).sort_values(["country", "year"]).reset_index(drop=True)

    out_dir = args.docs_dir / "atlas" / "data"
    ensure_dir(out_dir)

    records = [build_record(row) for _, row in df.iterrows()]

    # JSON principal para el atlas
    save_json(out_dir / "atlas_data.json", records)

    # CSV auxiliar normalizado para depuración / consumo alternativo
    csv_columns = REQUIRED_COLUMNS + [
        c
        for c in [
            "aging_index",
            "old_age_dependency_ratio",
            "youth_dependency_ratio",
            "total_dependency_ratio",
            "demographic_bonus_proxy",
            "working_age_share",
            "median_age_proxy",
        ]
        if c in df.columns
    ]
    df[csv_columns].to_csv(out_dir / "atlas_indicators.csv", index=False, encoding="utf-8")

    # JSON de metadatos útil para la interfaz
    metadata = {
        "countries": sorted(df["country"].dropna().unique().tolist()),
        "years": sorted(int(y) for y in df["year"].dropna().unique().tolist()),
        "row_count": int(len(df)),
        "columns": csv_columns,
    }
    save_json(out_dir / "atlas_metadata.json", metadata)

    print(f"OK: atlas_data.json generado en {out_dir}")
    print(f"OK: atlas_indicators.csv generado en {out_dir}")
    print(f"OK: atlas_metadata.json generado en {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
