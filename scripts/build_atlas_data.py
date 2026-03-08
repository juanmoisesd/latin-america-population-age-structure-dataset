#!/usr/bin/env python3
from __future__ import annotations

import sys

from common import add_indicators, ensure_dir, parse_args, read_dataset, save_json


def main() -> int:
    parser = parse_args('Genera los archivos consumidos por el atlas interactivo.')
    args = parser.parse_args()

    df = add_indicators(read_dataset(args.input)).sort_values(['País', 'Año']).reset_index(drop=True)
    out_dir = args.docs_dir / 'atlas' / 'data'
    ensure_dir(out_dir)

    records = []
    for _, r in df.iterrows():
        records.append({
            'country': r['País'],
            'iso3': r['ISO3'],
            'region': r['Región'],
            'year': int(r['Año']),
            'population_total_millions': float(r['Población_Total_Millones']),
            'age_groups_pct': {
                '0_14': float(r['Pct_0_14']), '15_24': float(r['Pct_15_24']), '25_54': float(r['Pct_25_54']),
                '55_64': float(r['Pct_55_64']), '65_plus': float(r['Pct_65_más']),
            },
            'age_groups_thousands': {
                '0_14': float(r['Pob_0_14_Miles']), '15_24': float(r['Pob_15_24_Miles']), '25_54': float(r['Pob_25_54_Miles']),
                '55_64': float(r['Pob_55_64_Miles']), '65_plus': float(r['Pob_65_más_Miles']),
            },
            'indicators': {
                'aging_index': None if str(r['Indice_Envejecimiento']) == 'nan' else float(r['Indice_Envejecimiento']),
                'dependency_ratio_total': None if str(r['Razon_Dependencia_Total']) == 'nan' else float(r['Razon_Dependencia_Total']),
                'dependency_ratio_child': None if str(r['Razon_Dependencia_Infantil']) == 'nan' else float(r['Razon_Dependencia_Infantil']),
                'dependency_ratio_older': None if str(r['Razon_Dependencia_Mayores']) == 'nan' else float(r['Razon_Dependencia_Mayores']),
                'demographic_dividend_index': None if str(r['Indice_Bono_Demografico']) == 'nan' else float(r['Indice_Bono_Demografico']),
                'working_age_pct': float(r['Pct_Edad_Laboral']),
                'youth_pct': float(r['Pct_Joven_Total']),
                'working_age_thousands': float(r['Pob_Edad_Laboral_Miles']),
                'dependent_thousands': float(r['Pob_Dependiente_Miles']),
                'aging_change_vs_2000': None if str(r['Cambio_Envejecimiento_vs_2000']) == 'nan' else float(r['Cambio_Envejecimiento_vs_2000']),
            },
            'source': r['Fuente'],
        })

    metadata = {
        'title': 'Atlas Demográfico Interactivo de América Latina',
        'author': 'Juan Moisés de la Serna',
        'record_count': int(len(df)),
        'country_count': int(df['País'].nunique()),
        'year_range': [int(df['Año'].min()), int(df['Año'].max())],
        'variables': list(df.columns),
    }

    save_json(out_dir / 'atlas_data.json', {'metadata': metadata, 'records': records})
    save_json(out_dir / 'atlas_metadata.json', metadata)
    df.to_csv(out_dir / 'atlas_data_with_indicators.csv', index=False, encoding='utf-8-sig')

    print(f'OK: {out_dir / "atlas_data.json"}')
    print(f'OK: {out_dir / "atlas_metadata.json"}')
    print(f'OK: {out_dir / "atlas_data_with_indicators.csv"}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
