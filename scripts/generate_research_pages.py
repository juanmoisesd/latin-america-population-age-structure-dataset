#!/usr/bin/env python3
"""
generate_research_pages.py - Genera páginas de preguntas de investigación.
"""
from __future__ import annotations
import html, json, math, sys
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd

SITE_TITLE = "Latin America Population Age Structure Dataset"
SITE_BASE_URL = "https://juanmoisesd.github.io/latin-america-population-age-structure-dataset"
AUTHOR_NAME = "Juan Moisés de la Serna"
AUTHOR_ORCID = "https://orcid.org/0000-0002-8401-8018"
DOI_DATASET = "https://doi.org/10.5281/zenodo.18891177"
ZENODO_RECORD = "https://zenodo.org/records/18891177"
RESEARCHGATE = "https://www.researchgate.net/profile/Juan_Moises_De_La_Serna"
AUTHOR_URL = "https://juanmoisesdelaserna.es/"

def slugify(text):
    t = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ü":"u","ñ":"n",
         "Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ü":"U","Ñ":"N"}
    res = "".join(t.get(c, c) for c in str(text)).lower()
    out, prev = [], False
    for ch in res:
        if ch.isalnum():
            out.append(ch); prev = False
        elif not prev:
            out.append("-"); prev = True
    return "".join(out).strip("-") or "item"

def esc(v): return html.escape(str(v))
def fmt(v, d=2):
    if v is None or (isinstance(v, float) and math.isnan(v)): return "N/D"
    return f"{float(v):,.{d}f}".replace(",","X").replace(".","," ).replace("X",".")
def ensure_dir(p): p.mkdir(parents=True, exist_ok=True)

def load_data(base_dir):
    enriched = base_dir/"data"/"dataset_with_indicators.csv"
    raw = base_dir/"data"/"dataset.csv"
    summary = base_dir/"data"/"indicators_summary_by_country.csv"
    questions = base_dir/"data"/"research_question_catalog.csv"
    df = pd.read_csv(enriched if enriched.exists() else raw)
    summary_df = pd.read_csv(summary) if summary.exists() else pd.DataFrame()
    questions_df = pd.read_csv(questions) if questions.exists() else pd.DataFrame()
    df["Año"] = pd.to_numeric(df["Año"], errors="raise").astype(int)
    return df.sort_values(["País","Año"]), summary_df, questions_df

def nav_html():
    return (
        '<nav class="navlinks">'
        '<a href="../../index.html">Inicio</a>'
        '<a href="../countries.html">Países</a>'
        '<a href="../years.html">Años</a>'
        '<a href="../indicators.html">Indicadores</a>'
        '<a href="../comparisons.html">Comparaciones</a>'
        '<a href="index.html">Preguntas de investigación</a>'
        '<a href="../about.html">Acerca del dataset</a>'
        f'<a href="{ZENODO_RECORD}">Zenodo</a>'
        '</nav>'
    )

def footer_html():
    return (
        '<div class="footer">'
        f'<p><strong>Autor:</strong> <a href="{AUTHOR_URL}">{AUTHOR_NAME}</a>'
        f' · <a href="{AUTHOR_ORCID}">ORCID</a>'
        f' · <a href="{RESEARCHGATE}">ResearchGate</a></p>'
        '<p><strong>Repositorios:</strong>'
        f' <a href="{DOI_DATASET}">Zenodo DOI</a>'
        f' · <a href="{ZENODO_RECORD}">Zenodo registro</a></p>'
        '</div>'
    )

def page_shell(title, description, keywords, canonical_url, body, ld_json):
    return (
        '<!doctype html>\n<html lang="es">\n<head>\n'
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'  <title>{esc(title)}</title>\n'
        f'  <meta name="description" content="{esc(description)}">\n'
        f'  <meta name="keywords" content="{esc(keywords)}">\n'
        '  <meta name="robots" content="index, follow">\n'
        f'  <link rel="canonical" href="{esc(canonical_url)}">\n'
        '  <meta property="og:type" content="article">\n'
        '  <meta property="og:locale" content="es_ES">\n'
        f'  <meta property="og:title" content="{esc(title)}">\n'
        f'  <meta property="og:url" content="{esc(canonical_url)}">\n'
        '  <link rel="stylesheet" href="../../assets/style.css">\n'
        '  <script defer src="../../assets/app.js"></script>\n'
        '  <style>\n'
        '    .rq-grid{display:grid;grid-template-columns:1.3fr .9fr;gap:20px}\n'
        '    .metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:14px}\n'
        '    .metric{background:#0d1324;border:1px solid #24314f;border-radius:16px;padding:14px}\n'
        '    .metric strong{display:block;color:#eef2ff;font-size:1.35rem}\n'
        '    .micro{color:#bcc7e7;font-size:.94rem}\n'
        '    .kicker{color:#c4f1be;text-transform:uppercase;letter-spacing:.04em;font-size:.92rem}\n'
        '    .cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:16px}\n'
        '    .btn-rq{display:inline-block;background:#1d4ed8;color:white;border-radius:999px;padding:10px 16px;font-weight:700;text-decoration:none}\n'
        '    .btn-rq.secondary{background:transparent;border:1px solid #24314f;color:#8ab4ff}\n'
        '    .btn-rq:hover{text-decoration:underline}\n'
        '    @media(max-width:900px){.rq-grid{grid-template-columns:1fr}}\n'
        '  </style>\n'
        '  <script type="application/ld+json">\n'
        f'{ld_json}\n'
        '  </script>\n'
        '</head>\n<body>\n<div class="wrap">\n'
        + nav_html() + "\n"
        + body + "\n"
        + footer_html() + "\n"
        '</div>\n</body>\n</html>'
    )

def build_page(df, summary_df, country):
    sub = df[df["País"]==country].sort_values("Año").copy()
    first, last = sub.iloc[0], sub.iloc[-1]
    sr = {}
    if not summary_df.empty and country in set(summary_df["País"]):
        sr = summary_df.loc[summary_df["País"]==country].iloc[0].to_dict()
    title = f"¿Cómo cambió la estructura por edades en {country} entre {int(first['Año'])} y {int(last['Año'])}?"
    slug = f"como-cambio-la-estructura-por-edades-en-{slugify(country)}-entre-{int(first['Año'])}-y-{int(last['Año'])}"
    desc = (f"Análisis demográfico de {country} entre {int(first['Año'])} y {int(last['Año'])} "
            "con interpretación científica, resultados, contexto, metodología, referencias y citación.")
    kw = ", ".join([f"estructura por edades {country}",f"envejecimiento poblacional {country}",
                    f"transición demográfica {country}",f"demografía {country}",
                    f"índice de envejecimiento {country}","análisis demográfico América Latina"])
    d65 = float(last["Pct_65_más"])-float(first["Pct_65_más"])
    d014 = float(last["Pct_0_14"])-float(first["Pct_0_14"])
    abstract = (f"Entre {int(first['Año'])} y {int(last['Año'])}, {country} experimentó un cambio en su composición por edades. "
                f"La población de 65 años o más pasó de {fmt(first['Pct_65_más'])}% a {fmt(last['Pct_65_más'])}%, mientras que la "
                f"de 0 a 14 años cambió de {fmt(first['Pct_0_14'])}% a {fmt(last['Pct_0_14'])}%.")
    context = (f"La estructura por edades resume la distribución relativa de la población. "
               f"En demografía, la reducción del peso de la infancia y el aumento del grupo de 65+ años "
               f"suelen asociarse con descensos de la fecundidad y avance de la transición demográfica.")
    results = (f"La proporción de 65+ cambió {fmt(d65)} pp. La de 0-14 cambió {fmt(d014)} pp. "
               f"El índice de envejecimiento pasó de {fmt(float(first['Indice_Envejecimiento']))} "
               f"a {fmt(float(last['Indice_Envejecimiento']))}. "
               f"Razón de dependencia total final: {fmt(float(last['Razon_Dependencia_Total']))}. "
               f"Categoría: {esc(sr.get('country_transition_type','transición demográfica observable'))}.")
    interp = (f"{country} ha desplazado su perfil demográfico hacia mayor presencia relativa de población mayor. "
              "Este patrón implica implicaciones para pensiones, atención sanitaria y capital humano.")
    method = (f"Datos del repositorio '{SITE_TITLE}' para {country}, periodos: "
              f"{', '.join(map(str,sub['Año'].tolist()))}. "
              "Los indicadores derivan de cocientes clásicos de envejecimiento y dependencia.")
    rows = "".join(
        f"<tr><td>{int(r['Año'])}</td><td>{fmt(r['Pct_0_14'])}</td><td>{fmt(r['Pct_15_24'])}</td>"
        f"<td>{fmt(r['Pct_25_54'])}</td><td>{fmt(r['Pct_55_64'])}</td><td>{fmt(r['Pct_65_más'])}</td>"
        f"<td>{fmt(r['Indice_Envejecimiento'])}</td><td>{fmt(r['Razon_Dependencia_Total'])}</td></tr>"
        for _,r in sub.iterrows()
    )
    refs = ("<ol><li>Bloom et al. (2003). The Demographic Dividend. RAND.</li>"
            "<li>Lee &amp; Mason (2011). Population Aging. Edward Elgar.</li>"
            "<li>UN DESA (2022). World Population Prospects 2022.</li>"
            f"<li>{esc(AUTHOR_NAME)} (2026). {esc(SITE_TITLE)}. Zenodo. "
            f'<a href="{esc(DOI_DATASET)}">{esc(DOI_DATASET)}</a></li></ol>')
    canon = f"{SITE_BASE_URL}/pages/research-questions/{slug}.html"
    country_url = f"../country-{slugify(country)}.html"
    ld = json.dumps({"@context":"https://schema.org","@type":"ScholarlyArticle",
                     "headline":title,"description":desc,"author":{"@type":"Person","name":AUTHOR_NAME},
                     "url":canon,"inLanguage":"es"},ensure_ascii=False,indent=2)
    body = (
        f'<section class="hero"><div class="kicker">Nota técnica demográfica citable</div>'
        f'<h1>{esc(title)}</h1><p>{esc(abstract)}</p>'
        f'<div class="cta-row">'
        f'<a class="btn-rq" href="{esc(DOI_DATASET)}">Ver DOI del dataset</a>'
        f'<a class="btn-rq secondary" href="{esc(country_url)}">Ver ficha del país</a>'
        f'<a class="btn-rq secondary" href="index.html">Todas las notas</a></div>'
        f'<div class="metric-grid">'
        f'<div class="metric"><span class="micro">% 65+ inicial</span><strong>{fmt(first["Pct_65_más"])}</strong></div>'
        f'<div class="metric"><span class="micro">% 65+ final</span><strong>{fmt(last["Pct_65_más"])}</strong></div>'
        f'<div class="metric"><span class="micro">% 0-14 inicial</span><strong>{fmt(first["Pct_0_14"])}</strong></div>'
        f'<div class="metric"><span class="micro">% 0-14 final</span><strong>{fmt(last["Pct_0_14"])}</strong></div>'
        f'<div class="metric"><span class="micro">Índice envejec. final</span><strong>{fmt(last["Indice_Envejecimiento"])}</strong></div>'
        f'<div class="metric"><span class="micro">Razón depend. final</span><strong>{fmt(last["Razon_Dependencia_Total"])}</strong></div>'
        f'</div></section>'
        f'<div class="rq-grid"><article>'
        f'<div class="section card"><h2>Resumen</h2><p>{esc(abstract)}</p></div>'
        f'<div class="section card"><h2>Contexto científico</h2><p>{esc(context)}</p></div>'
        f'<div class="section card"><h2>Resultados</h2><p>{esc(results)}</p>'
        f'<div style="overflow-x:auto"><table>'
        f'<thead><tr><th>Año</th><th>0-14%</th><th>15-24%</th><th>25-54%</th>'
        f'<th>55-64%</th><th>65+%</th><th>Índice</th><th>Depend.</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div></div>'
        f'<div class="section card"><h2>Interpretación</h2><p>{esc(interp)}</p></div>'
        f'<div class="section card"><h2>Metodología</h2><p>{esc(method)}</p></div>'
        f'</article><aside>'
        f'<div class="section card"><h2>Ficha técnica</h2><ul>'
        f'<li><strong>País:</strong> {esc(country)}</li>'
        f'<li><strong>Periodo:</strong> {int(first["Año"])}-{int(last["Año"])}</li>'
        f'<li><strong>URL:</strong> <a href="{esc(canon)}">{esc(canon)}</a></li>'
        f'</ul></div>'
        f'<div class="section card"><h2>Cómo citar</h2>'
        f'<p>{esc(AUTHOR_NAME)} (2026). {esc(title)}. En <em>{esc(SITE_TITLE)}</em>.'
        f' <a href="{esc(canon)}">{esc(canon)}</a></p></div>'
        f'<div class="section card"><h2>Referencias</h2>{refs}</div>'
        f'</aside></div>'
    )
    return {"slug":slug,"title":title,"description":desc,"keywords":kw,"canonical_url":canon,"body":body,"ld_json":ld}

def build_index_page(pages):
    title = "Preguntas de investigación demográfica: notas técnicas y análisis citables"
    desc = "Colección de notas técnicas demográficas con contexto, resultados, referencias y citación."
    canon = f"{SITE_BASE_URL}/pages/research-questions/index.html"
    kw = "preguntas investigación demográfica, notas técnicas, envejecimiento, transición demográfica"
    items = "".join(f'<li><a href="{esc(p["slug"])}.html">{esc(p["title"])}</a></li>' for p in pages)
    ld = json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":title,"url":canon},ensure_ascii=False,indent=2)
    body = (f'<section class="hero"><div class="kicker">Colección de notas técnicas</div>'
            f'<h1>{esc(title)}</h1>'
            f'<p>Cada página incorpora contexto científico, resultados, interpretación, metodología y bibliografía.</p>'
            f'</section><div class="section card"><h2>Análisis disponibles</h2><ul>{items}</ul></div>')
    return page_shell(title,desc,kw,canon,body,ld)

def main():
    base_dir = Path(__file__).resolve().parent.parent
    df, summary_df, questions_df = load_data(base_dir)
    output_dir = base_dir/"docs"/"pages"/"research-questions"
    ensure_dir(output_dir)
    pages = []
    if not questions_df.empty and "country_change" in set(questions_df.get("page_type",[])):
        for _,q in questions_df[questions_df["page_type"]=="country_change"].iterrows():
            p = build_page(df,summary_df,q["country_a"])
            (output_dir/f"{p['slug']}.html").write_text(
                page_shell(p["title"],p["description"],p["keywords"],p["canonical_url"],p["body"],p["ld_json"]),encoding="utf-8")
            pages.append(p)
    else:
        for country in sorted(df["País"].dropna().unique()):
            p = build_page(df,summary_df,country)
            (output_dir/f"{p['slug']}.html").write_text(
                page_shell(p["title"],p["description"],p["keywords"],p["canonical_url"],p["body"],p["ld_json"]),encoding="utf-8")
            pages.append(p)
    (output_dir/"index.html").write_text(build_index_page(pages),encoding="utf-8")
    print(f"OK: {len(pages)} páginas en {output_dir}")
    return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc: print(f"ERROR: {exc}",file=sys.stderr); raise