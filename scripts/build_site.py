#!/usr/bin/env python3
from __future__ import annotations

import html
import itertools
import sys

from common import add_indicators, ensure_dir, growth_comment, latest_by_country, nav_links, parse_args, read_dataset, slugify


def fmt(value, decimals=2):
    try:
        return f'{float(value):,.{decimals}f}'
    except Exception:
        return ''


def render_page(title: str, description: str, body: str, rel_prefix: str = '') -> str:
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="stylesheet" href="{rel_prefix}assets/atlas.css">
</head>
<body>
<main class="container">
<nav><a href="{rel_prefix}index.html">Inicio</a> · <a href="{rel_prefix}research-questions/top-envejecimiento.html">Preguntas de investigación</a></nav>
{body}
</main>
</body>
</html>'''


def country_comment(sub) -> str:
    first = sub.iloc[0]
    last = sub.iloc[-1]
    msg = growth_comment(last['Indice_Envejecimiento'], first['Indice_Envejecimiento'])
    return (
        f'Entre {int(first["Año"])} y {int(last["Año"])} el índice de envejecimiento en {first["País"]} {msg}. '
        f'En el último corte, la población de 65+ representa {fmt(last["Pct_65_más"])}% y la de 0-14 años {fmt(last["Pct_0_14"])}%.'
    )


def build_country_page(country: str, sub, latest, all_countries) -> str:
    rows = []
    for _, r in sub.iterrows():
        rows.append(
            '<tr>'
            f'<td>{int(r["Año"])}</td>'
            f'<td>{fmt(r["Población_Total_Millones"])}</td>'
            f'<td>{fmt(r["Pct_0_14"])}</td>'
            f'<td>{fmt(r["Pct_15_24"])}</td>'
            f'<td>{fmt(r["Pct_25_54"])}</td>'
            f'<td>{fmt(r["Pct_55_64"])}</td>'
            f'<td>{fmt(r["Pct_65_más"])}</td>'
            f'<td>{fmt(r["Indice_Envejecimiento"])}</td>'
            f'<td>{fmt(r["Razon_Dependencia_Total"])}</td>'
            '</tr>'
        )
    also = [(slugify(c), c) for c in all_countries if c != country][:6]
    body = f'''
<h1>{html.escape(country)}</h1>
<p>{country_comment(sub)}</p>
<div class="summary-grid">
  <div class="card"><strong>ISO3</strong><br>{html.escape(str(latest["ISO3"]))}</div>
  <div class="card"><strong>Región</strong><br>{html.escape(str(latest["Región"]))}</div>
  <div class="card"><strong>Último año</strong><br>{int(latest["Año"])}</div>
  <div class="card"><strong>Población total</strong><br>{fmt(latest["Población_Total_Millones"])} millones</div>
</div>
<table>
<thead><tr><th>Año</th><th>Población total</th><th>% 0-14</th><th>% 15-24</th><th>% 25-54</th><th>% 55-64</th><th>% 65+</th><th>Índice envejecimiento</th><th>Razón dependencia total</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
<section>
<h2>También te puede interesar</h2>
<ul>{nav_links(slugify(country), also, '')}</ul>
</section>
'''
    return render_page(f'{country} | Atlas Demográfico', f'Perfil demográfico de {country}.', body, '../')


def build_compare_page(country_a: str, country_b: str, latest_a, latest_b) -> str:
    body = f'''
<h1>Comparativa: {html.escape(country_a)} vs {html.escape(country_b)}</h1>
<table>
<thead><tr><th>Indicador</th><th>{html.escape(country_a)}</th><th>{html.escape(country_b)}</th></tr></thead>
<tbody>
<tr><td>Último año disponible</td><td>{int(latest_a['Año'])}</td><td>{int(latest_b['Año'])}</td></tr>
<tr><td>Población total (millones)</td><td>{fmt(latest_a['Población_Total_Millones'])}</td><td>{fmt(latest_b['Población_Total_Millones'])}</td></tr>
<tr><td>% 0-14</td><td>{fmt(latest_a['Pct_0_14'])}</td><td>{fmt(latest_b['Pct_0_14'])}</td></tr>
<tr><td>% 65+</td><td>{fmt(latest_a['Pct_65_más'])}</td><td>{fmt(latest_b['Pct_65_más'])}</td></tr>
<tr><td>Índice de envejecimiento</td><td>{fmt(latest_a['Indice_Envejecimiento'])}</td><td>{fmt(latest_b['Indice_Envejecimiento'])}</td></tr>
<tr><td>Razón de dependencia total</td><td>{fmt(latest_a['Razon_Dependencia_Total'])}</td><td>{fmt(latest_b['Razon_Dependencia_Total'])}</td></tr>
<tr><td>Índice de bono demográfico</td><td>{fmt(latest_a['Indice_Bono_Demografico'], 4)}</td><td>{fmt(latest_b['Indice_Bono_Demografico'], 4)}</td></tr>
</tbody>
</table>
'''
    return render_page(f'Comparativa {country_a} vs {country_b}', f'Comparativa demográfica entre {country_a} y {country_b}.', body, '../')


def build_index_page(latest, countries) -> str:
    cards = []
    for _, row in latest.sort_values('Indice_Envejecimiento', ascending=False).head(6).iterrows():
        cards.append(
            f'<div class="card"><strong><a href="countries/{slugify(row["País"])}.html">{html.escape(row["País"])}</a></strong><br>Índice de envejecimiento: {fmt(row["Indice_Envejecimiento"])}<\/div>'
        )
    country_links = ''.join([f'<li><a href="countries/{slugify(c)}.html">{html.escape(c)}</a></li>' for c in countries])
    body = f'''
<h1>Atlas Demográfico Interactivo de América Latina</h1>
<p>Sitio generado automáticamente desde el dataset base. Incluye perfiles por país, comparativas y páginas de investigación.</p>
<div class="summary-grid">{''.join(cards)}</div>
<section>
<h2>Explorar países</h2>
<ul>{country_links}</ul>
</section>
<section>
<h2>Preguntas de investigación</h2>
<ul>
<li><a href="research-questions/top-envejecimiento.html">¿Qué países presentan mayor envejecimiento demográfico?</a></li>
<li><a href="research-questions/bono-demografico.html">¿Dónde persiste con más fuerza el bono demográfico?</a></li>
<li><a href="research-questions/envejecimiento-mas-rapido.html">¿Qué países envejecen más rápido desde 2000?</a></li>
</ul>
</section>
'''
    return render_page('Atlas Demográfico Interactivo de América Latina', 'Atlas demográfico interactivo generado automáticamente.', body)


def main() -> int:
    parser = parse_args('Genera el sitio HTML estático a partir del dataset.')
    args = parser.parse_args()

    docs_dir = args.docs_dir
    countries_dir = docs_dir / 'countries'
    compare_dir = docs_dir / 'compare'
    ensure_dir(countries_dir)
    ensure_dir(compare_dir)

    df = add_indicators(read_dataset(args.input)).sort_values(['País', 'Año']).reset_index(drop=True)
    latest = latest_by_country(df)
    countries = sorted(df['País'].unique().tolist())

    (docs_dir / 'index.html').write_text(build_index_page(latest, countries), encoding='utf-8')

    latest_map = {row['País']: row for _, row in latest.iterrows()}
    for country in countries:
        sub = df[df['País'] == country].copy().sort_values('Año')
        (countries_dir / f'{slugify(country)}.html').write_text(
            build_country_page(country, sub, latest_map[country], countries), encoding='utf-8'
        )

    for country_a, country_b in itertools.combinations(countries, 2):
        (compare_dir / f'{slugify(country_a)}-vs-{slugify(country_b)}.html').write_text(
            build_compare_page(country_a, country_b, latest_map[country_a], latest_map[country_b]),
            encoding='utf-8'
        )

    print(f'OK: {docs_dir / "index.html"}')
    print(f'OK: {countries_dir}')
    print(f'OK: {compare_dir}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
