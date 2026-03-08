#!/usr/bin/env python3
from __future__ import annotations

import html
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


def nav() -> str:
    return f"""<nav class="navlinks">
 <a href="../../index.html">Inicio</a>
 <a href="../../pages/countries.html">Países</a>
 <a href="../../pages/years.html">Años</a>
 <a href="../../pages/indicators.html">Indicadores</a>
 <a href="../../pages/comparisons.html">Comparaciones</a>
 <a href="../../pages/research-questions/index.html">Preguntas de investigación</a>
 <a href="../../pages/about.html">Acerca del dataset</a>
 <a href="{ZENODO_RECORD}">Zenodo</a>
</nav>"""


def footer() -> str:
    return f"""<div class="footer">
 <p><strong>Autor:</strong> <a href="{AUTHOR_URL}">{AUTHOR}</a> · <a href="{ORCID}">ORCID</a> · <a href="{RESEARCHGATE}">ResearchGate</a></p>
 <p><strong>Repositorios:</strong> <a href="{ZENODO_DOI}">Zenodo DOI</a> · <a href="{ZENODO_RECORD}">Zenodo registro</a> · <a href="{OSF_DOI}">OSF DOI</a></p>
 <p><strong>Cómo citar:</strong> de la Serna, J. M. ({CITATION_YEAR}). <em>{CITATION_TITLE}</em>. Zenodo. <a href="{ZENODO_DOI}">{ZENODO_DOI}</a></p>
</div>"""


def render_page(title: str, description: str, body: str, page_url: str) -> str:
    return f"""<!doctype html>
<html lang="es"><head>
 <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
 <title>{html.escape(title)}</title>
 <meta name="description" content="{html.escape(description)}">
 <link rel="canonical" href="{page_url}">
 <link rel="stylesheet" href="../../assets/style.css"><script defer src="../../assets/app.js"></script>
 <script type="application/ld+json">{ld_json(title, description, page_url)}</script>
</head><body><div class="wrap">
{nav()}
{body}
{footer()}
</div></body></html>"""


def fmt(value, decimals=2):
    try:
        v = float(value)
        if decimals == 0 or v == int(v):
            return f'{int(v):,}'.replace(',', '.')
        return f'{v:,.{decimals}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
        return ''


def line_chart(series: list[tuple], color: str = '#61dafb', h: int = 260) -> str:
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


# ── Global research questions ─────────────────────────────────────────────────

def build_global_rq(slug: str, title: str, description: str,
                    ranked, value_col: str, decimals: int,
                    rq_dir: Path) -> None:
    rows = ''
    for i, (_, r) in enumerate(ranked.iterrows(), 1):
        c_slug = slugify(r['País'])
        rows += (f"<tr><td>{i}</td>"
                 f"<td><a href='../country-{c_slug}.html'>{html.escape(r['País'])}</a></td>"
                 f"<td>{fmt(r[value_col], decimals)}</td></tr>")
    body = f"""<div class='hero'><h1>{html.escape(title)}</h1>
<p class='sub'>{html.escape(description)}</p></div>
<div class='section card'>
<table><thead><tr><th>Pos.</th><th>País</th><th>Valor</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='index.html'>Todas las preguntas</a>
<a href='../countries.html'>Explorar países</a>
</div></div>"""
    page_url = f"{BASE_URL}/pages/research-questions/{slug}.html"
    out = rq_dir / f'{slug}.html'
    out.write_text(render_page(title, description, body, page_url), encoding='utf-8')


# ── Per-country research questions ────────────────────────────────────────────

def build_country_rq_estructura(country: str, sub, rq_dir: Path) -> None:
    slug = slugify(country)
    series_65 = [(str(int(r['Año'])), float(r['Pct_65_más'])) for _, r in sub.iterrows()]
    series_014 = [(str(int(r['Año'])), float(r['Pct_0_14'])) for _, r in sub.iterrows()]
    title = f'¿Cómo cambió la estructura por edades en {country} entre 2000 y 2023?'
    description = f'Evolución de los grupos de edad en {country} entre 2000 y 2023.'
    body = f"""<div class='hero'><h1>{html.escape(title)}</h1>
<p class='sub'>{html.escape(description)}</p></div>
<div class='section grid'>
<div class='card'><h2>65+ años (%)</h2>{line_chart(series_65)}
<p class='small'>Comentario: evolución de la población mayor relativa en {html.escape(country)}.</p></div>
<div class='card'><h2>0–14 años (%)</h2>{line_chart(series_014, '#fbbf24')}
<p class='small'>Comentario: evolución de la población joven relativa en {html.escape(country)}.</p></div>
</div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='../country-{slug}.html'>{html.escape(country)}</a>
<a href='como-evoluciono-la-poblacion-de-65-anos-o-mas-en-{slug}.html'>65+ en {html.escape(country)}</a>
<a href='index.html'>Todas las preguntas</a>
</div></div>"""
    page_url = f"{BASE_URL}/pages/research-questions/como-cambio-la-estructura-por-edades-en-{slug}.html"
    out = rq_dir / f'como-cambio-la-estructura-por-edades-en-{slug}.html'
    out.write_text(render_page(title, description, body, page_url), encoding='utf-8')


def build_country_rq_65(country: str, sub, rq_dir: Path) -> None:
    slug = slugify(country)
    series = [(str(int(r['Año'])), float(r['Pct_65_más'])) for _, r in sub.iterrows()]
    first, last = sub.iloc[0], sub.iloc[-1]
    diff = round(float(last['Pct_65_más']) - float(first['Pct_65_más']), 1)
    direction = 'aumentó' if diff >= 0 else 'disminuyó'
    title = f'¿Cómo evolucionó la población de 65 años o más en {country} entre 2000 y 2023?'
    description = f'La proporción de 65+ en {country} {direction} {abs(diff)} puntos porcentuales entre {int(first["Año"])} y {int(last["Año"])}.'
    body = f"""<div class='hero'><h1>{html.escape(title)}</h1>
<p class='sub'>{html.escape(description)}</p></div>
<div class='section card'>{line_chart(series)}
<p class='small'>Comentario: la línea muestra la evolución del porcentaje de población de 65 años o más en {html.escape(country)}.</p></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='../country-{slug}.html'>{html.escape(country)}</a>
<a href='como-cambio-la-estructura-por-edades-en-{slug}.html'>Estructura en {html.escape(country)}</a>
<a href='index.html'>Todas las preguntas</a>
</div></div>"""
    page_url = f"{BASE_URL}/pages/research-questions/como-evoluciono-la-poblacion-de-65-anos-o-mas-en-{slug}.html"
    out = rq_dir / f'como-evoluciono-la-poblacion-de-65-anos-o-mas-en-{slug}.html'
    out.write_text(render_page(title, description, body, page_url), encoding='utf-8')


def build_country_rq_014(country: str, sub, rq_dir: Path) -> None:
    slug = slugify(country)
    series = [(str(int(r['Año'])), float(r['Pct_0_14'])) for _, r in sub.iterrows()]
    first, last = sub.iloc[0], sub.iloc[-1]
    diff = round(float(last['Pct_0_14']) - float(first['Pct_0_14']), 1)
    direction = 'aumentó' if diff >= 0 else 'disminuyó'
    title = f'¿Cómo cambió la población de 0 a 14 años en {country} entre 2000 y 2023?'
    description = f'La proporción de 0-14 en {country} {direction} {abs(diff)} puntos porcentuales entre {int(first["Año"])} y {int(last["Año"])}.'
    body = f"""<div class='hero'><h1>{html.escape(title)}</h1>
<p class='sub'>{html.escape(description)}</p></div>
<div class='section card'>{line_chart(series, '#fbbf24')}
<p class='small'>Comentario: la línea muestra la evolución del porcentaje de población de 0 a 14 años en {html.escape(country)}.</p></div>
<div class='section card'><h2>También te puede interesar</h2><div class='related'>
<a href='../country-{slug}.html'>{html.escape(country)}</a>
<a href='como-cambio-la-estructura-por-edades-en-{slug}.html'>Estructura en {html.escape(country)}</a>
<a href='index.html'>Todas las preguntas</a>
</div></div>"""
    page_url = f"{BASE_URL}/pages/research-questions/como-cambio-la-poblacion-de-0-a-14-anos-en-{slug}.html"
    out = rq_dir / f'como-cambio-la-poblacion-de-0-a-14-anos-en-{slug}.html'
    out.write_text(render_page(title, description, body, page_url), encoding='utf-8')


# ── Research questions index ─────────────────────────────────────────────────

def build_rq_index(rq_dir: Path, countries: list[str], global_slugs: list[tuple]) -> None:
    items = ''
    for slug, title in global_slugs:
        items += f"<li data-search='{html.escape(title)}'><a href='{slug}.html'>{html.escape(title)}</a></li>"
    for country in countries:
        slug = slugify(country)
        for rq_slug, rq_title in [
            (f'como-cambio-la-estructura-por-edades-en-{slug}',
             f'¿Cómo cambió la estructura por edades en {country} entre 2000 y 2023?'),
            (f'como-evoluciono-la-poblacion-de-65-anos-o-mas-en-{slug}',
             f'¿Cómo evolucionó la población de 65 años o más en {country} entre 2000 y 2023?'),
            (f'como-cambio-la-poblacion-de-0-a-14-anos-en-{slug}',
             f'¿Cómo cambió la población de 0 a 14 años en {country} entre 2000 y 2023?'),
        ]:
            items += f"<li data-search='{html.escape(rq_title)}'><a href='{rq_slug}.html'>{html.escape(rq_title)}</a></li>"

    body = f"""<div class="hero"><h1>Preguntas de investigación</h1>
<p class="sub">Aquí el dataset responde preguntas concretas de investigación y divulgación. Esta versión amplía mucho las páginas por país + pregunta.</p>
<input id="searchBox" class="search" placeholder="Buscar pregunta..."></div>
<div class="section card"><ul class="cols">{items}</ul></div>"""

    page_url = f"{BASE_URL}/pages/research-questions/index.html"
    out = rq_dir / 'index.html'
    out.write_text(render_page('Preguntas de investigación',
                               'Preguntas de investigación respondidas mediante el dataset demográfico de América Latina.',
                               body, page_url), encoding='utf-8')


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = parse_args('Genera páginas de investigación con rankings automáticos.')
    args = parser.parse_args()

    rq_dir = args.docs_dir / 'pages' / 'research-questions'
    ensure_dir(rq_dir)

    df = add_indicators(read_dataset(args.input))
    latest = latest_by_country(df)
    countries = sorted(df['País'].unique().tolist())

    # Global questions
    global_questions = [
        ('que-paises-tienen-mas-poblacion-de-65-en-2023',
         '¿Qué países de América Latina tienen más población de 65+ en 2023?',
         'Ranking por porcentaje de población de 65 años o más en el último corte.',
         latest.sort_values('Pct_65_más', ascending=False),
         'Pct_65_más', 1),
        ('que-paises-presentan-mayor-indice-de-envejecimiento-en-2023',
         '¿Qué países presentan mayor índice de envejecimiento en 2023?',
         'Ranking basado en el último año disponible por país.',
         latest.sort_values('Indice_Envejecimiento', ascending=False),
         'Indice_Envejecimiento', 2),
        ('que-paises-mantienen-una-estructura-mas-joven-en-2023',
         '¿Qué países mantienen una estructura más joven en 2023?',
         'Ranking por porcentaje de población de 0 a 14 años en el último corte.',
         latest.sort_values('Pct_0_14', ascending=False),
         'Pct_0_14', 1),
        ('que-paises-tienen-mas-poblacion-total-en-2023',
         '¿Qué países tienen más población total en 2023?',
         'Ranking por población total en millones en el último corte.',
         latest.sort_values('Población_Total_Millones', ascending=False),
         'Población_Total_Millones', 1),
    ]

    global_slugs = [(slug, title) for slug, title, *_ in global_questions]

    for slug, title, desc, ranked, col, dec in global_questions:
        build_global_rq(slug, title, desc, ranked, col, dec, rq_dir)
        print(f'OK: {rq_dir / slug}.html')

    # Per-country questions
    for country in countries:
        sub = df[df['País'] == country].copy().sort_values('Año')
        build_country_rq_estructura(country, sub, rq_dir)
        build_country_rq_65(country, sub, rq_dir)
        build_country_rq_014(country, sub, rq_dir)
        print(f'OK: preguntas para {country}')

    # Index
    build_rq_index(rq_dir, countries, global_slugs)
    print(f'OK: {rq_dir / "index.html"}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
