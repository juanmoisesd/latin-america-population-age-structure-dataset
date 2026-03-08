#!/usr/bin/env python3
from __future__ import annotations

import html
import itertools
import json
import sys
from pathlib import Path

from common import (
    add_indicators, ensure_dir,
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


def ld_json(title, description, page_url):
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


def nav(prefix='../'):
    return f"""<nav class="navlinks">
 <a href="{prefix}index.html">Inicio</a>
 <a href="{prefix}pages/countries.html">Países</a>
 <a href="{prefix}pages/years.html">Años</a>
 <a href="{prefix}pages/indicators.html">Indicadores</a>
 <a href="{prefix}pages/comparisons.html">Comparaciones</a>
 <a href="{prefix}pages/research-questions/index.html">Preguntas de investigación</a>
 <a href="{prefix}pages/about.html">Acerca del dataset</a>
 <a href="{ZENODO_RECORD}">Zenodo</a>
</nav>"""


def footer():
    return f"""<div class="footer">
 <p><strong>Autor:</strong> <a href="{AUTHOR_URL}">{AUTHOR}</a> · <a href="{ORCID}">ORCID</a> · <a href="{RESEARCHGATE}">ResearchGate</a></p>
 <p><strong>Repositorios:</strong> <a href="{ZENODO_DOI}">Zenodo DOI</a> · <a href="{ZENODO_RECORD}">Zenodo registro</a> · <a href="{OSF_DOI}">OSF DOI</a></p>
 <p><strong>Cómo citar:</strong> de la Serna, J. M. ({CITATION_YEAR}). <em>{CITATION_TITLE}</em>. Zenodo. <a href="{ZENODO_DOI}">{ZENODO_DOI}</a></p>
</div>"""


def render_page(title, description, body, page_url, css_prefix='../'):
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


def line_chart(series, color='#61dafb', h=260):
    if not series:
        return ''
    values = [v for _, v in series]
    lo, hi = min(values), max(values)
    rng = hi - lo if hi != lo else 1
    W, H = 760, h
    px, py, pb = 36, 36, 26
    n = len(series)
    xs = [px + i * (W - 2 * px) / max(n - 1, 1) for i in range(n)]
    ys = [H - pb - py - (v - lo) / rng * (H - pb - 2 * py) for _, v in series]
    mid_y = H - pb - py - 0.5 * (H - pb - 2 * py)
    lines = (
        f'<line x1="{px}" y1="{py}" x2="{W-px}" y2="{py}" stroke="#20344c" stroke-width="1"/>'
        f'<line x1="{px}" y1="{mid_y}" x2="{W-px}" y2="{mid_y}" stroke="#20344c" stroke-width="1"/>'
        f'<line x1="{px}" y1="{H-pb}" x2="{W-px}" y2="{H-pb}" stroke="#20344c" stroke-width="1"/>'
    )
    pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in zip(xs, ys))
    poly = f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{pts}"/>'
    circles = ''
    for (label, val), x, y in zip(series, xs, ys):
        circles += (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>'
            f'<text x="{x:.1f}" y="{y-10:.1f}" fill="#dbeafe" text-anchor="middle" font-size="11">{fmt(val)}</text>'
            f'<text x="{x:.1f}" y="{H-pb+16}" fill="#a9bdd3" text-anchor="middle" font-size="11">{label}</text>'
        )
    return f'<svg class="chart" viewBox="0 0 {W} {H}">{lines}{poly}{circles}</svg>'


def bar_chart(items, color='#61dafb', h=280):
    if not items:
        return ''
    values = [v for _, v in items]
    lo, hi = 0, max(values)
    rng = hi - lo if hi != lo else 1
    W, H = 760, h
    px, py, pb = 36, 36, 36
    n = len(items)
    slot = (W - 2 * px) / n
    bw = slot * 0.65
    bars = ''
    for i, (label, val) in enumerate(items):
        x = px + i * slot + (slot - bw) / 2
        bh = (val - lo) / rng * (H - pb - 2 * py)
        y = H - pb - py - bh
        bars += (
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="6" fill="{color}"/>'
            f'<text x="{x+bw/2:.1f}" y="{y-7:.1f}" fill="#dbeafe" text-anchor="middle" font-size="11">{fmt(val)}</text>'
            f'<text x="{x+bw/2:.1f}" y="{H-pb+16}" fill="#a9bdd3" text-anchor="middle" font-size="11">{label}</text>'
        )
    mid_y = H - pb - py - 0.5 * (H - pb - 2 * py)
    lines = (
        f'<line x1="{px}" y1="{py}" x2="{W-px}" y2="{py}" stroke="#20344c" stroke-width="1"/>'
        f'<line x1="{px}" y1="{mid_y}" x2="{W-px}" y2="{mid_y}" stroke="#20344c" stroke-width="1"/>'
        f'<line x1="{px}" y1="{H-pb}" x2="{W-px}" y2="{H-pb}" stroke="#20344c" stroke-width="1"/>'
    )
    return f'<svg class="chart" viewBox="0 0 {W} {H}">{lines}{bars}</svg>'


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


def country_intro(country, sub):
    first, last = sub.iloc[0], sub.iloc[-1]
    return (
        f'Entre {int(first["Año"])} y {int(last["Año"])}, {country} muestra una evolución '
        f'en la que la población de 65 años o más aumenta, mientras que la proporción de '
        f'0 a 14 años disminuye. Esta combinación sitúa al país dentro del proceso regional '
        f'de transición demográfica.'
    )


def build_country_page(country, sub, latest, all_countries, docs_dir):
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
            f"<tr><td>{yr}</td><td>{fmt(r['Población_Total_Millones'])}</td>"
            f"<td>{fmt(r['Pct_0_14'])}%</td><td>{fmt(r['Pct_65_más'])}%</td>"
            f"<td>{fmt(r['Indice_Envejecimiento'])}</td>"
            f"<td><a href='country-{slug}-year-{yr}.html'>Ficha completa</a></td></tr>"
        )
    related = [c for c in all_countries if c != country][:3]
    rel_links = ''.join([f"<a href='country-{slugify(c)}.html'>{html.escape(c)}</a>" for c in related])
    rel_links += (
        f"<a href='research-questions/como-cambio-la-estructura-por-edades-en-{slug}.html'>Estructura en {html.escape(country)}</a>"
        f"<a href='research-questions/como-evoluciono-la-poblacion-de-65-anos-o-mas-en-{slug}.html'>65+ en {html.escape(country)}</a>"
        f"<a href='research-questions/como-cambio-la-poblacion-de-0-a-14-anos-en-{slug}.html'>0–14 en {html.escape(country)}</a>"
    )
    body = f"""<div class="hero"><h1>{html.escape(country)}</h1><p class="sub">{intro}</p>{kpis}</div>
<div class="section grid">
 <div class="card"><h2>Evolución de 65+ años</h2>{line_chart(series_65)}<p class="small">Comentario: una trayectoria ascendente sugiere una mayor presencia relativa de población mayor.</p></div>
 <div class="card"><h2>Evolución de la población total</h2>{line_chart(series_pop, '#fbbf24')}<p class="small">Comentario: esta serie permite interpretar el envejecimiento junto con el tamaño poblacional total.</p></div>
</div>
<div class="section card"><h2>Tabla de resumen por año</h2>
<table><thead><tr><th>Año</th><th>Población total</th><th>0–14</th><th>65+</th><th>Índice envejecimiento</th><th>Detalle</th></tr></thead>
<tbody>{table_rows}</tbody></table>
<p class="small">Comentario: la tabla resume el desplazamiento de la estructura por edades y enlaza a la ficha detallada de cada corte temporal.</p></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>{rel_links}</div></div>"""
    page_url = f"{BASE_URL}/pages/country-{slug}.html"
    (docs_dir / 'pages' / f'country-{slug}.html').write_text(
        render_page(f'{country} | estructura demográfica',
                    f'Serie temporal y detalle demográfico de {country} dentro del dataset de América Latina 2000–2023.',
                    body, page_url), encoding='utf-8')


def build_country_year_page(country, row, docs_dir):
    slug = slugify(country)
    yr = int(row['Año'])
    kpis = f"""<div class="kpis">
 <div class="kpi"><strong>Año</strong><div>{yr}</div></div>
 <div class="kpi"><strong>Población total</strong><div>{fmt(row['Población_Total_Millones'])} M</div></div>
 <div class="kpi"><strong>65+ años</strong><div>{fmt(row['Pct_65_más'])}%</div></div>
 <div class="kpi"><strong>0–14 años</strong><div>{fmt(row['Pct_0_14'])}%</div></div>
</div>"""
    groups = (
        f"<tr><td>0–14</td><td>{fmt(row['Pct_0_14'])}%</td><td>{fmt(row['Pob_0_14_Miles'])} miles</td></tr>"
        f"<tr><td>15–24</td><td>{fmt(row['Pct_15_24'])}%</td><td>{fmt(row['Pob_15_24_Miles'])} miles</td></tr>"
        f"<tr><td>25–54</td><td>{fmt(row['Pct_25_54'])}%</td><td>{fmt(row['Pob_25_54_Miles'])} miles</td></tr>"
        f"<tr><td>55–64</td><td>{fmt(row['Pct_55_64'])}%</td><td>{fmt(row['Pob_55_64_Miles'])} miles</td></tr>"
        f"<tr><td>65+</td><td>{fmt(row['Pct_65_más'])}%</td><td>{fmt(row['Pob_65_más_Miles'])} miles</td></tr>"
    )
    indicators = (
        f"<tr><td>Índice de envejecimiento</td><td>{fmt(row['Indice_Envejecimiento'])}</td></tr>"
        f"<tr><td>Razón dependencia total</td><td>{fmt(row['Razon_Dependencia_Total'])}</td></tr>"
        f"<tr><td>Razón dependencia infantil</td><td>{fmt(row['Razon_Dependencia_Infantil'])}</td></tr>"
        f"<tr><td>Razón dependencia mayores</td><td>{fmt(row['Razon_Dependencia_Mayores'])}</td></tr>"
        f"<tr><td>Índice bono demográfico</td><td>{fmt(row['Indice_Bono_Demografico'], 4)}</td></tr>"
    )
    body = f"""<div class='hero'><h1>{html.escape(country)} — {yr}</h1>
<p class='sub'>Ficha detallada del corte {yr} para {html.escape(country)}.</p>{kpis}</div>
<div class='section card'><h2>Grupos de edad</h2>
<table><thead><tr><th>Grupo</th><th>Porcentaje</th><th>Absoluto</th></tr></thead><tbody>{groups}</tbody></table></div>
<div class='section card'><h2>Indicadores derivados</h2>
<table><thead><tr><th>Indicador</th><th>Valor</th></tr></thead><tbody>{indicators}</tbody></table></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='country-{slug}.html'>Volver a {html.escape(country)}</a>
<a href='countries.html'>Todos los países</a></div></div>"""
    page_url = f"{BASE_URL}/pages/country-{slug}-year-{yr}.html"
    (docs_dir / 'pages' / f'country-{slug}-year-{yr}.html').write_text(
        render_page(f'{country} {yr} | ficha demográfica',
                    f'Detalle de la estructura por edades de {country} en {yr}.',
                    body, page_url), encoding='utf-8')


def build_compare_page(ca, cb, row_a, row_b, col, label, docs_dir):
    sa, sb = slugify(ca), slugify(cb)
    def v(x):
        try:
            return fmt(float(x))
        except Exception:
            return 'N/D'
    bar_data = []
    try:
        bar_data.append((ca, float(row_a[col])))
    except Exception:
        pass
    try:
        bar_data.append((cb, float(row_b[col])))
    except Exception:
        pass
    body = f"""<div class="hero">
<h1>Comparativa: {html.escape(ca)} vs {html.escape(cb)}</h1>
<p class="sub">Indicador: {html.escape(label)} · Último año disponible por país.</p></div>
<div class="section card">
{bar_chart(bar_data)}
<table><thead><tr><th>Indicador</th><th>{html.escape(ca)}</th><th>{html.escape(cb)}</th></tr></thead>
<tbody>
<tr><td>{html.escape(label)}</td><td>{v(row_a[col])}</td><td>{v(row_b[col])}</td></tr>
<tr><td>Último año</td><td>{int(row_a['Año'])}</td><td>{int(row_b['Año'])}</td></tr>
<tr><td>Población total (M)</td><td>{fmt(row_a['Población_Total_Millones'])}</td><td>{fmt(row_b['Población_Total_Millones'])}</td></tr>
<tr><td>65+ años (%)</td><td>{fmt(row_a['Pct_65_más'])}</td><td>{fmt(row_b['Pct_65_más'])}</td></tr>
<tr><td>0–14 años (%)</td><td>{fmt(row_a['Pct_0_14'])}</td><td>{fmt(row_b['Pct_0_14'])}</td></tr>
<tr><td>Índice envejecimiento</td><td>{fmt(row_a['Indice_Envejecimiento'])}</td><td>{fmt(row_b['Indice_Envejecimiento'])}</td></tr>
</tbody></table></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='country-{sa}.html'>{html.escape(ca)}</a>
<a href='country-{sb}.html'>{html.escape(cb)}</a>
<a href='comparisons.html'>Todas las comparaciones</a></div></div>"""
    fname = f'compare-{sa}-vs-{sb}-{slugify(label)}.html'
    page_url = f"{BASE_URL}/pages/{fname}"
    (docs_dir / 'pages' / fname).write_text(
        render_page(f'{ca} vs {cb} | {label}',
                    f'Comparativa de {label} entre {ca} y {cb}.',
                    body, page_url), encoding='utf-8')


def build_countries_index(df, countries, docs_dir):
    latest = latest_by_country(df)
    lm = {r['País']: r for _, r in latest.iterrows()}
    cards = ''
    for country in countries:
        slug = slugify(country)
        row = lm[country]
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
    (docs_dir / 'pages' / 'countries.html').write_text(
        render_page('Países del dataset',
                    'Listado de países incluidos con vista previa del envejecimiento y enlaces a fichas detalladas.',
                    body, page_url), encoding='utf-8')


def build_years_index(df, docs_dir):
    years = sorted(df['Año'].unique().astype(int).tolist())
    cards = ''.join([
        f"<div class='card'><h3><a href='year-{y}.html'>{y}</a></h3>"
        f"<p class='small'>Países: {len(df[df['Año']==y])} · 65+ promedio: {fmt(df[df['Año']==y]['Pct_65_más'].mean())}% · Índice envej. promedio: {fmt(df[df['Año']==y]['Indice_Envejecimiento'].mean())}</p></div>"
        for y in years
    ])
    body = f"""<div class='hero'><h1>Años del dataset</h1><p class='sub'>Cortes temporales: {', '.join(str(y) for y in years)}.</p></div><div class='section grid'>{cards}</div>"""
    page_url = f"{BASE_URL}/pages/years.html"
    (docs_dir / 'pages' / 'years.html').write_text(
        render_page('Años del dataset', 'Cortes temporales del dataset demográfico de América Latina.', body, page_url), encoding='utf-8')


def build_year_page(yr, sub, docs_dir):
    rows = ''.join([
        f"<tr><td><a href='country-{slugify(r['País'])}.html'>{html.escape(r['País'])}</a></td>"
        f"<td>{fmt(r['Población_Total_Millones'])}</td><td>{fmt(r['Pct_0_14'])}%</td>"
        f"<td>{fmt(r['Pct_65_más'])}%</td><td>{fmt(r['Indice_Envejecimiento'])}</td></tr>"
        for _, r in sub.sort_values('Indice_Envejecimiento', ascending=False).iterrows()
    ])
    body = f"""<div class='hero'><h1>Año {yr}</h1><p class='sub'>Resumen de {len(sub)} países en {yr}.</p></div>
<div class='section card'><table><thead><tr><th>País</th><th>Población (M)</th><th>0–14 (%)</th><th>65+ (%)</th><th>Índice envej.</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class='section card'><div class='related'><a href='years.html'>Todos los años</a></div></div>"""
    page_url = f"{BASE_URL}/pages/year-{yr}.html"
    (docs_dir / 'pages' / f'year-{yr}.html').write_text(
        render_page(f'Año {yr} | demografía regional', f'Estructura demográfica de América Latina en {yr}.', body, page_url), encoding='utf-8')


def build_indicators_index(docs_dir):
    items = ''.join([f"<li><a href='indicator-{s}.html'>{html.escape(l)}</a></li>" for _, s, l in INDICATORS])
    body = f"""<div class='hero'><h1>Indicadores del dataset</h1><p class='sub'>Doce indicadores disponibles con ranking regional.</p></div>
<div class='section card'><ul class='cols'>{items}</ul></div>"""
    page_url = f"{BASE_URL}/pages/indicators.html"
    (docs_dir / 'pages' / 'indicators.html').write_text(
        render_page('Indicadores del dataset', 'Indicadores demográficos disponibles en el dataset de América Latina.', body, page_url), encoding='utf-8')


def build_indicator_page(col, ind_slug, label, latest, docs_dir):
    ranked = latest.sort_values(col, ascending=False)
    rows = ''.join([
        f"<tr><td>{i}</td><td><a href='country-{slugify(r['País'])}.html'>{html.escape(r['País'])}</a></td><td>{fmt(r[col])}</td></tr>"
        for i, (_, r) in enumerate(ranked.iterrows(), 1)
    ])
    bar_data = [(r['País'], float(r[col])) for _, r in ranked.iterrows() if str(r[col]) not in ('nan', '')]
    body = f"""<div class='hero'><h1>{html.escape(label)}</h1><p class='sub'>Ranking regional · último año por país.</p></div>
<div class='section card'>{bar_chart(bar_data)}
<table><thead><tr><th>Pos.</th><th>País</th><th>{html.escape(label)}</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class='section card'><div class='related'><a href='indicators.html'>Todos los indicadores</a></div></div>"""
    page_url = f"{BASE_URL}/pages/indicator-{ind_slug}.html"
    (docs_dir / 'pages' / f'indicator-{ind_slug}.html').write_text(
        render_page(f'{label} | comparación regional', f'Ranking de {label} en América Latina.', body, page_url), encoding='utf-8')


def build_comparisons_index(countries, docs_dir):
    items = ''.join([
        f"<li><a href='compare-{slugify(ca)}-vs-{slugify(cb)}-{slugify(label)}.html'>{html.escape(ca)} vs {html.escape(cb)} · {html.escape(label)}</a></li>"
        for ca, cb in itertools.combinations(countries, 2)
        for _, _, label in INDICATORS
    ])
    body = f"""<div class='hero'><h1>Comparaciones bilaterales</h1>
<p class='sub'>Comparativas entre pares de países para cada indicador.</p>
<input id='searchBox' class='search' placeholder='Buscar comparación...'></div>
<div class='section card'><ul class='cols'>{items}</ul></div>"""
    page_url = f"{BASE_URL}/pages/comparisons.html"
    (docs_dir / 'pages' / 'comparisons.html').write_text(
        render_page('Comparaciones bilaterales', 'Comparativas entre pares de países del dataset de América Latina.', body, page_url), encoding='utf-8')


def main():
    parser = parse_args('Genera el sitio HTML estático a partir del dataset.')
    args = parser.parse_args()
    docs_dir = args.docs_dir
    ensure_dir(docs_dir / 'pages')
    ensure_dir(docs_dir / 'pages' / 'research-questions')

    df = add_indicators(read_dataset(args.input)).sort_values(['País', 'Año']).reset_index(drop=True)
    latest = latest_by_country(df)
    lm = {r['País']: r for _, r in latest.iterrows()}
    countries = sorted(df['País'].unique().tolist())
    years = sorted(df['Año'].unique().astype(int).tolist())

    for country in countries:
        sub = df[df['País'] == country].copy().sort_values('Año')
        build_country_page(country, sub, lm[country], countries, docs_dir)
        for _, row in sub.iterrows():
            build_country_year_page(country, row, docs_dir)

    for ca, cb in itertools.combinations(countries, 2):
        for col, ind_slug, label in INDICATORS:
            build_compare_page(ca, cb, lm[ca], lm[cb], col, label, docs_dir)

    build_countries_index(df, countries, docs_dir)
    build_years_index(df, docs_dir)
    for yr in years:
        build_year_page(yr, df[df['Año'] == yr], docs_dir)
    build_indicators_index(docs_dir)
    for col, ind_slug, label in INDICATORS:
        build_indicator_page(col, ind_slug, label, latest, docs_dir)
    build_comparisons_index(countries, docs_dir)

    print(f'OK: {len(countries)} países · {len(years)} años · {len(INDICATORS)} indicadores')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
