#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS = [
    'País', 'Año', 'Población_Total_Millones',
    'Pct_0_14', 'Pct_15_24', 'Pct_25_54', 'Pct_55_64', 'Pct_65_más',
    'Pob_0_14_Miles', 'Pob_15_24_Miles', 'Pob_25_54_Miles', 'Pob_55_64_Miles', 'Pob_65_más_Miles',
    'Fuente',
]

PCT_COLUMNS = ['Pct_0_14', 'Pct_15_24', 'Pct_25_54', 'Pct_55_64', 'Pct_65_más']
ABS_COLUMNS = ['Pob_0_14_Miles', 'Pob_15_24_Miles', 'Pob_25_54_Miles', 'Pob_55_64_Miles', 'Pob_65_más_Miles']
NUMERIC_COLUMNS = ['Población_Total_Millones', *PCT_COLUMNS, *ABS_COLUMNS]

ISO3_MAP = {
    'México': 'MEX', 'Brasil': 'BRA', 'Argentina': 'ARG', 'Colombia': 'COL',
    'Chile': 'CHL', 'Perú': 'PER', 'Venezuela': 'VEN', 'Ecuador': 'ECU',
    'Bolivia': 'BOL', 'Paraguay': 'PRY', 'Uruguay': 'URY',
}

REGION_MAP = {
    'México': 'Norteamérica',
    'Brasil': 'Cono Sur',
    'Argentina': 'Cono Sur',
    'Colombia': 'Andina',
    'Chile': 'Cono Sur',
    'Perú': 'Andina',
    'Venezuela': 'Andina',
    'Ecuador': 'Andina',
    'Bolivia': 'Andina',
    'Paraguay': 'Cono Sur',
    'Uruguay': 'Cono Sur',
}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_input() -> Path:
    return repo_root() / 'data' / 'dataset.csv'


def default_docs() -> Path:
    return repo_root() / 'docs'


def default_data() -> Path:
    return repo_root() / 'data'


def parse_args(description: str):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', type=Path, default=default_input(), help='Ruta al dataset CSV de entrada.')
    parser.add_argument('--docs-dir', type=Path, default=default_docs(), help='Directorio docs de salida.')
    parser.add_argument('--data-dir', type=Path, default=default_data(), help='Directorio data de salida.')
    return parser


def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')
    return text or 'item'


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f'No existe el dataset de entrada: {path}')
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f'Faltan columnas obligatorias: {missing}')

    df = df.copy()
    df['País'] = df['País'].astype(str).str.strip()
    df['Fuente'] = df['Fuente'].astype(str).str.strip()
    df['Año'] = pd.to_numeric(df['Año'], errors='raise').astype(int)
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors='raise')
    return df


def safe_divide(a, b):
    b = b.replace({0: pd.NA})
    return (a / b).astype('float64')


def add_dimensions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['ISO3'] = df['País'].map(ISO3_MAP).fillna('UNK')
    df['Región'] = df['País'].map(REGION_MAP).fillna('Sin clasificar')
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = add_dimensions(df)
    df = df.copy()

    df['Pct_Edad_Laboral'] = (df['Pct_15_24'] + df['Pct_25_54'] + df['Pct_55_64']).round(2)
    df['Pct_Joven_Total'] = (df['Pct_0_14'] + df['Pct_15_24']).round(2)
    df['Pob_Edad_Laboral_Miles'] = (df['Pob_15_24_Miles'] + df['Pob_25_54_Miles'] + df['Pob_55_64_Miles']).round(2)
    df['Pob_Dependiente_Miles'] = (df['Pob_0_14_Miles'] + df['Pob_65_más_Miles']).round(2)
    df['Indice_Envejecimiento'] = (safe_divide(df['Pob_65_más_Miles'], df['Pob_0_14_Miles']) * 100).round(2)
    df['Razon_Dependencia_Total'] = (safe_divide(df['Pob_Dependiente_Miles'], df['Pob_Edad_Laboral_Miles']) * 100).round(2)
    df['Razon_Dependencia_Infantil'] = (safe_divide(df['Pob_0_14_Miles'], df['Pob_Edad_Laboral_Miles']) * 100).round(2)
    df['Razon_Dependencia_Mayores'] = (safe_divide(df['Pob_65_más_Miles'], df['Pob_Edad_Laboral_Miles']) * 100).round(2)
    df['Indice_Bono_Demografico'] = safe_divide(df['Pob_Edad_Laboral_Miles'], df['Pob_Dependiente_Miles']).round(4)
    df['Cambio_Envejecimiento_vs_2000'] = (
        df['Indice_Envejecimiento'] - df.groupby('País')['Indice_Envejecimiento'].transform('first')
    ).round(2)
    df['Suma_Pct_Grupos'] = df[PCT_COLUMNS].sum(axis=1).round(2)
    df['Pct_Grupos_Validos'] = df['Suma_Pct_Grupos'].between(99.5, 100.5)
    return df


def latest_by_country(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(['País', 'Año']).groupby('País', as_index=False).tail(1).reset_index(drop=True)


def growth_comment(current: float, previous: float) -> str:
    diff = round(current - previous, 2)
    if math.isclose(diff, 0.0, abs_tol=0.01):
        return 'sin cambios relevantes frente al corte anterior'
    if diff > 0:
        return f'aumentó {diff} puntos respecto al corte anterior'
    return f'disminuyó {abs(diff)} puntos respecto al corte anterior'


def save_json(path: Path, payload) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def nav_links(current_slug: str, items: Iterable[tuple[str, str]], prefix: str = '') -> str:
    links = []
    for slug, label in items:
        if slug == current_slug:
            continue
        href = f'{prefix}{slug}.html'
        links.append(f'<li><a href="{href}">{label}</a></li>')
    return '\n'.join(links[:6])
