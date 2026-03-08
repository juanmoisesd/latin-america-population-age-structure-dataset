#!/usr/bin/env python3
from __future__ import annotations

import html
import itertools
import json
import sys
from pathlib import Path

from common import (
    add_indicators, ensure_dir, growth_comment,
    latest_by_country, parse_args, read_dataset, slugify,
)

BASE_URL = "https://juanmoisesd.github.io/latin-america-population-age-structure-dataset"
AUTHOR = "Juan Moisés de la Serna"
ZENODO_DOI = "https://doi.org/10.5281/zenodo.18891177"
ZENODO_RECORD = "https://zenodo.org/records/18891177"
OSF_DOI = "https://doi.org/10.17605/OSF.IO/3WAEU"
ORCID = "https://orcid.org/0000-0002-8401-8018"
RESEARCHGATE = "https://www.researchgate.net/profile/Juan_Moises_De_La_Serna"
AUTHOR_URL = "https://juanmoisesdelaserna.es/"
CITATION_YEAR = "2026"
CITATION_TITLE = "Evolución Poblacional por Grupos de Edad en América Latina (2000–2023): Dataset Demográfico por País"


def fmt(value, decimals=2):
    try:
        v = float(value)
        if decimals == 0 or v == int(v):
            return f'{int(v):,}'.replace(',', '.')
        return f'{v:,.{decimals}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
        return ''


def ld_json(title: str, description: str, page_url: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": title,
        "description": description,
        "creator": {
            "@type": "Person",
            "name": AUTHOR,
            "url": AUTHOR_URL,
            "sameAs": [ORCID, RESEARCHGATE],
        },
        "url": page_url,
        "identifier": [ZENODO_DOI, OSF_DOI],
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }
    return json.dumps(data, ensure_ascii=False)


def nav(css_prefix: str = '../') -> str:
    return f"""<nav class="navlinks">
 <a href="{css_prefix}index.html">Inicio</a>
 <a href="{css_prefix}pages/countries.html">Países</a>
 <a href="{css_prefix}pages/years.html">Años</a>
 <a href="{css_prefix}pages/indicators.html">Indicadores</a>
 <a href="{css_prefix}pages/comparisons.html">Comparaciones</a>
 <a href="{css_prefix}pages/research-questions/index.html">Preguntas de investigación</a>
 <a href="{css_prefix}pages/about.html">Acerca del dataset</a>
 <a href="{ZENODO_RECORD}">Zenodo</a>
</nav>"""


def footer() -> str:
    return f"""<div class="footer">
 <p><strong>Autor:</strong> <a href="{AUTHOR_URL}">{AUTHOR}</a> · <a href="{ORCID}">ORCID</a> · <a href="{RESEARCHGATE}">ResearchGate</a></p>
 <p><strong>Repositorios:</strong> <a href="{ZENODO_DOI}">Zenodo DOI</a> · <a href="{ZENODO_RECORD}">Zenodo registro</a> · <a href="{OSF_DOI}">OSF DOI</a></p>
 <p><strong>Cómo citar:</strong> de la Serna, J. M. ({CITATION_YEAR}). <em>{CITATION_TITLE}</em>. Zenodo. <a href="{ZENODO_DOI}">{ZENODO_DOI}</a></p>
</div>"""


def render_page(title: str, description: str, body: str,
                page_url: str, css_prefix: str = '../') -> str:
    return f"""<!doctype html>
<html lang="es"><head>
 <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
 <title>{html.escape(title)}</title>
 <meta name="description" content="{html.escape(description)}">
 <link rel="canonical" href="{page_url}">
 <link rel="stylesheet" href="{css_prefix}assets/style.css"><script defer src="{css_prefix}assets/app.js"></script>
 <script type="application/ld+json">{ld_json(title, description, page_url)}</script>
</head><body><div class="wrap">
{nav(css_prefix)}
{body}
{footer()}
</div></body></html>"""


def line_chart(series: list[tuple], color: str = '#61dafb', h: int = 260) -> str:
    """Generate inline SVG line chart from list of (label, value) tuples."""
    if not series:
        return ''
    values = [v for _, v in series]
    lo, hi = min(values), max(values)
    rng = hi - lo if hi != lo else 1
    W, H = 760, h
    pad_x, pad_y, pad_b = 36, 36, 26
    n = len(series)
    xs = [pad_x + i * (W - 2 * pad_x) / max(n - 1, 1) for i in range(n)]
    ys = [H - pad_b - pad_y - (v - lo) / rng * (H - pad_b - 2 * pad_y) for _, v in series]
    mid_y = H - pad_b - pad_y - 0.5 * (H - pad_b - 2 * pad_y)
    lines = (
        f'<line x1="{pad_x}" y1="{pad_y}" x2="{W-pad_x}" y2="{pad_y}" stroke="#20344c" stroke-width="1"/>'
        f'<line x1="{pad_x}" y1="{mid_y}" x2="{W-pad_x}" y2="{mid_y}" stroke="#20344c" stroke-width="1"/>'
        f'<line x1="{pad_x}" y1="{H-pad_b}" x2="{W-pad_x}" y2="{H-pad_b}" stroke="#20344c" stroke-width="1"/>'
    )
    pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in zip(xs, ys))
    polyline = f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{pts}"/>'
    circles = ''
    for (label, val), x, y in zip(series, xs, ys):
        v_str = fmt(val)
        circles += (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>'
            f'<text x="{x:.1f}" y="{y-10:.1f}" fill="#dbeafe" text-anchor="middle" font-size="11">{v_str}</text>'
            f'<text x="{x:.1f}" y="{H-pad_b+16}" fill="#a9bdd3" text-anchor="middle" font-size="11">{label}</text>'
        )
    return f'<svg class="chart" viewBox="0 0 {W} {H}">{lines}{polyline}{circles}</svg>'


def bar_chart(items: list[tuple], color: str = '#61dafb', h: int = 280) -> str:
    """Generate inline SVG bar chart from list of (label, value) tuples."""
    if not items:
        return ''
    values = [v for _, v in items]
    lo, hi = 0, max(values)
    rng = hi - lo if hi != lo else 1
    W, H = 760, h
    pad_x, pad_y, pad_b = 36, 36, 36
    n = len(items)
    slot = (W - 2 * pad_x) / n
    bar_w = slot * 0.65
    bars = ''
    for i, (label, val) in enumerate(items):
        x = pad_x + i * slot + (slot - bar_w) / 2
        bar_h = (val - lo) / rng * (H - pad_b - 2 * pad_y)
        y = H - pad_b - pad_y - bar_h
        v_str = fmt(val)
        bars += (
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="6" fill="{color}"/>'
            f'<text x="{x+bar_w/2:.1f}" y="{y-7:.1f}" fill="#dbeafe" text-anchor="middle" font-size="11">{v_str}</text>'
            f'<text x="{x+bar_w/2:.1f}" y="{H-pad_b+16}" fill="#a9bdd3" text-anchor="middle" font-size="11">{label}</text>'
        )
    mid_y = H - pad_b - pad_y - 0.5 * (H - pad_b - 2 * pad_y)
    lines = (
        f'<line x1="{pad_x}" y1="{pad_y}" x2="{W-pad_x}" y2="{pad_y}" stroke="#20344c" stroke-width="1"/>'
        f'<line x1="{pad_x}" y1="{mid_y}" x2="{W-pad_x}" y2="{mid_y}" stroke="#20344c" stroke-width="1"/>'
        f'<line x1="{pad_x}" y1="{H-pad_b}" x2="{W-pad_x}" y2="{H-pad_b}" stroke="#20344c" stroke-width="1"/>'
    )
    return f'<svg class="chart" viewBox="0 0 {W} {H}">{lines}{bars}</svg>'


# ── Country pages ──────────────────────────────────────────────────────────────

def country_intro(country: str, sub) -> str:
    first = sub.iloc[0]
    last = sub.iloc[-1]
    return (
        f'Entre {int(first["Año"])} y {int(last["Año"])}, {country} muestra una evolución '
        f'en la que la población de 65 años o más aumenta, mientras que la proporción de '
        f'0 a 14 años disminuye. Esta combinación sitúa al país dentro del proceso regional '
        f'de transición demográfica.'
    )


def build_country_page(country: str, sub, latest, all_countries, docs_dir: Path) -> None:
    slug = slugify(country)
    years = list(sub['Año'].astype(int))
    series_65 = [(str(y), float(r['Pct_65_más'])) for y, (_, r) in zip(years, sub.iterrows())]
    series_pop = [(str(y), float(r['Población_Total_Millones'])) for y, (_, r) in zip(years, sub.iterrows())]

    intro = country_intro(country, sub)
    kpis = f"""<div class="kpis">
 <div class="kpi"><strong>Último año</strong><div>{int(latest['Año'])}</div></div>
 <div class="kpi"><strong>Población total</strong><div>{fmt(latest['Población_Total_Millones'])} M</div></div>
 <div class="kpi"><strong>65+ años</strong><div>{fmt(latest['Pct_65_más'])}%</div></div>
 <div class="kpi"><strong>Índice de envejecimiento</strong><div>{fmt(latest['Indice_Envejecimiento'])}</div></div>
</div>"""

    table_rows = ''
    for _, r in sub.iterrows():
        yr = int(r['Año'])
        table_rows += (
            f"<tr><td>{yr}</td>"
            f"<td>{fmt(r['Población_Total_Millones'])}</td>"
            f"<td>{fmt(r['Pct_0_14'])}%</td>"
            f"<td>{fmt(r['Pct_65_más'])}%</td>"
            f"<td>{fmt(r['Indice_Envejecimiento'])}</td>"
            f"<td><a href='country-{slug}-year-{yr}.html'>Ficha completa</a></td></tr>"
        )

    related_countries = [c for c in all_countries if c != country][:3]
    related_links = ''.join([
        f"<a href='country-{slugify(c)}.html'>{html.escape(c)}</a>"
        for c in related_countries
    ])
    related_links += (
        f"<a href='research-questions/como-cambio-la-estructura-por-edades-en-{slug}.html'>"
        f"Estructura por edades en {html.escape(country)}</a>"
        f"<a href='research-questions/como-evoluciono-la-poblacion-de-65-anos-o-mas-en-{slug}.html'>"
        f"65+ años en {html.escape(country)}</a>"
        f"<a href='research-questions/como-cambio-la-poblacion-de-0-a-14-anos-en-{slug}.html'>"
        f"0–14 años en {html.escape(country)}</a>"
    )

    body = f"""<div class="hero"><h1>{html.escape(country)}</h1><p class="sub">{intro}</p>
{kpis}</div>
<div class="section grid">
 <div class="card"><h2>Evolución de 65+ años</h2>{line_chart(series_65)}
  <p class="small">Comentario: una trayectoria ascendente sugiere una mayor presencia relativa de población mayor.</p></div>
 <div class="card"><h2>Evolución de la población total</h2>{line_chart(series_pop, '#fbbf24')}
  <p class="small">Comentario: esta serie permite interpretar el envejecimiento junto con el tamaño poblacional total.</p></div>
</div>
<div class="section card"><h2>Tabla de resumen por año</h2>
<table><thead><tr><th>Año</th><th>Población total</th><th>0–14</th><th>65+</th><th>Índice envejecimiento</th><th>Detalle</th></tr></thead>
<tbody>{table_rows}</tbody></table>
<p class="small">Comentario: la tabla resume el desplazamiento de la estructura por edades y enlaza a la ficha detallada de cada corte temporal.</p></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>{related_links}</div></div>"""

    page_url = f"{BASE_URL}/pages/country-{slug}.html"
    out = docs_dir / 'pages' / f'country-{slug}.html'
    out.write_text(render_page(
        f'{country} | estructura demográfica',
        f'Serie temporal y detalle demográfico de {country} dentro del dataset de América Latina 2000–2023.',
        body, page_url,
    ), encoding='utf-8')


def build_country_year_page(country: str, row, docs_dir: Path) -> None:
    slug = slugify(country)
    yr = int(row['Año'])

    kpis = f"""<div class="kpis">
 <div class="kpi"><strong>Año</strong><div>{yr}</div></div>
 <div class="kpi"><strong>Población total</strong><div>{fmt(row['Población_Total_Millones'])} M</div></div>
 <div class="kpi"><strong>65+ años</strong><div>{fmt(row['Pct_65_más'])}%</div></div>
 <div class="kpi"><strong>0–14 años</strong><div>{fmt(row['Pct_0_14'])}%</div></div>
</div>"""

    indicators_rows = (
        f"<tr><td>Índice de envejecimiento</td><td>{fmt(row['Indice_Envejecimiento'])}</td></tr>"
        f"<tr><td>Razón de dependencia total</td><td>{fmt(row['Razon_Dependencia_Total'])}</td></tr>"
        f"<tr><td>Razón de dependencia infantil</td><td>{fmt(row['Razon_Dependencia_Infantil'])}</td></tr>"
        f"<tr><td>Razón de dependencia mayores</td><td>{fmt(row['Razon_Dependencia_Mayores'])}</td></tr>"
        f"<tr><td>Índice bono demográfico</td><td>{fmt(row['Indice_Bono_Demografico'], 4)}</td></tr>"
    )
    groups_rows = (
        f"<tr><td>0–14 años</td><td>{fmt(row['Pct_0_14'])}%</td><td>{fmt(row['Pob_0_14_Miles'])} miles</td></tr>"
        f"<tr><td>15–24 años</td><td>{fmt(row['Pct_15_24'])}%</td><td>{fmt(row['Pob_15_24_Miles'])} miles</td></tr>"
        f"<tr><td>25–54 años</td><td>{fmt(row['Pct_25_54'])}%</td><td>{fmt(row['Pob_25_54_Miles'])} miles</td></tr>"
        f"<tr><td>55–64 años</td><td>{fmt(row['Pct_55_64'])}%</td><td>{fmt(row['Pob_55_64_Miles'])} miles</td></tr>"
        f"<tr><td>65+ años</td><td>{fmt(row['Pct_65_más'])}%</td><td>{fmt(row['Pob_65_más_Miles'])} miles</td></tr>"
    )

    body = f"""<div class="hero"><h1>{html.escape(country)} — {yr}</h1><p class="sub">Ficha detallada del corte {yr} para {html.escape(country)}.</p>
{kpis}</div>
<div class="section card"><h2>Grupos de edad</h2>
<table><thead><tr><th>Grupo</th><th>Porcentaje</th><th>Absoluto</th></tr></thead>
<tbody>{groups_rows}</tbody></table></div>
<div class="section card"><h2>Indicadores derivados</h2>
<table><thead><tr><th>Indicador</th><th>Valor</th></tr></thead>
<tbody>{indicators_rows}</tbody></table></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='country-{slug}.html'>Volver a {html.escape(country)}</a>
<a href='countries.html'>Todos los países</a>
</div></div>"""

    page_url = f"{BASE_URL}/pages/country-{slug}-year-{yr}.html"
    out = docs_dir / 'pages' / f'country-{slug}-year-{yr}.html'
    out.write_text(render_page(
        f'{country} {yr} | ficha demográfica',
        f'Detalle de la estructura por edades de {country} en {yr}.',
        body, page_url,
    ), encoding='utf-8')


# ── Comparison pages ───────────────────────────────────────────────────────────

def build_compare_page(country_a: str, country_b: str, row_a, row_b,
                       indicator_slug: str, indicator_label: str,
                       docs_dir: Path) -> None:
    slug_a = slugify(country_a)
    slug_b = slugify(country_b)
    col = indicator_slug  # column name in dataframe

    val_a = float(row_a[col]) if str(row_a[col]) not in ('nan', '') else None
    val_b = float(row_b[col]) if str(row_b[col]) not in ('nan', '') else None

    def v(x):
        return fmt(x) if x is not None else 'N/D'

    bar_data = []
    if val_a is not None:
        bar_data.append((country_a, val_a))
    if val_b is not None:
        bar_data.append((country_b, val_b))

    chart_html = bar_chart(bar_data) if bar_data else ''

    body = f"""<div class="hero">
<h1>Comparativa: {html.escape(country_a)} vs {html.escape(country_b)}</h1>
<p class="sub">Indicador: {html.escape(indicator_label)} · Último año disponible por país.</p>
</div>
<div class="section card">
{chart_html}
<table><thead><tr><th>Indicador</th><th>{html.escape(country_a)}</th><th>{html.escape(country_b)}</th></tr></thead>
<tbody>
<tr><td>{html.escape(indicator_label)}</td><td>{v(val_a)}</td><td>{v(val_b)}</td></tr>
<tr><td>Último año</td><td>{int(row_a['Año'])}</td><td>{int(row_b['Año'])}</td></tr>
<tr><td>Población total (M)</td><td>{fmt(row_a['Población_Total_Millones'])}</td><td>{fmt(row_b['Población_Total_Millones'])}</td></tr>
<tr><td>65+ años (%)</td><td>{fmt(row_a['Pct_65_más'])}</td><td>{fmt(row_b['Pct_65_más'])}</td></tr>
<tr><td>0–14 años (%)</td><td>{fmt(row_a['Pct_0_14'])}</td><td>{fmt(row_b['Pct_0_14'])}</td></tr>
<tr><td>Índice envejecimiento</td><td>{fmt(row_a['Indice_Envejecimiento'])}</td><td>{fmt(row_b['Indice_Envejecimiento'])}</td></tr>
</tbody></table></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='country-{slug_a}.html'>{html.escape(country_a)}</a>
<a href='country-{slug_b}.html'>{html.escape(country_b)}</a>
<a href='comparisons.html'>Todas las comparaciones</a>
</div></div>"""

    fname = f'compare-{slug_a}-vs-{slug_b}-{slugify(indicator_label)}.html'
    page_url = f"{BASE_URL}/pages/{fname}"
    out = docs_dir / 'pages' / fname
    out.write_text(render_page(
        f'{country_a} vs {country_b} | {indicator_label}',
        f'Comparativa de {indicator_label} entre {country_a} y {country_b}.',
        body, page_url,
    ), encoding='utf-8')


# ── Index pages ────────────────────────────────────────────────────────────────

INDICATORS = [
    ('Pct_65_más', 'pct_65_mas', '65+ años (%)'),
    ('Pct_0_14', 'pct_0_14', '0–14 años (%)'),
    ('Pct_15_24', 'pct_15_24', '15–24 años (%)'),
    ('Pct_25_54', 'pct_25_54', '25–54 años (%)'),
    ('Pct_55_64', 'pct_55_64', '55–64 años (%)'),
    ('Indice_Envejecimiento', 'indice_envejecimiento', 'Índice de envejecimiento'),
    ('Razon_Dependencia_Total', 'razon_dependencia_total', 'Razón de dependencia total'),
    ('Razon_Dependencia_Infantil', 'razon_dependencia_infantil', 'Razón de dependencia infantil'),
    ('Razon_Dependencia_Mayores', 'razon_dependencia_mayores', 'Razón de dependencia mayores'),
    ('Indice_Bono_Demografico', 'indice_bono_demografico', 'Índice bono demográfico'),
    ('Población_Total_Millones', 'poblacion_total_millones', 'Población total (millones)'),
    ('Pct_Edad_Laboral', 'pct_edad_laboral', 'Edad laboral (%)'),
]


def build_countries_index(df, countries, docs_dir: Path) -> None:
    latest = latest_by_country(df)
    latest_map = {row['País']: row for _, row in latest.iterrows()}
    cards = ''
    for country in countries:
        slug = slugify(country)
        row = latest_map[country]
        sub = df[df['País'] == country].sort_values('Año')
        series = [(str(int(r['Año'])), float(r['Pct_65_más'])) for _, r in sub.iterrows()]
        intro = country_intro(country, sub)
        cards += f"""<div class='card' data-search='{html.escape(country)}'>
<h3><a href='country-{slug}.html'>{html.escape(country)}</a></h3>
<p class='small'>{intro}</p>
<p class='small'>Último corte: {int(row['Año'])} · Población total: {fmt(row['Población_Total_Millones'])} millones · 65+ años: {fmt(row['Pct_65_más'])}%</p>
{line_chart(series, h=260)}
<p class='small'>Comentario: la línea resume la evolución del peso relativo de la población de 65 años o más en {html.escape(country)}.</p>
</div>"""

    body = f"""<div class='hero'><h1>Países incluidos en el dataset</h1><p class='sub'>Cada país dispone de una página principal con narrativa introductoria, gráficos, tabla resumen y bloques de navegación cruzada.</p><input id='searchBox' class='search' placeholder='Buscar país...'></div><div class='section grid'>{cards}</div>"""
    page_url = f"{BASE_URL}/pages/countries.html"
    out = docs_dir / 'pages' / 'countries.html'
    out.write_text(render_page('Países del dataset',
                               'Listado de países incluidos con vista previa del envejecimiento y enlaces a fichas detalladas.',
                               body, page_url), encoding='utf-8')


def build_years_index(df, docs_dir: Path) -> None:
    years = sorted(df['Año'].unique().astype(int).tolist())
    cards = ''
    for yr in years:
        sub = df[df['Año'] == yr]
        n = len(sub)
        avg_65 = sub['Pct_65_más'].mean()
        avg_env = sub['Indice_Envejecimiento'].mean()
        cards += f"""<div class='card'>
<h3><a href='year-{yr}.html'>{yr}</a></h3>
<p class='small'>Países cubiertos: {n} · % 65+ promedio: {fmt(avg_65)}% · Índice envejecimiento promedio: {fmt(avg_env)}</p>
</div>"""
    body = f"""<div class='hero'><h1>Años del dataset</h1><p class='sub'>Cortes temporales disponibles: {', '.join(str(y) for y in years)}.</p></div><div class='section grid'>{cards}</div>"""
    page_url = f"{BASE_URL}/pages/years.html"
    out = docs_dir / 'pages' / 'years.html'
    out.write_text(render_page('Años del dataset',
                               'Cortes temporales del dataset demográfico de América Latina.',
                               body, page_url), encoding='utf-8')


def build_year_page(yr: int, sub, docs_dir: Path) -> None:
    rows = ''
    for _, r in sub.sort_values('Indice_Envejecimiento', ascending=False).iterrows():
        slug = slugify(r['País'])
        rows += (f"<tr><td><a href='country-{slug}.html'>{html.escape(r['País'])}</a></td>"
                 f"<td>{fmt(r['Población_Total_Millones'])}</td>"
                 f"<td>{fmt(r['Pct_0_14'])}%</td>"
                 f"<td>{fmt(r['Pct_65_más'])}%</td>"
                 f"<td>{fmt(r['Indice_Envejecimiento'])}</td></tr>")
    body = f"""<div class='hero'><h1>Año {yr}</h1>
<p class='sub'>Resumen demográfico de los {len(sub)} países del dataset en {yr}.</p></div>
<div class='section card'>
<table><thead><tr><th>País</th><th>Población (M)</th><th>0–14 (%)</th><th>65+ (%)</th><th>Índice envej.</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='years.html'>Todos los años</a></div></div>"""
    page_url = f"{BASE_URL}/pages/year-{yr}.html"
    out = docs_dir / 'pages' / f'year-{yr}.html'
    out.write_text(render_page(f'Año {yr} | demografía regional',
                               f'Estructura demográfica de América Latina en {yr}.',
                               body, page_url), encoding='utf-8')


def build_indicators_index(docs_dir: Path) -> None:
    items = ''.join([
        f"<li><a href='indicator-{ind_slug}.html'>{html.escape(label)}</a></li>"
        for _, ind_slug, label in INDICATORS
    ])
    body = f"""<div class='hero'><h1>Indicadores del dataset</h1><p class='sub'>Doce indicadores disponibles con ranking regional.</p></div>
<div class='section card'><ul class='cols'>{items}</ul></div>"""
    page_url = f"{BASE_URL}/pages/indicators.html"
    out = docs_dir / 'pages' / 'indicators.html'
    out.write_text(render_page('Indicadores del dataset',
                               'Indicadores demográficos disponibles en el dataset de América Latina.',
                               body, page_url), encoding='utf-8')


def build_indicator_page(col: str, ind_slug: str, label: str, latest, docs_dir: Path) -> None:
    ranked = latest.sort_values(col, ascending=False)
    rows = ''
    for i, (_, r) in enumerate(ranked.iterrows(), 1):
        slug = slugify(r['País'])
        rows += (f"<tr><td>{i}</td>"
                 f"<td><a href='country-{slug}.html'>{html.escape(r['País'])}</a></td>"
                 f"<td>{fmt(r[col])}</td></tr>")
    bar_data = [(r['País'], float(r[col])) for _, r in ranked.iterrows()
                if str(r[col]) not in ('nan', '')]
    body = f"""<div class='hero'><h1>{html.escape(label)}</h1>
<p class='sub'>Ranking regional por {html.escape(label)} · último año disponible por país.</p></div>
<div class='section card'>
{bar_chart(bar_data)}
<table><thead><tr><th>Pos.</th><th>País</th><th>{html.escape(label)}</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='indicators.html'>Todos los indicadores</a></div></div>"""
    page_url = f"{BASE_URL}/pages/indicator-{ind_slug}.html"
    out = docs_dir / 'pages' / f'indicator-{ind_slug}.html'
    out.write_text(render_page(f'{label} | comparación regional',
                               f'Ranking de {label} en América Latina.',
                               body, page_url), encoding='utf-8')


def build_comparisons_index(countries, docs_dir: Path) -> None:
    items = ''
    for ca, cb in itertools.combinations(countries, 2):
        slug_a, slug_b = slugify(ca), slugify(cb)
        for col, ind_slug, label in INDICATORS:
            fname = f'compare-{slug_a}-vs-{slug_b}-{slugify(label)}.html'
            items += f"<li><a href='{fname}'>{html.escape(ca)} vs {html.escape(cb)} · {html.escape(label)}</a></li>"
    body = f"""<div class='hero'><h1>Comparaciones bilaterales</h1>
<p class='sub'>Comparativas entre pares de países para cada indicador.</p>
<input id='searchBox' class='search' placeholder='Buscar comparación...'></div>
<div class='section card'><ul class='cols'>{items}</ul></div>"""
    page_url = f"{BASE_URL}/pages/comparisons.html"
    out = docs_dir / 'pages' / 'comparisons.html'
    out.write_text(render_page('Comparaciones bilaterales',
                               'Comparativas entre pares de países del dataset de América Latina.',
                               body, page_url), encoding='utf-8')


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = parse_args('Genera el sitio HTML estático a partir del dataset.')
    args = parser.parse_args()
    docs_dir = args.docs_dir

    ensure_dir(docs_dir / 'pages')
    ensure_dir(docs_dir / 'pages' / 'research-questions')

    df = add_indicators(read_dataset(args.input)).sort_values(['País', 'Año']).reset_index(drop=True)
    latest = latest_by_country(df)
    latest_map = {row['País']: row for _, row in latest.iterrows()}
    countries = sorted(df['País'].unique().tolist())
    years = sorted(df['Año'].unique().astype(int).tolist())

    # Country pages
    for country in countries:
        sub = df[df['País'] == country].copy().sort_values('Año')
        build_country_page(country, sub, latest_map[country], countries, docs_dir)
        for _, row in sub.iterrows():
            build_country_year_page(country, row, docs_dir)

    # Comparison pages (country pairs × indicators)
    for ca, cb in itertools.combinations(countries, 2):
        for col, ind_slug, label in INDICATORS:
            build_compare_page(ca, cb, latest_map[ca], latest_map[cb],
                               col, label, docs_dir)

    # Index pages
    build_countries_index(df, countries, docs_dir)
    build_years_index(df, docs_dir)
    for yr in years:
        build_year_page(yr, df[df['Año'] == yr], docs_dir)
    build_indicators_index(docs_dir)
    for col, ind_slug, label in INDICATORS:
        build_indicator_page(col, ind_slug, label, latest, docs_dir)
    build_comparisons_index(countries, docs_dir)

    print(f'OK: {docs_dir / "pages"} — {len(countries)} países, {len(years)} años')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
