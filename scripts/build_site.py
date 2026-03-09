#!/usr/bin/env python3
# build_site.py - ACTUALIZADO para dataset iberoamericano 1995-2025
# Cambios: 19 paises, annos 1995/2000/2025, columnas sexo, slugs sin guion bajo
from __future__ import annotations
import html, itertools, json, sys
from pathlib import Path
from common import (add_indicators,ensure_dir,latest_by_country,parse_args,read_dataset,slugify)

BASE_URL      = "https://juanmoisesd.github.io/latin-america-population-age-structure-dataset"
AUTHOR        = "Juan Moises de la Serna"
ZENODO_DOI    = "https://doi.org/10.5281/zenodo.18891177"
ZENODO_RECORD = "https://zenodo.org/records/18891177"
OSF_DOI       = "https://doi.org/10.17605/OSF.IO/3WAEU"
ORCID         = "https://orcid.org/0000-0002-8401-8018"
RESEARCHGATE  = "https://www.researchgate.net/profile/Juan_Moises_De_La_Serna"
AUTHOR_URL    = "https://juanmoisesdelaserna.es/"
CITATION_YEAR  = "2026"
CITATION_TITLE = "Evolucion Poblacional por Grupos de Edad en Iberoamerica (1995-2025): Dataset Demografico por Pais"

def fmt(value, decimals=2):
    try:
        v = float(value)
        if decimals == 0 or v == int(v): return f'{int(v):,}'.replace(',','.')
        return f'{v:,.{decimals}f}'.replace(',','X').replace('.',',').replace('X','.')
    except Exception: return ''

def ld_json(title, description, page_url):
    return json.dumps({"@context":"https://schema.org","@type":"Dataset","name":title,
        "description":description,"creator":{"@type":"Person","name":AUTHOR,"url":AUTHOR_URL,
        "sameAs":[ORCID,RESEARCHGATE]},"url":page_url,"identifier":[ZENODO_DOI,OSF_DOI],
        "license":"https://creativecommons.org/licenses/by/4.0/"}, ensure_ascii=False)

def nav(prefix='../'):
    return (f'<nav class="navlinks">'
        f'<a href="{prefix}index.html">Inicio</a>'
        f'<a href="{prefix}pages/countries.html">Paises</a>'
        f'<a href="{prefix}pages/years.html">Anos</a>'
        f'<a href="{prefix}pages/indicators.html">Indicadores</a>'
        f'<a href="{prefix}pages/comparisons.html">Comparaciones</a>'
        f'<a href="{prefix}pages/research-questions/index.html">Preguntas de investigacion</a>'
        f'<a href="{prefix}pages/about.html">Acerca del dataset</a>'
        f'<a href="{ZENODO_RECORD}">Zenodo</a></nav>')

def footer():
    return (f'<div class="footer">'
        f'<p><strong>Autor:</strong> <a href="{AUTHOR_URL}">{AUTHOR}</a>'
        f' - <a href="{ORCID}">ORCID</a> - <a href="{RESEARCHGATE}">ResearchGate</a></p>'
        f'<p><strong>Repositorios:</strong> <a href="{ZENODO_DOI}">Zenodo DOI</a>'
        f' - <a href="{ZENODO_RECORD}">Zenodo registro</a>'
        f' - <a href="{OSF_DOI}">OSF DOI</a></p>'
        f'<p><strong>Como citar:</strong> de la Serna, J. M. ({CITATION_YEAR}).'
        f' <em>{CITATION_TITLE}</em>. Zenodo. <a href="{ZENODO_DOI}">{ZENODO_DOI}</a></p>'
        f'</div>')

def render_page(title, description, body, page_url, css_prefix='../'):
    return (f'<!doctype html><html lang="es"><head>'
        f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title>'
        f'<meta name="description" content="{html.escape(description)}">'
        f'<link rel="canonical" href="{page_url}">'
        f'<link rel="stylesheet" href="{css_prefix}assets/style.css">'
        f'<script defer src="{css_prefix}assets/app.js"></script>'
        f'<script type="application/ld+json">{ld_json(title,description,page_url)}</script>'
        f'</head><body><div class="wrap">'
        + nav(css_prefix) + body + footer() + '</div></body></html>')

def line_chart(series, color='#61dafb', h=260):
    if not series: return ''
    values=[v for _,v in series]; lo,hi=min(values),max(values); rng=hi-lo if hi!=lo else 1
    W,H=760,h; px,py,pb=36,36,26; n=len(series)
    xs=[px+i*(W-2*px)/max(n-1,1) for i in range(n)]
    ys=[H-pb-py-(v-lo)/rng*(H-pb-2*py) for _,v in series]
    mid_y=H-pb-py-0.5*(H-pb-2*py)
    lines=(f'<line x1="{px}" y1="{py}" x2="{W-px}" y2="{py}" stroke="#20344c" stroke-width="1"/>'
           f'<line x1="{px}" y1="{mid_y}" x2="{W-px}" y2="{mid_y}" stroke="#20344c" stroke-width="1"/>'
           f'<line x1="{px}" y1="{H-pb}" x2="{W-px}" y2="{H-pb}" stroke="#20344c" stroke-width="1"/>')
    pts=' '.join(f'{x:.1f},{y:.1f}' for x,y in zip(xs,ys))
    poly=f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{pts}"/>'
    circles=''
    for (label,val),x,y in zip(series,xs,ys):
        circles+=(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>'
                  f'<text x="{x:.1f}" y="{y-10:.1f}" fill="#dbeafe" text-anchor="middle" font-size="11">{fmt(val)}</text>'
                  f'<text x="{x:.1f}" y="{H-pb+16}" fill="#a9bdd3" text-anchor="middle" font-size="11">{label}</text>')
    return f'<svg class="chart" viewBox="0 0 {W} {H}">{lines}{poly}{circles}</svg>'

def bar_chart(items, color='#61dafb', h=280):
    if not items: return ''
    values=[v for _,v in items]; lo,hi=0,max(values); rng=hi-lo if hi!=lo else 1
    W,H=760,h; px,py,pb=36,36,36; n=len(items)
    slot=(W-2*px)/n; bw=slot*0.65; bars=''
    for i,(label,val) in enumerate(items):
        x=px+i*slot+(slot-bw)/2; bh=(val-lo)/rng*(H-pb-2*py); y=H-pb-py-bh
        bars+=(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="6" fill="{color}"/>'
               f'<text x="{x+bw/2:.1f}" y="{y-7:.1f}" fill="#dbeafe" text-anchor="middle" font-size="11">{fmt(val)}</text>'
               f'<text x="{x+bw/2:.1f}" y="{H-pb+16}" fill="#a9bdd3" text-anchor="middle" font-size="11">{label}</text>')
    mid_y=H-pb-py-0.5*(H-pb-2*py)
    lines=(f'<line x1="{px}" y1="{py}" x2="{W-px}" y2="{py}" stroke="#20344c" stroke-width="1"/>'
           f'<line x1="{px}" y1="{mid_y}" x2="{W-px}" y2="{mid_y}" stroke="#20344c" stroke-width="1"/>'
           f'<line x1="{px}" y1="{H-pb}" x2="{W-px}" y2="{H-pb}" stroke="#20344c" stroke-width="1"/>')
    return f'<svg class="chart" viewBox="0 0 {W} {H}">{lines}{bars}</svg>'

INDICATORS = [
    ('Pct_65_mas',              'pct-65-mas',              '65+ anos (%)'),
    ('Pct_0_14',                'pct-0-14',                '0-14 anos (%)'),
    ('Pct_15_24',               'pct-15-24',               '15-24 anos (%)'),
    ('Pct_25_54',               'pct-25-54',               '25-54 anos (%)'),
    ('Pct_55_64',               'pct-55-64',               '55-64 anos (%)'),
    ('Indice_Envejecimiento',   'indice-envejecimiento',   'Indice de envejecimiento'),
    ('Razon_Dependencia_Total', 'razon-dependencia-total', 'Razon de dependencia total'),
    ('Razon_Dependencia_Infantil','razon-dependencia-infantil','Razon de dependencia infantil'),
    ('Razon_Dependencia_Mayores','razon-dependencia-mayores','Razon de dependencia mayores'),
    ('Indice_Bono_Demografico', 'indice-bono-demografico', 'Indice bono demografico'),
    ('Poblacion_Total_Millones','poblacion-total-millones', 'Poblacion total (millones)'),
    ('Pct_Edad_Laboral',        'pct-edad-laboral',        'Edad laboral (%)'),
]

# Mapeo de nombre interno de columna (puede diferir del CSV normalizado)
COL_ALIAS = {
    'Pct_65_mas': 'Pct_65_mas',
    'Poblacion_Total_Millones': 'Poblacion_Total_Millones',
}

def get_col(row, col):
    # Intentar nombre directo y alias
    for c in [col, col.replace('_mas','_mas').replace('_','_')]:
        if c in row.index: return row[c]
    # fallback con Pct_65_mas -> Pct_65_mas
    return row.get(col, '')

def country_intro(country, sub):
    first,last=sub.iloc[0],sub.iloc[-1]
    return (f'Entre {int(first["Ano"])} y {int(last["Ano"])}, {country} muestra una evolucion '
            f'en la que la poblacion de 65 anos o mas aumenta, mientras que la proporcion de '
            f'0 a 14 anos disminuye, dentro del proceso regional de transicion demografica iberoamericana.')

def build_country_page(country, sub, latest, all_countries, docs_dir):
    slug=slugify(country)
    years=list(sub['Ano'].astype(int))
    p65   = 'Pct_65_mas' if 'Pct_65_mas' in sub.columns else 'Pct_65_mas'
    ptot  = 'Poblacion_Total_Millones' if 'Poblacion_Total_Millones' in sub.columns else 'Poblacion_Total_Millones'
    idx   = 'Indice_Envejecimiento'
    series_65  = [(str(y), float(r[p65]))  for y,(_,r) in zip(years,sub.iterrows())]
    series_pop = [(str(y), float(r[ptot])) for y,(_,r) in zip(years,sub.iterrows())]
    intro=country_intro(country,sub)
    kpis=(f'<div class="kpis">'
          f'<div class="kpi"><strong>Ultimo ano</strong><div>{int(latest["Ano"])}</div></div>'
          f'<div class="kpi"><strong>Poblacion total</strong><div>{fmt(latest[ptot])} M</div></div>'
          f'<div class="kpi"><strong>65+ anos</strong><div>{fmt(latest[p65])}%</div></div>'
          f'<div class="kpi"><strong>Indice de envejecimiento</strong><div>{fmt(latest[idx])}</div></div>'
          f'</div>')
    table_rows=''
    for _,r in sub.iterrows():
        yr=int(r['Ano'])
        table_rows+=(f"<tr><td>{yr}</td><td>{fmt(r[ptot])}</td>"
                     f"<td>{fmt(r['Pct_0_14'])}%</td><td>{fmt(r[p65])}%</td>"
                     f"<td>{fmt(r[idx])}</td>"
                     f"<td><a href='country-{slug}-year-{yr}.html'>Ficha completa</a></td></tr>")
    related=[c for c in all_countries if c!=country][:3]
    rel_links=''.join([f"<a href='country-{slugify(c)}.html'>{html.escape(c)}</a>" for c in related])
    body=(f'<div class="hero"><h1>{html.escape(country)}</h1><p class="sub">{intro}</p>{kpis}</div>'
          f'<div class="section grid">'
          f'<div class="card"><h2>Evolucion de 65+ anos</h2>{line_chart(series_65)}</div>'
          f'<div class="card"><h2>Evolucion de la poblacion total</h2>{line_chart(series_pop,"#fbbf24")}</div>'
          f'</div>'
          f'<div class="section card"><h2>Tabla de resumen por ano</h2>'
          f'<table><thead><tr><th>Ano</th><th>Poblacion total</th><th>0-14</th><th>65+</th><th>Indice envejecimiento</th><th>Detalle</th></tr></thead>'
          f'<tbody>{table_rows}</tbody></table></div>'
          f'<div class="section card"><h2>Tambien te puede interesar</h2><div class="related">{rel_links}</div></div>')
    page_url=f"{BASE_URL}/pages/country-{slug}.html"
    (docs_dir/'pages'/f'country-{slug}.html').write_text(
        render_page(f'{country} | estructura demografica',
                    f'Serie temporal demografica de {country} 1995-2025.',
                    body,page_url), encoding='utf-8')

def build_country_year_page(country, row, docs_dir):
    slug=slugify(country); yr=int(row['Ano'])
    p65='Pct_65_mas' if 'Pct_65_mas' in row.index else 'Pct_65_mas'
    ptot='Poblacion_Total_Millones' if 'Poblacion_Total_Millones' in row.index else 'Poblacion_Total_Millones'
    kpis=(f'<div class="kpis">'
          f'<div class="kpi"><strong>Ano</strong><div>{yr}</div></div>'
          f'<div class="kpi"><strong>Poblacion total</strong><div>{fmt(row[ptot])} M</div></div>'
          f'<div class="kpi"><strong>65+ anos</strong><div>{fmt(row[p65])}%</div></div>'
          f'<div class="kpi"><strong>0-14 anos</strong><div>{fmt(row["Pct_0_14"])}%</div></div>'
          f'</div>')
    def sex_row(label, pct, ph, pm):
        return (f"<tr><td>{label}</td><td>{fmt(row.get(pct,''))}%</td>"
                f"<td>{fmt(row.get(ph,''))}%</td><td>{fmt(row.get(pm,''))}%</td></tr>")
    groups=(sex_row('0-14',  'Pct_0_14',  'Pct_0_14_H',  'Pct_0_14_M')
           +sex_row('15-24', 'Pct_15_24', 'Pct_15_24_H', 'Pct_15_24_M')
           +sex_row('25-54', 'Pct_25_54', 'Pct_25_54_H', 'Pct_25_54_M')
           +sex_row('55-64', 'Pct_55_64', 'Pct_55_64_H', 'Pct_55_64_M')
           +sex_row('65+',   p65,          'Pct_65_H',    'Pct_65_M'))
    indicators=(f"<tr><td>Indice de envejecimiento</td><td>{fmt(row.get('Indice_Envejecimiento',''))}</td></tr>"
                f"<tr><td>Razon dependencia total</td><td>{fmt(row.get('Razon_Dependencia_Total',''))}</td></tr>"
                f"<tr><td>Razon dependencia infantil</td><td>{fmt(row.get('Razon_Dependencia_Infantil',''))}</td></tr>"
                f"<tr><td>Razon dependencia mayores</td><td>{fmt(row.get('Razon_Dependencia_Mayores',''))}</td></tr>"
                f"<tr><td>Indice bono demografico</td><td>{fmt(row.get('Indice_Bono_Demografico',''),4)}</td></tr>")
    body=(f'<div class="hero"><h1>{html.escape(country)} - {yr}</h1>'
          f'<p class="sub">Ficha detallada del corte {yr} para {html.escape(country)}.</p>{kpis}</div>'
          f'<div class="section card"><h2>Grupos de edad con desglose por sexo</h2>'
          f'<table><thead><tr><th>Grupo</th><th>Total</th><th>Hombres</th><th>Mujeres</th></tr></thead>'
          f'<tbody>{groups}</tbody></table></div>'
          f'<div class="section card"><h2>Indicadores derivados</h2>'
          f'<table><thead><tr><th>Indicador</th><th>Valor</th></tr></thead>'
          f'<tbody>{indicators}</tbody></table></div>'
          f'<div class="section card"><div class="related">'
          f"<a href='country-{slug}.html'>Volver a {html.escape(country)}</a>"
          f"<a href='countries.html'>Todos los paises</a>"
          f'</div></div>')
    page_url=f"{BASE_URL}/pages/country-{slug}-year-{yr}.html"
    (docs_dir/'pages'/f'country-{slug}-year-{yr}.html').write_text(
        render_page(f'{country} {yr} | ficha demografica',
                    f'Detalle demografico de {country} en {yr}.',body,page_url), encoding='utf-8')

def build_compare_page(ca,cb,row_a,row_b,col,label,slug_label,docs_dir):
    sa,sb=slugify(ca),slugify(cb)
    def v(x):
        try: return fmt(float(x))
        except: return 'N/D'
    p65='Pct_65_mas' if 'Pct_65_mas' in row_a.index else 'Pct_65_mas'
    ptot='Poblacion_Total_Millones' if 'Poblacion_Total_Millones' in row_a.index else 'Poblacion_Total_Millones'
    bar_data=[]
    try: bar_data.append((ca, float(row_a[col])))
    except: pass
    try: bar_data.append((cb, float(row_b[col])))
    except: pass
    body=(f'<div class="hero"><h1>Comparativa: {html.escape(ca)} vs {html.escape(cb)}</h1>'
          f'<p class="sub">Indicador: {html.escape(label)} - Ultimo ano disponible.</p></div>'
          f'<div class="section card">{bar_chart(bar_data)}'
          f'<table><thead><tr><th>Indicador</th><th>{html.escape(ca)}</th><th>{html.escape(cb)}</th></tr></thead>'
          f'<tbody>'
          f'<tr><td>{html.escape(label)}</td><td>{v(row_a[col])}</td><td>{v(row_b[col])}</td></tr>'
          f'<tr><td>Ultimo ano</td><td>{int(row_a["Ano"])}</td><td>{int(row_b["Ano"])}</td></tr>'
          f'<tr><td>Poblacion (M)</td><td>{fmt(row_a[ptot])}</td><td>{fmt(row_b[ptot])}</td></tr>'
          f'<tr><td>65+ anos (%)</td><td>{fmt(row_a[p65])}</td><td>{fmt(row_b[p65])}</td></tr>'
          f'<tr><td>0-14 anos (%)</td><td>{fmt(row_a["Pct_0_14"])}</td><td>{fmt(row_b["Pct_0_14"])}</td></tr>'
          f'<tr><td>Indice envejecimiento</td><td>{fmt(row_a.get("Indice_Envejecimiento",""))}</td><td>{fmt(row_b.get("Indice_Envejecimiento",""))}</td></tr>'
          f'</tbody></table></div>'
          f'<div class="section card"><div class="related">'
          f"<a href='country-{sa}.html'>{html.escape(ca)}</a>"
          f"<a href='country-{sb}.html'>{html.escape(cb)}</a>"
          f"<a href='comparisons.html'>Todas las comparaciones</a>"
          f'</div></div>')
    fname=f'compare-{sa}-vs-{sb}-{slug_label}.html'
    page_url=f"{BASE_URL}/pages/{fname}"
    (docs_dir/'pages'/fname).write_text(
        render_page(f'{ca} vs {cb} | {label}',f'Comparativa de {label} entre {ca} y {cb}.',
                    body,page_url), encoding='utf-8')

def build_countries_index(df,countries,docs_dir):
    p65='Pct_65_mas' if 'Pct_65_mas' in df.columns else 'Pct_65_mas'
    ptot='Poblacion_Total_Millones' if 'Poblacion_Total_Millones' in df.columns else 'Poblacion_Total_Millones'
    latest=latest_by_country(df); lm={r['Pais']:r for _,r in latest.iterrows()}
    cards=''
    for country in countries:
        slug=slugify(country); row=lm[country]
        sub=df[df['Pais']==country].sort_values('Ano')
        series=[(str(int(r['Ano'])),float(r[p65])) for _,r in sub.iterrows()]
        intro=country_intro(country,sub)
        cards+=(f'<div class="card" data-search="{html.escape(country)}">'
                f'<h3><a href="country-{slug}.html">{html.escape(country)}</a></h3>'
                f'<p class="small">{intro}</p>'
                f'<p class="small">Ultimo corte: {int(row["Ano"])} - Poblacion: {fmt(row[ptot])} M - 65+: {fmt(row[p65])}%</p>'
                f'{line_chart(series,h=200)}</div>')
    body=(f'<div class="hero"><h1>Paises incluidos en el dataset</h1>'
          f'<p class="sub">19 paises iberoamericanos. Datos 1995-2025.</p>'
          f'<input id="searchBox" class="search" placeholder="Buscar pais..."></div>'
          f'<div class="section grid">{cards}</div>')
    page_url=f"{BASE_URL}/pages/countries.html"
    (docs_dir/'pages'/'countries.html').write_text(
        render_page('Paises del dataset','19 paises iberoamericanos 1995-2025.',body,page_url), encoding='utf-8')

def build_years_index(df,docs_dir):
    p65='Pct_65_mas' if 'Pct_65_mas' in df.columns else 'Pct_65_mas'
    years=sorted(df['Ano'].unique().astype(int).tolist())
    cards=''.join([
        f"<div class='card'><h3><a href='year-{y}.html'>{y}</a></h3>"
        f"<p class='small'>Paises: {len(df[df['Ano']==y])} - "
        f"65+ promedio: {fmt(df[df['Ano']==y][p65].mean())}% - "
        f"Indice envej. promedio: {fmt(df[df['Ano']==y]['Indice_Envejecimiento'].mean())}</p></div>"
        for y in years])
    body=(f"<div class='hero'><h1>Anos del dataset</h1>"
          f"<p class='sub'>Cortes temporales: {', '.join(str(y) for y in years)}.</p></div>"
          f"<div class='section grid'>{cards}</div>")
    page_url=f"{BASE_URL}/pages/years.html"
    (docs_dir/'pages'/'years.html').write_text(
        render_page('Anos del dataset','Cortes temporales 1995-2025.',body,page_url), encoding='utf-8')

def build_year_page(yr,sub,docs_dir):
    p65='Pct_65_mas' if 'Pct_65_mas' in sub.columns else 'Pct_65_mas'
    ptot='Poblacion_Total_Millones' if 'Poblacion_Total_Millones' in sub.columns else 'Poblacion_Total_Millones'
    rows=''.join([
        f"<tr><td><a href='country-{slugify(r['Pais'])}.html'>{html.escape(r['Pais'])}</a></td>"
        f"<td>{fmt(r[ptot])}</td><td>{fmt(r['Pct_0_14'])}%</td>"
        f"<td>{fmt(r[p65])}%</td><td>{fmt(r['Indice_Envejecimiento'])}</td></tr>"
        for _,r in sub.sort_values('Indice_Envejecimiento',ascending=False).iterrows()])
    body=(f"<div class='hero'><h1>Ano {yr}</h1><p class='sub'>Resumen de {len(sub)} paises en {yr}.</p></div>"
          f"<div class='section card'><table><thead><tr><th>Pais</th><th>Poblacion (M)</th>"
          f"<th>0-14 (%)</th><th>65+ (%)</th><th>Indice envej.</th></tr></thead><tbody>{rows}</tbody></table></div>"
          f"<div class='section card'><div class='related'><a href='years.html'>Todos los anos</a></div></div>")
    page_url=f"{BASE_URL}/pages/year-{yr}.html"
    (docs_dir/'pages'/f'year-{yr}.html').write_text(
        render_page(f'Ano {yr} | demografia regional',f'Estructura demografica iberoamericana en {yr}.',
                    body,page_url), encoding='utf-8')

def build_indicators_index(docs_dir):
    items=''.join([f"<li><a href='indicator-{s}.html'>{html.escape(l)}</a></li>" for _,s,l in INDICATORS])
    body=(f"<div class='hero'><h1>Indicadores del dataset</h1>"
          f"<p class='sub'>Doce indicadores disponibles con ranking regional.</p></div>"
          f"<div class='section card'><ul class='cols'>{items}</ul></div>")
    page_url=f"{BASE_URL}/pages/indicators.html"
    (docs_dir/'pages'/'indicators.html').write_text(
        render_page('Indicadores del dataset','Indicadores demograficos iberoamericanos.',body,page_url), encoding='utf-8')

def build_indicator_page(col,ind_slug,label,latest,docs_dir):
    ranked=latest.sort_values(col,ascending=False)
    rows=''.join([
        f"<tr><td>{i}</td><td><a href='country-{slugify(r['Pais'])}.html'>{html.escape(r['Pais'])}</a></td>"
        f"<td>{fmt(r[col])}</td></tr>"
        for i,(_,r) in enumerate(ranked.iterrows(),1)])
    bar_data=[(r['Pais'],float(r[col])) for _,r in ranked.iterrows() if str(r[col]) not in ('nan','')]
    body=(f"<div class='hero'><h1>{html.escape(label)}</h1><p class='sub'>Ranking regional - ultimo ano por pais.</p></div>"
          f"<div class='section card'>{bar_chart(bar_data)}"
          f"<table><thead><tr><th>Pos.</th><th>Pais</th><th>{html.escape(label)}</th></tr></thead>"
          f"<tbody>{rows}</tbody></table></div>"
          f"<div class='section card'><div class='related'><a href='indicators.html'>Todos los indicadores</a></div></div>")
    page_url=f"{BASE_URL}/pages/indicator-{ind_slug}.html"
    (docs_dir/'pages'/f'indicator-{ind_slug}.html').write_text(
        render_page(f'{label} | comparacion regional',f'Ranking de {label} en Iberoamerica.',
                    body,page_url), encoding='utf-8')

def build_comparisons_index(countries,docs_dir):
    items=''.join([
        f"<li><a href='compare-{slugify(ca)}-vs-{slugify(cb)}-{slug}.html'>"
        f"{html.escape(ca)} vs {html.escape(cb)} - {html.escape(label)}</a></li>"
        for ca,cb in itertools.combinations(countries,2) for _,slug,label in INDICATORS])
    body=(f"<div class='hero'><h1>Comparaciones bilaterales</h1>"
          f"<p class='sub'>Comparativas entre pares de paises para cada indicador.</p>"
          f"<input id='searchBox' class='search' placeholder='Buscar comparacion...'></div>"
          f"<div class='section card'><ul class='cols'>{items}</ul></div>")
    page_url=f"{BASE_URL}/pages/comparisons.html"
    (docs_dir/'pages'/'comparisons.html').write_text(
        render_page('Comparaciones bilaterales','Comparativas entre pares de paises iberoamericanos.',
                    body,page_url), encoding='utf-8')

def main():
    parser=parse_args('Genera el sitio HTML estatico a partir del dataset.')
    args=parser.parse_args()
    docs_dir=args.docs_dir
    ensure_dir(docs_dir/'pages')
    ensure_dir(docs_dir/'pages'/'research-questions')
    df=add_indicators(read_dataset(args.input)).sort_values(['Pais','Ano']).reset_index(drop=True)
    latest=latest_by_country(df); lm={r['Pais']:r for _,r in latest.iterrows()}
    countries=sorted(df['Pais'].unique().tolist())
    years=sorted(df['Ano'].unique().astype(int).tolist())
    for country in countries:
        sub=df[df['Pais']==country].copy().sort_values('Ano')
        build_country_page(country,sub,lm[country],countries,docs_dir)
        for _,row in sub.iterrows():
            build_country_year_page(country,row,docs_dir)
    for ca,cb in itertools.combinations(countries,2):
        for col,slug_label,label in INDICATORS:
            build_compare_page(ca,cb,lm[ca],lm[cb],col,label,slug_label,docs_dir)
    build_countries_index(df,countries,docs_dir)
    build_years_index(df,docs_dir)
    for yr in years:
        build_year_page(yr,df[df['Ano']==yr],docs_dir)
    build_indicators_index(docs_dir)
    for col,slug_label,label in INDICATORS:
        build_indicator_page(col,slug_label,label,latest,docs_dir)
    build_comparisons_index(countries,docs_dir)
    print(f'OK: {len(countries)} paises - {len(years)} anos - {len(INDICATORS)} indicadores')
    return 0

if __name__ == '__main__':
    try: raise SystemExit(main())
    except Exception as exc: print(f'ERROR: {exc}',file=sys.stderr); raise
