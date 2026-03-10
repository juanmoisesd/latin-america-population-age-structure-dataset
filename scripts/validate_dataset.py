#!/usr/bin/env python3
from __future__ import annotations

import sys

from common import (
    RAW_ABS_COLUMNS,
    RAW_NUMERIC_COLUMNS,
    RAW_PCT_COLUMNS,
    parse_args,
    read_dataset,
)


def main() -> int:
    parser = parse_args("Valida estructura, tipos y coherencia básica del dataset.")
    args = parser.parse_args()

    df = read_dataset(args.input)
    issues: list[str] = []

    # Duplicados: ahora la clave correcta incluye Sexo
    duplicated = df[df.duplicated(subset=["País", "Año", "Sexo"], keep=False)][["País", "Año", "Sexo"]]
    if not duplicated.empty:
        issues.append("Duplicados por País-Año-Sexo:\n" + duplicated.to_string(index=False))

    # La suma de porcentajes debe aproximarse a 100 usando los tramos quinquenales
    invalid_pct_sum = df.loc[
        ~df[RAW_PCT_COLUMNS].sum(axis=1).round(2).between(99.5, 100.5),
        ["País", "Año", "Sexo", *RAW_PCT_COLUMNS],
    ]
    if not invalid_pct_sum.empty:
        issues.append(
            "Filas donde los porcentajes quinquenales no suman aproximadamente 100:\n"
            + invalid_pct_sum.to_string(index=False)
        )

    # Valores negativos
    for col in RAW_NUMERIC_COLUMNS:
        negative = df.loc[df[col] < 0, ["País", "Año", "Sexo", col]]
        if not negative.empty:
            issues.append(f"Valores negativos en {col}:\n" + negative.to_string(index=False))

    # Coherencia entre población total y suma de grupos absolutos
    total_thousands = df[RAW_ABS_COLUMNS].sum(axis=1)
    implied_millions = (total_thousands / 1000).round(2)
    population_gap = (df["Pob_Total_Millones"].round(2) - implied_millions).abs()

    mismatch = df.loc[
        population_gap > 0.2,
        ["País", "Año", "Sexo", "Pob_Total_Millones"],
    ].copy()

    if not mismatch.empty:
        mismatch["Población_Implícita_Millones"] = implied_millions[population_gap > 0.2].values
        mismatch["Diferencia"] = population_gap[population_gap > 0.2].values
        issues.append(
            "Desajuste entre población total y suma de grupos absolutos:\n"
            + mismatch.to_string(index=False)
        )

    print(f"Registros: {len(df)}")
    print(f"Países: {df['País'].nunique()}")
    print(f"Años: {sorted(df['Año'].unique().tolist())}")
    print(f"Sexos: {sorted(df['Sexo'].astype(str).unique().tolist())}")
    print(f"Columnas: {len(df.columns)}")

    if issues:
        print("\nVALIDACIÓN CON OBSERVACIONES\n")
        print("\n\n".join(issues))
        return 1

    print("\nVALIDACIÓN OK: dataset coherente a nivel estructural y aritmético.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
