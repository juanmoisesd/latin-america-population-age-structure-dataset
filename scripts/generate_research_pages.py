#!/usr/bin/env python3
"""
generate_research_pages.py
--------------------------
Genera páginas de preguntas de investigación con estructura de mini-artículo:
- título indexable
- resumen / abstract
- contexto
- resultados
- interpretación
- metodología
- referencias
- citación
- SEO completo (description, keywords, canonical, OG, Twitter)
- JSON-LD tipo ScholarlyArticle

Entradas:
    data/dataset.csv
    data/dataset_with_indicators.csv
    data/indicators_summary_by_country.csv
    data/research_question_catalog.csv (si existe)

Salidas:
    docs/pages/research-questions/index.html
    docs/pages/research-questions/*.html
"""

from __future__ import annotations

import html
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

SITE_TITLE = "Latin America Population Age Structure Dataset"
SITE_BASE_URL = "https://juanmoisesd.github.io/latin-america-population-age-structure-dataset"
AUTHOR_NAME = "Juan Moisés de la Serna"
AUTHOR_ORCID = "https://orcid.org/0000-0002-8401-8018"
DOI_DATASET = "https://doi.org/10.5281/zenodo.18891177"


def slugify(text: str) -> str:
    replacements = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    text = text.translate(replacements).lower()
    out = []
    for ch in text:
        out.append(ch if ch.isalnum() else "-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def esc(value: object) -> str:
    return html.escape(str(value))


def fmt(value: float, decimals: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/D"
    return f"{float(value):,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_data(base_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    enriched = base_dir / "data" / "dataset_with_indicators.csv"
    raw = base_dir / "data" / "dataset.csv"
    summary = base_dir / "data" / "indicators_summary_by_country.csv"
    questions = base_dir / "data" / "research_question_catalog.csv"

    if enriched.exists():
        df = pd.read_csv(enriched)
    else:
        df = pd.read_csv(raw)

    summary_df = pd.read_csv(summary) if summary.exists() else pd.DataFrame()
    questions_df = pd.read_csv(questions) if questions.exists() else pd.DataFrame()

    df["Año"] = pd.to_numeric(df["Año"], errors="raise").astype(int)
    return df.sort_values(["País", "Año"]), summary_df, questions_df


def page_shell(title: str, description: str, keywords: str, canonical_url: str, body: str, ld_json: str) -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="keywords" content="{esc(keywords)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{esc(canonical_url)}">
<meta property="og:type" content="article">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="{esc(SITE_TITLE)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical_url)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<style>
:root {{
  --bg:#0b1120; --panel:#121a2f; --line:#24314f; --text:#eef2ff; --muted:#bcc7e7; --accent:#8ab4ff; --ok:#c4f1be;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:16px/1.68 Inter, Segoe UI, Arial, sans-serif; }}
a {{ color:var(--accent); text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
.container {{ max-width:1080px; margin:0 auto; padding:28px 20px 48px; }}
.hero, .panel {{
  background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:24px; margin-bottom:20px;
}}
.kicker {{ color:var(--ok); text-transform:uppercase; letter-spacing:.04em; font-size:.92rem; }}
h1, h2, h3 {{ line-height:1.2; }}
h1 {{ font-size:2rem; margin:.2rem 0 1rem; }}
h2 {{ font-size:1.4rem; margin:0 0 1rem; }}
p, li {{ color:var(--muted); }}
.grid {{ display:grid; grid-template-columns:1.3fr .9fr; gap:20px; }}
.metric-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; margin-top:14px; }}
.metric {{ background:#0d1324; border:1px solid var(--line); border-radius:16px; padding:14px; }}
.metric strong {{ display:block; color:var(--text); font-size:1.35rem; }}
table {{ width:100%; border-collapse:collapse; }}
th, td {{ text-align:left; border-bottom:1px solid var(--line); padding:10px 8px; }}
th {{ color:#dbe4ff; }}
.btn {{ display:inline-block; background:#1d4ed8; color:white; border-radius:999px; padding:10px 16px; font-weight:700; }}
.btn.secondary {{ background:transparent; border:1px solid var(--line); color:var(--accent); }}
.cta-row {{ display:flex; gap:12px; flex-wrap:wrap; margin-top:16px; }}
.micro {{ color:var(--muted); font-size:.94rem; }}
@media (max-width: 900px) {{
  .grid {{ grid-template-columns:1fr; }}
  h1 {{ font-size:1.7rem; }}
}}
</style>
<script type="application/ld+json">
{ld_json}
</script>
</head>
<body>
{body}
</body>
</html>"""


def build_country_change_question(df: pd.DataFrame, summary_df: pd.DataFrame, country: str) -> Dict[str, str]:
    sub = df[df["País"] == country].sort_values("Año").copy()
    first = sub.iloc[0]
    last = sub.iloc[-1]
    summary_row = {}
    if not summary_df.empty and country in set(summary_df["País"]):
        summary_row = summary_df.loc[summary_df["País"] == country].iloc[0].to_dict()

    title = f"¿Cómo cambió la estructura por edades en {country} entre {int(first['Año'])} y {int(last['Año'])}?"
    slug = f"como-cambio-la-estructura-por-edades-en-{slugify(country)}-entre-{int(first['Año'])}-y-{int(last['Año'])}"
    description = (
        f"Análisis demográfico de {country} entre {int(first['Año'])} y {int(last['Año'])} con interpretación científica, "
        f"resultados, contexto, metodología, referencias y citación."
    )
    keywords = ", ".join([
        f"estructura por edades {country}",
        f"envejecimiento poblacional {country}",
        f"transición demográfica {country}",
        f"demografía {country}",
        f"índice de envejecimiento {country}",
        "análisis demográfico América Latina",
    ])

    old_diff = float(last["Pct_65_más"]) - float(first["Pct_65_más"])
    young_diff = float(last["Pct_0_14"]) - float(first["Pct_0_14"])
    aging_start = float(first["Indice_Envejecimiento"])
    aging_end = float(last["Indice_Envejecimiento"])
    dep_end = float(last["Razon_Dependencia_Total"])

    abstract = (
        f"Entre {int(first['Año'])} y {int(last['Año'])}, {country} experimentó un cambio en su composición por edades. "
        f"La población de 65 años o más pasó de {fmt(first['Pct_65_más'])}% a {fmt(last['Pct_65_más'])}%, mientras que la "
        f"población de 0 a 14 años cambió de {fmt(first['Pct_0_14'])}% a {fmt(last['Pct_0_14'])}%. Estos resultados son "
        f"compatibles con un proceso de transición demográfica y aportan evidencia útil para interpretar cambios en dependencia, "
        f"envejecimiento y presión futura sobre servicios sociales."
    )

    context = (
        f"La estructura por edades resume la distribución relativa de la población entre cohortes jóvenes, potencialmente activas y mayores. "
        f"En demografía, la reducción del peso relativo de la infancia y el aumento del grupo de 65 años o más suelen asociarse con descensos "
        f"de la fecundidad, mejoras en supervivencia y avance de la transición demográfica. En este marco, analizar a {country} permite "
        f"observar la dirección y la intensidad del cambio demográfico dentro del contexto latinoamericano."
    )

    results = (
        f"Los resultados muestran que la proporción de población de 65 años o más cambió {fmt(old_diff)} puntos porcentuales en el periodo. "
        f"Al mismo tiempo, el grupo de 0 a 14 años cambió {fmt(young_diff)} puntos. El índice de envejecimiento pasó de {fmt(aging_start)} "
        f"a {fmt(aging_end)}, y la razón de dependencia total en el último año disponible fue de {fmt(dep_end)}. "
        f"En términos regionales, {country} se sitúa actualmente en la categoría de "
        f"{esc(summary_row.get('country_transition_type', 'transición demográfica observable'))}."
    )

    interpretation = (
        f"En conjunto, la evidencia sugiere que {country} ha desplazado gradualmente su perfil demográfico hacia una menor concentración "
        f"de población infantil y una mayor presencia relativa de población mayor. Desde una perspectiva analítica, este patrón puede "
        f"interpretarse como un avance en la transición demográfica, con implicaciones para pensiones, atención sanitaria, dependencia "
        f"y planificación del capital humano. La importancia de este hallazgo no radica solo en el cambio absoluto, sino en la velocidad "
        f"y consistencia del desplazamiento a lo largo del periodo."
    )

    methodology = (
        f"Se emplearon los datos del repositorio '{SITE_TITLE}', utilizando observaciones para {country} en {int(first['Año'])}, "
        f"{', '.join(map(str, sub['Año'].tolist()[1:-1])) + ', ' if len(sub) > 2 else ''}{int(last['Año'])}. "
        f"Los indicadores presentados derivan de la distribución por edades y de los cocientes clásicos de envejecimiento y dependencia. "
        f"La presente nota se generó automáticamente desde el pipeline reproducible del repositorio."
    )

    rows = []
    for _, row in sub.iterrows():
        rows.append(
            "<tr>"
            f"<td>{int(row['Año'])}</td>"
            f"<td>{fmt(row['Pct_0_14'])}</td>"
            f"<td>{fmt(row['Pct_15_24'])}</td>"
            f"<td>{fmt(row['Pct_25_54'])}</td>"
            f"<td>{fmt(row['Pct_55_64'])}</td>"
            f"<td>{fmt(row['Pct_65_más'])}</td>"
            f"<td>{fmt(row['Indice_Envejecimiento'])}</td>"
            f"<td>{fmt(row['Razon_Dependencia_Total'])}</td>"
            "</tr>"
        )

    references_html = (
        "<ol>"
        "<li>Bloom, D. E., Canning, D., & Sevilla, J. (2003). The Demographic Dividend. RAND.</li>"
        "<li>Lee, R., & Mason, A. (2011). Population Aging and the Generational Economy. Edward Elgar.</li>"
        "<li>United Nations, Department of Economic and Social Affairs. (2022). World Population Prospects 2022.</li>"
        f"<li>{esc(AUTHOR_NAME)} (2026). {esc(SITE_TITLE)}. Zenodo. <a href=\"{esc(DOI_DATASET)}\">{esc(DOI_DATASET)}</a></li>"
        "</ol>"
    )

    canonical_url = f"{SITE_BASE_URL}/pages/research-questions/{slug}.html"
    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": title,
        "description": description,
        "keywords": keywords,
        "author": {"@type": "Person", "name": AUTHOR_NAME, "identifier": AUTHOR_ORCID},
        "mainEntityOfPage": canonical_url,
        "url": canonical_url,
        "isPartOf": {"@type": "Dataset", "name": SITE_TITLE, "identifier": DOI_DATASET, "url": DOI_DATASET},
        "inLanguage": "es",
    }, ensure_ascii=False, indent=2)

    body = f"""
<main class="container">
  <section class="hero">
    <div class="kicker">Nota técnica demográfica citable</div>
    <h1>{esc(title)}</h1>
    <p>{esc(abstract)}</p>
    <div class="cta-row">
      <a class="btn" href="{esc(DOI_DATASET)}">Ver DOI del dataset</a>
      <a class="btn secondary" href="{SITE_BASE_URL}/pages/countries/{slugify(country)}.html">Ver ficha del país</a>
      <a class="btn secondary" href="{SITE_BASE_URL}/pages/research-questions/index.html">Todas las notas</a>
    </div>

    <div class="metric-grid">
      <div class="metric"><span class="micro">% 65+ inicial</span><strong>{fmt(first['Pct_65_más'])}</strong></div>
      <div class="metric"><span class="micro">% 65+ final</span><strong>{fmt(last['Pct_65_más'])}</strong></div>
      <div class="metric"><span class="micro">% 0–14 inicial</span><strong>{fmt(first['Pct_0_14'])}</strong></div>
      <div class="metric"><span class="micro">% 0–14 final</span><strong>{fmt(last['Pct_0_14'])}</strong></div>
      <div class="metric"><span class="micro">Índice envejecimiento final</span><strong>{fmt(last['Indice_Envejecimiento'])}</strong></div>
      <div class="metric"><span class="micro">Razón dependencia final</span><strong>{fmt(last['Razon_Dependencia_Total'])}</strong></div>
    </div>
  </section>

  <section class="grid">
    <article>
      <section class="panel">
        <h2>Resumen / Abstract</h2>
        <p>{esc(abstract)}</p>
      </section>

      <section class="panel">
        <h2>Contexto científico</h2>
        <p>{esc(context)}</p>
      </section>

      <section class="panel">
        <h2>Resultados</h2>
        <p>{esc(results)}</p>
        <div style="overflow-x:auto">
          <table>
            <thead>
              <tr>
                <th>Año</th>
                <th>% 0–14</th>
                <th>% 15–24</th>
                <th>% 25–54</th>
                <th>% 55–64</th>
                <th>% 65+</th>
                <th>Índice envejec.</th>
                <th>Razón dependencia</th>
              </tr>
            </thead>
            <tbody>
              {"".join(rows)}
            </tbody>
          </table>
        </div>
      </section>

      <section class="panel">
        <h2>Interpretación</h2>
        <p>{esc(interpretation)}</p>
      </section>

      <section class="panel">
        <h2>Metodología</h2>
        <p>{esc(methodology)}</p>
      </section>
    </article>

    <aside>
      <section class="panel">
        <h2>Ficha técnica</h2>
        <ul>
          <li><strong>País analizado:</strong> {esc(country)}</li>
          <li><strong>Periodo:</strong> {int(first['Año'])}–{int(last['Año'])}</li>
          <li><strong>Unidad de análisis:</strong> país-año</li>
          <li><strong>URL canónica:</strong> <a href="{esc(canonical_url)}">{esc(canonical_url)}</a></li>
          <li><strong>Dataset de base:</strong> <a href="{esc(DOI_DATASET)}">{esc(DOI_DATASET)}</a></li>
        </ul>
      </section>

      <section class="panel">
        <h2>Cómo citar</h2>
        <p>{esc(AUTHOR_NAME)} (2026). {esc(title)}. En <em>{esc(SITE_TITLE)}</em>. <a href="{esc(canonical_url)}">{esc(canonical_url)}</a></p>
      </section>

      <section class="panel">
        <h2>Referencias bibliográficas</h2>
        {references_html}
      </section>
    </aside>
  </section>
</main>
"""
    return {
        "slug": slug,
        "title": title,
        "description": description,
        "keywords": keywords,
        "canonical_url": canonical_url,
        "body": body,
        "ld_json": ld_json,
    }


def build_index_page(pages: List[Dict[str, str]]) -> str:
    title = "Preguntas de investigación demográfica: notas técnicas y análisis citables"
    description = "Colección de notas técnicas demográficas generadas a partir del dataset latinoamericano, con contexto, resultados, referencias y citación."
    canonical_url = f"{SITE_BASE_URL}/pages/research-questions/index.html"
    keywords = "preguntas de investigación demográfica, notas técnicas, envejecimiento poblacional, transición demográfica"

    items = "".join(
        f'<li><a href="{esc(page["slug"])}.html">{esc(page["title"])}</a> — análisis breve, resultados, interpretación y referencias.</li>'
        for page in pages
    )
    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": canonical_url,
        "about": SITE_TITLE,
    }, ensure_ascii=False, indent=2)
    body = f"""
<main class="container">
  <section class="hero">
    <div class="kicker">Colección de notas técnicas</div>
    <h1>{esc(title)}</h1>
    <p>Esta sección reúne preguntas de investigación reconvertidas en páginas de análisis demográfico citable. Cada una incorpora estructura de mini-artículo, contexto científico, resultados, interpretación, metodología y bibliografía.</p>
  </section>

  <section class="panel">
    <h2>Listado de análisis disponibles</h2>
    <ul>{items}</ul>
  </section>
</main>
"""
    return page_shell(title, description, keywords, canonical_url, body, ld_json)


def main() -> int:
    base_dir = Path(__file__).resolve().parent.parent
    df, summary_df, questions_df = load_data(base_dir)

    output_dir = base_dir / "docs" / "pages" / "research-questions"
    ensure_dir(output_dir)

    pages: List[Dict[str, str]] = []

    if not questions_df.empty and "country_change" in set(questions_df["page_type"]):
        for _, q in questions_df[questions_df["page_type"] == "country_change"].iterrows():
            country = q["country_a"]
            page = build_country_change_question(df, summary_df, country)
            html_output = page_shell(page["title"], page["description"], page["keywords"], page["canonical_url"], page["body"], page["ld_json"])
            (output_dir / f"{page['slug']}.html").write_text(html_output, encoding="utf-8")
            pages.append(page)
    else:
        for country in sorted(df["País"].dropna().unique()):
            page = build_country_change_question(df, summary_df, country)
            html_output = page_shell(page["title"], page["description"], page["keywords"], page["canonical_url"], page["body"], page["ld_json"])
            (output_dir / f"{page['slug']}.html").write_text(html_output, encoding="utf-8")
            pages.append(page)

    index_html = build_index_page(pages)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")

    print(f"OK: {output_dir / 'index.html'}")
    print(f"OK: páginas generadas en {output_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
