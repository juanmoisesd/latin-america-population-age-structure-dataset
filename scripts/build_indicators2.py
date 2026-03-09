#!/usr/bin/env python3
from __future__ import annotations

import sys

from common import add_indicators, ensure_dir, latest_by_country, parse_args, read_dataset


def main() -> int:
    parser = parse_args('Calcula indicadores demográficos derivados y resúmenes.')
    args = parser.parse_args()

    df = add_indicators(read_dataset(args.input))
    ensure_dir(args.data_dir)

    out_main = args.data_dir / 'dataset_with_indicators.csv'
    out_country = args.data_dir / 'indicators_summary_by_country.csv'
    out_year = args.data_dir / 'indicators_summary_by_year.csv'
    out_latest = args.data_dir / 'latest_snapshot.csv'

    df.sort_values(['País', 'Año']).to_csv(out_main, index=False, encoding='utf-8-sig')

    df.groupby('País', as_index=False)[[
        'Indice_Envejecimiento', 'Razon_Dependencia_Total', 'Razon_Dependencia_Juvenil',
        'Razon_Dependencia_Vejez', 'Indice_Bono_Demografico'
    ]].mean(numeric_only=True).round(2).sort_values('Indice_Envejecimiento', ascending=False).to_csv(
        out_country, index=False, encoding='utf-8-sig'
    )

    df.groupby('Año', as_index=False)[[
        'Indice_Envejecimiento', 'Razon_Dependencia_Total', 'Razon_Dependencia_Juvenil',
        'Razon_Dependencia_Vejez', 'Indice_Bono_Demografico'
    ]].mean(numeric_only=True).round(2).sort_values('Año').to_csv(
        out_year, index=False, encoding='utf-8-sig'
    )

    latest_by_country(df).sort_values('Indice_Envejecimiento', ascending=False).to_csv(
        out_latest, index=False, encoding='utf-8-sig'
    )

    print(f'OK: {out_main}')
    print(f'OK: {out_country}')
    print(f'OK: {out_year}')
    print(f'OK: {out_latest}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
