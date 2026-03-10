#!/usr/bin/env python3
from __future__ import annotations

import sys
from typing import Any

import pandas as pd

from common import add_indicators, ensure_dir, parse_args, read_dataset, save_json


def safe_float(value: Any) -> float | None:
    return None if pd.isna(value) else float(value)


def safe_int(value: Any) -> int | None:
    return None if pd.isna(value) else int(value)


def require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(missing)}")


def main() -> int:
    parser = parse_args("Genera los archivos consumidos por el atlas interactivo.")
    args = parser.parse_args()

    df = read_dataset(args.input).copy()

    # Si existe columna Sexo, nos quedamos solo con TOTAL para evitar duplicados por sexo
    if "Sexo" in df.columns:
        df = df[df["Sexo"].astype(str).str.upper() == "TOTAL"].copy()

    df = add_indicators(df).sort_values(["País", "Año"]).reset_index(drop=True)

    require_columns(
        df,
        [
            "País",
            "Año",
            "Pob_Total_Millones",
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
        ],
    )

    out_dir = args.docs_dir / "atlas" / "data"
    ensure_dir(out_dir)

    records = []
    for _, r in df.iterrows():
        record = {
            "country": r["País"],
            "year": safe_int(r["Año"]),
            "population_total_millions": safe_float(r["Pob_Total_Millones"]),
            "age_groups_pct": {
                "0_14": safe_float(r["Pct_0_14"]),
                "15_24": safe_float(r["Pct_15_24"]),
                "25_54": safe_float(r["Pct_25_54"]),
                "55_64": safe_float(r["Pct_55_64"]),
                "65_plus": safe_float(r["Pct_65_más"]),
            },
            "age_groups_thousands": {
                "0_14": safe_float(r["Pob_0_14_Miles"]),
                "15_24": safe_float(r["Pob_15_24_Miles"]),
                "25_54": safe_float(r["Pob_25_54_Miles"]),
                "55_64": safe_float(r["Pob_55_64_Miles"]),
                "65_plus": safe_float(r["Pob_65_más_Miles"]),
            },
            "indicators": {
                "aging_index": safe_float(r.get("Indice_Envejecimiento")),
                "youth_index": safe_float(r.get("Indice_Juventud")),
                "dependency_ratio_total": safe_float(r.get("Razon_Dependencia_Total")),
                "dependency_ratio_youth": safe_float(r.get("Razon_Dependencia_Juvenil")),
                "dependency_ratio_old_age": safe_float(r.get("Razon_Dependencia_Vejez")),
                "demographic_dividend_index": safe_float(r.get("Indice_Bono_Demografico")),
                "working_age_pct": safe_float(r.get("Pct_Edad_Laboral")),
                "youth_pct": safe_float(r.get("Pct_Joven_Total")),
                "older_pct": safe_float(r.get("Pct_65_más")),
                "working_age_thousands": safe_float(r.get("Pob_Edad_Laboral_Miles")),
                "dependent_thousands": safe_float(r.get("Pob_Dependiente_Miles")),
                "youth_to_older_ratio": safe_float(r.get("Relacion_Jovenes_Mayores")),
                "old_age_ratio": safe_float(r.get("Old_Age_Ratio")),
                "aging_change_vs_2000": safe_float(r.get("Cambio_Envejecimiento_vs_2000")),
                "pct_65_plus_change_vs_2000": safe_float(r.get("Cambio_Pct_65_más_vs_2000")),
                "pct_0_14_change_vs_2000": safe_float(r.get("Cambio_Pct_0_14_vs_2000")),
                "sum_pct_groups": safe_float(r.get("Suma_Pct_Grupos")),
                "pct_groups_valid": (
                    None if pd.isna(r.get("Pct_Grupos_Validos")) else bool(r.get("Pct_Grupos_Validos"))
                ),
            },
            "classification": {
                "aging": r.get("Clasificacion_Envejecimiento"),
                "dependency": r.get("Clasificacion_Dependencia"),
            },
            "source": r["Fuente"],
        }

        if "ISO3" in df.columns:
            record["iso3"] = r["ISO3"]
        if "Región" in df.columns:
            record["region"] = r["Región"]

        records.append(record)

    metadata = {
        "title": "Atlas Demográfico Interactivo de América Latina",
        "author": "Juan Moisés de la Serna",
        "record_count": int(len(df)),
        "country_count": int(df["País"].nunique()),
        "year_range": [int(df["Año"].min()), int(df["Año"].max())],
        "years": sorted(int(y) for y in df["Año"].dropna().unique()),
        "countries": sorted(str(c) for c in df["País"].dropna().unique()),
        "variables": list(df.columns),
        "source_column": "Fuente",
        "dataset_description": (
            "Dataset demográfico comparativo con población total, estructura "
            "por grandes grupos de edad, población por grupos de edad en miles "
            "e indicadores derivados de envejecimiento, dependencia y bono demográfico."
        ),
    }

    save_json(out_dir / "atlas_data.json", {"metadata": metadata, "records": records})
    save_json(out_dir / "atlas_metadata.json", metadata)
    df.to_csv(out_dir / "atlas_data_with_indicators.csv", index=False, encoding="utf-8-sig")

    print(f'OK: {out_dir / "atlas_data.json"}')
    print(f'OK: {out_dir / "atlas_metadata.json"}')
    print(f'OK: {out_dir / "atlas_data_with_indicators.csv"}')
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
