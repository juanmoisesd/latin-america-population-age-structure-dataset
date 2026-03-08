#!/usr/bin/env python3
from __future__ import annotations

import sys

from common import ABS_COLUMNS, NUMERIC_COLUMNS, PCT_COLUMNS, parse_args, read_dataset


def main() -> int:
    parser = parse_args('Valida estructura, tipos y coherencia básica del dataset.')
    args = parser.parse_args()

    df = read_dataset(args.input)
    issues: list[str] = []

    duplicated = df[df.duplicated(subset=['País', 'Año'], keep=False)][['País', 'Año']]
    if not duplicated.empty:
        issues.append('Duplicados por País-Año:\n' + duplicated.to_string(index=False))

    invalid_pct_sum = df.loc[~df[PCT_COLUMNS].sum(axis=1).round(2).between(99.5, 100.5), ['País', 'Año', *PCT_COLUMNS]]
    if not invalid_pct_sum.empty:
        issues.append('Filas donde los porcentajes no suman aproximadamente 100:\n' + invalid_pct_sum.to_string(index=False))

    for col in NUMERIC_COLUMNS:
        negative = df.loc[df[col] < 0, ['País', 'Año', col]]
        if not negative.empty:
            issues.append(f'Valores negativos en {col}:\n' + negative.to_string(index=False))

    total_thousands = df[ABS_COLUMNS].sum(axis=1)
    implied_millions = (total_thousands / 1000).round(2)
    population_gap = (df['Población_Total_Millones'].round(2) - implied_millions).abs()
    mismatch = df.loc[population_gap > 0.2, ['País', 'Año', 'Población_Total_Millones']].copy()
    if not mismatch.empty:
        mismatch['Población_Implícita_Millones'] = implied_millions[population_gap > 0.2].values
        mismatch['Diferencia'] = population_gap[population_gap > 0.2].values
        issues.append('Desajuste entre población total y suma de grupos absolutos:\n' + mismatch.to_string(index=False))

    print(f'Registros: {len(df)}')
    print(f'Países: {df["País"].nunique()}')
    print(f'Años: {sorted(df["Año"].unique().tolist())}')
    print(f'Columnas: {len(df.columns)}')

    if issues:
        print('\nVALIDACIÓN CON OBSERVACIONES\n')
        print('\n\n'.join(issues))
        return 1

    print('\nVALIDACIÓN OK: dataset coherente a nivel estructural y aritmético.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
