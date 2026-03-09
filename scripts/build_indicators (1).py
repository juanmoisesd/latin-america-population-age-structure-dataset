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


def main() -> int:
    parser = parse_args("Genera los archivos consumidos por el atlas interactivo.")
    args = parser.parse_args()

    df = (
        add_indicators(read_dataset(args.input))
        .sort_values(["País", "Año"])
        .reset_index(drop=True)
    )

    out_dir = args.docs_dir / "atlas" / "data"
    ensure_dir(out_dir)

    records = []
    for _, r in df.iterrows():
        record = {
            "country": r["País"],
            "year": int(r["Año"]),
            "population_total_millions": safe_float(r["Población_Total_Millones"]),
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
                "aging_change_vs_2000": safe_float(r.get("Cambio_Envejecimiento_vs_2000")),
            },
            "source": r["Fuente"],
        }

        # Solo incluir estas claves si existen en el dataset procesado
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
            "por grupos de edad en porcentaje y población por grupos de edad "
            "en miles."
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
