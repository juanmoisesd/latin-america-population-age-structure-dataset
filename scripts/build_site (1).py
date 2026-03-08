#!/usr/bin/env python3
"""
build_site.py
-------------
Genera páginas completas y SEO-friendly por país, con:
- título y resumen ejecutivo
- ficha técnica
- interpretación científica
- indicadores clave
- comparaciones sugeridas
- referencias bibliográficas
- JSON-LD para indexación
- metadatos Open Graph / Twitter / canonical
- enlaces internos y bloques de citación

Entradas:
    data/dataset.csv
    data/dataset_with_indicators.csv (preferente)
    data/indicators_summary_by_country.csv

Salidas principales:
    docs/pages/countries/index.html
    docs/pages/countries/<country-slug>.html
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


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def esc(value: object) -> str:
    return html.escape(str(value))


def fmt(value: float, decimals: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/D"
    return f"{float(value):,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def load_enriched_data(base_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    enriched = base_dir / "data" / "dataset_with_indicators.csv"
    raw = base_dir / "data" / "dataset.csv"
    summary = base_dir / "data" / "indicators_summary_by_country.csv"

    if enriched.exists():
        df = pd.read_csv(enriched)
    else:
        df = pd.read_csv(raw)

    if summary.exists():
        summary_df = pd.read_csv(summary)
    else:
        summary_df = pd.DataFrame()

    df["Año"] = pd.to_numeric(df["Año"], errors="raise").astype(int)
    return df.sort_values(["País", "Año"]), summary_df


def country_neighbors(summary_df: pd.DataFrame, country: str, top_n: int = 3) -> List[str]:
    if summary_df.empty or country not in set(summary_df["País"]):
        return []

    row = summary_df.loc[summary_df["País"] == country].iloc[0]
    candidates = summary_df.copy()
    candidates = candidates[candidates["País"] != country].copy()
    candidates["distance"] = (
        (candidates["Indice_Envejecimiento"] - row["Indice_Envejecimiento"]).abs() +
        (candidates["Razon_Dependencia_Total"] - row["Razon_Dependencia_Total"]).abs() +
        (candidates["Pct_0_14"] - row["Pct_0_14"]).abs()
    )
    return candidates.sort_values("distance").head(top_n)["País"].tolist()


def build_country_keywords(country: str) -> str:
    keywords = [
        f"estructura por edades {country}",
        f"envejecimiento poblacional {country}",
        f"transición demográfica {country}",
        f"índice de envejecimiento {country}",
        f"demografía {country}",
        f"población {country} 2000 2023",
        f"pirámide poblacional {country}",
        "Latin America demographic dataset",
        "demographic transition Latin America",
    ]
    return ", ".join(keywords)


def build_country_title(country: str) -> str:
    return f"{country}: estructura por edades, envejecimiento y transición demográfica (2000–2023)"


def build_country_description(sub: pd.DataFrame) -> str:
    first = sub.iloc[0]
    last = sub.iloc[-1]
    return (
        f"Ficha técnica y análisis demográfico de {last['País']} entre {int(first['Año'])} y {int(last['Año'])}. "
        f"Incluye indicadores de envejecimiento, dependencia, interpretación científica, referencias y cómo citar."
    )


def build_intro(sub: pd.DataFrame) -> str:
    first = sub.iloc[0]
    last = sub.iloc[-1]
    return (
        f"Esta página presenta una ficha técnica ampliada sobre la evolución de la estructura por edades de "
        f"{last['País']} entre {int(first['Año'])} y {int(last['Año'])}. El objetivo es ofrecer una lectura "
        f"científica, clara y citable del cambio demográfico, integrando resultados cuantitativos, contexto "
        f"demográfico, implicaciones y bibliografía básica."
    )


def build_scientific_interpretation(sub: pd.DataFrame, summary_row: Dict[str, object]) -> str:
    first = sub.iloc[0]
    last = sub.iloc[-1]
    old_diff = float(last["Pct_65_más"]) - float(first["Pct_65_más"])
    young_diff = float(last["Pct_0_14"]) - float(first["Pct_0_14"])
    aging_start = float(first["Indice_Envejecimiento"])
    aging_end = float(last["Indice_Envejecimiento"])
    transition_type = summary_row.get("country_transition_type", "transición demográfica")
    priority_type = summary_row.get("country_priority_type", "presión demográfica")

    return (
        f"Entre {int(first['Año'])} y {int(last['Año'])}, {last['País']} pasó por un proceso compatible con una "
        f"{transition_type}. La población de 65 años o más aumentó {fmt(old_diff, 2)} puntos porcentuales, "
        f"mientras que el grupo de 0 a 14 años cambió {fmt(young_diff, 2)} puntos. En conjunto, esta pauta es "
        f"consistente con un descenso relativo del peso de la infancia y un aumento gradual de la población mayor, "
        f"dos rasgos clásicos de la transición demográfica. El índice de envejecimiento pasó de {fmt(aging_start)} "
        f"a {fmt(aging_end)}, y en el último año disponible el país mostró una situación de {priority_type}. "
        f"Desde una perspectiva analítica, el patrón observado sugiere un cambio relevante en la relación entre "
        f"cohortes dependientes y población potencialmente activa."
    )


def build_implications(sub: pd.DataFrame) -> str:
    last = sub.iloc[-1]
    dependency = float(last["Razon_Dependencia_Total"])
    old_pct = float(last["Pct_65_más"])
    young_pct = float(last["Pct_0_14"])

    pieces = [
        "En términos de política pública, la evolución observada tiene implicaciones para la planificación sanitaria, educativa y previsional."
    ]
    if old_pct >= 10:
        pieces.append(
            "El peso relativamente más alto de la población mayor apunta a una creciente importancia de los servicios sanitarios, la atención de largo plazo y las pensiones."
        )
    if young_pct >= 30:
        pieces.append(
            "La persistencia de una población infantil amplia sigue exigiendo inversión sostenida en educación, vacunación, nutrición y empleo futuro."
        )
    if dependency >= 55:
        pieces.append(
            "La razón de dependencia total relativamente elevada sugiere presión sobre la población en edad potencialmente activa."
        )
    else:
        pieces.append(
            "La razón de dependencia total moderada sugiere una ventana demográfica comparativamente más favorable que en países más envejecidos."
        )
    return " ".join(pieces)


def build_methodology(country: str) -> str:
    return (
        f"Los resultados se derivan del dataset '{SITE_TITLE}', con observaciones por país y año. "
        f"Se utilizaron grupos de edad de 0–14, 15–24, 25–54, 55–64 y 65 años o más. El índice de envejecimiento "
        f"se calculó como la razón entre la población de 65 años o más y la población de 0 a 14 años, multiplicada por 100. "
        f"La razón de dependencia total se calculó como el cociente entre la población dependiente "
        f"(0–14 y 65+) y la población de 15 a 64 años, multiplicado por 100. Esta ficha técnica se ha generado "
        f"automáticamente para {country} a partir del repositorio reproducible asociado."
    )


def build_references_html() -> str:
    refs = [
        "Bloom, D. E., Canning, D., & Sevilla, J. (2003). The Demographic Dividend: A New Perspective on the Economic Consequences of Population Change. RAND.",
        "Lee, R., & Mason, A. (2011). Population Aging and the Generational Economy: A Global Perspective. Edward Elgar.",
        "United Nations, Department of Economic and Social Affairs. (2022). World Population Prospects 2022.",
        "Comisión Económica para América Latina y el Caribe (CEPAL). Panorama Demográfico de América Latina y el Caribe.",
        f"de la Serna, J. M. (2026). {SITE_TITLE}. Zenodo. {DOI_DATASET}",
    ]
    return "<ol>" + "".join(f"<li>{esc(ref)}</li>" for ref in refs) + "</ol>"


def build_metrics_cards(last: pd.Series, summary_row: Dict[str, object]) -> str:
    cards = [
        ("Población total (millones)", fmt(last["Población_Total_Millones"])),
        ("% población 0–14", fmt(last["Pct_0_14"])),
        ("% población 65+", fmt(last["Pct_65_más"])),
        ("Índice de envejecimiento", fmt(last["Indice_Envejecimiento"])),
        ("Razón de dependencia", fmt(last["Razon_Dependencia_Total"])),
        ("Ranking regional de envejecimiento", str(summary_row.get("Ranking_Envejecimiento_Regional", "N/D"))),
    ]
    html_cards = []
    for label, value in cards:
        html_cards.append(
            f'<div class="metric-card"><div class="metric-value">{esc(value)}</div><div class="metric-label">{esc(label)}</div></div>'
        )
    return "".join(html_cards)


def build_table(sub: pd.DataFrame) -> str:
    rows = []
    for _, row in sub.iterrows():
        rows.append(
            "<tr>"
            f"<td>{int(row['Año'])}</td>"
            f"<td>{fmt(row['Población_Total_Millones'])}</td>"
            f"<td>{fmt(row['Pct_0_14'])}</td>"
            f"<td>{fmt(row['Pct_15_24'])}</td>"
            f"<td>{fmt(row['Pct_25_54'])}</td>"
            f"<td>{fmt(row['Pct_55_64'])}</td>"
            f"<td>{fmt(row['Pct_65_más'])}</td>"
            f"<td>{fmt(row['Indice_Envejecimiento'])}</td>"
            f"<td>{fmt(row['Razon_Dependencia_Total'])}</td>"
            "</tr>"
        )
    return "".join(rows)


def build_cross_links(country: str, neighbors: List[str]) -> str:
    if not neighbors:
        return "<p>No se encontraron países comparables con los datos actuales.</p>"
    items = []
    for item in neighbors:
        slug = slugify(item)
        items.append(
            f'<li><a href="{slug}.html">{esc(item)}</a> — perfil comparativamente próximo en envejecimiento, dependencia y peso de la población joven.</li>'
        )
    return "<ul>" + "".join(items) + "</ul>"


def json_ld_for_country(country: str, canonical_url: str, description: str, keywords: str) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": build_country_title(country),
        "description": description,
        "keywords": keywords,
        "author": {
            "@type": "Person",
            "name": AUTHOR_NAME,
            "identifier": AUTHOR_ORCID,
        },
        "publisher": {
            "@type": "Organization",
            "name": "GitHub Pages / Zenodo",
        },
        "mainEntityOfPage": canonical_url,
        "url": canonical_url,
        "isPartOf": {
            "@type": "Dataset",
            "name": SITE_TITLE,
            "identifier": DOI_DATASET,
            "url": DOI_DATASET,
        },
        "inLanguage": "es",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def page_shell(title: str, description: str, keywords: str, canonical_url: str, body: str, ld_json: str) -> str:
    og_title = esc(title)
    og_desc = esc(description)
    canonical = esc(canonical_url)
    kw = esc(keywords)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{og_title}</title>
<meta name="description" content="{og_desc}">
<meta name="keywords" content="{kw}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="{esc(SITE_TITLE)}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_desc}">
<style>
:root {{
  --bg: #0d1321;
  --panel: #151d31;
  --text: #eef2ff;
  --muted: #b6c1dd;
  --accent: #8ab4ff;
  --accent2: #c7d2fe;
  --line: #24314f;
  --ok: #c4f1be;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: #0b1120; color: var(--text);
  font: 16px/1.65 Inter, Segoe UI, Arial, sans-serif;
}}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.container {{ max-width: 1180px; margin: 0 auto; padding: 28px 20px 48px; }}
.hero {{
  background: linear-gradient(180deg, #121a2f 0%, #0f1728 100%);
  border: 1px solid var(--line); border-radius: 22px; padding: 28px; margin-bottom: 22px;
}}
.kicker {{ color: var(--ok); font-size: .92rem; letter-spacing: .04em; text-transform: uppercase; }}
h1, h2, h3 {{ line-height: 1.2; margin: 0 0 14px; }}
h1 {{ font-size: 2rem; }}
h2 {{ font-size: 1.45rem; margin-top: 28px; }}
p, li {{ color: var(--muted); }}
.metrics {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px; margin-top: 18px;
}}
.metric-card {{
  background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 16px;
}}
.metric-value {{ font-size: 1.45rem; font-weight: 800; color: var(--text); }}
.metric-label {{ color: var(--muted); font-size: .95rem; }}
.panel {{
  background: var(--panel); border: 1px solid var(--line); border-radius: 20px; padding: 22px; margin: 20px 0;
}}
.grid-2 {{
  display: grid; grid-template-columns: 1.35fr .95fr; gap: 20px;
}}
table {{ width: 100%; border-collapse: collapse; font-size: .95rem; }}
th, td {{ border-bottom: 1px solid var(--line); text-align: left; padding: 10px 8px; vertical-align: top; }}
th {{ color: var(--accent2); }}
small, .micro {{ color: var(--muted); }}
.cta-row {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }}
.btn {{
  display: inline-block; border-radius: 999px; padding: 10px 16px; font-weight: 700;
  background: #1d4ed8; color: white; border: 1px solid #1d4ed8;
}}
.btn.secondary {{ background: transparent; color: var(--accent); border-color: var(--line); }}
footer {{ margin-top: 34px; color: var(--muted); font-size: .95rem; }}
@media (max-width: 900px) {{
  .grid-2 {{ grid-template-columns: 1fr; }}
  h1 {{ font-size: 1.7rem; }}
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


def build_country_page(country: str, sub: pd.DataFrame, summary_df: pd.DataFrame) -> str:
    sub = sub.sort_values("Año").copy()
    first = sub.iloc[0]
    last = sub.iloc[-1]
    summary_row = {}
    if not summary_df.empty and country in set(summary_df["País"]):
        summary_row = summary_df.loc[summary_df["País"] == country].iloc[0].to_dict()

    title = build_country_title(country)
    description = build_country_description(sub)
    keywords = build_country_keywords(country)
    slug = slugify(country)
    canonical_url = f"{SITE_BASE_URL}/pages/countries/{slug}.html"
    neighbors = country_neighbors(summary_df, country, top_n=4)

    body = f"""
<main class="container">
  <section class="hero">
    <div class="kicker">Ficha técnica demográfica citable</div>
    <h1>{esc(title)}</h1>
    <p>{esc(build_intro(sub))}</p>
    <div class="cta-row">
      <a class="btn" href="{esc(DOI_DATASET)}">Ver DOI del dataset</a>
      <a class="btn secondary" href="{SITE_BASE_URL}/pages/countries/index.html">Índice de países</a>
      <a class="btn secondary" href="{SITE_BASE_URL}/pages/research-questions/index.html">Preguntas de investigación</a>
    </div>
    <div class="metrics">{build_metrics_cards(last, summary_row)}</div>
  </section>

  <section class="grid-2">
    <article class="panel">
      <h2>Resumen ejecutivo</h2>
      <p>{esc(summary_row.get("country_summary_long", build_scientific_interpretation(sub, summary_row)))}</p>

      <h2>Lectura científica</h2>
      <p>{esc(build_scientific_interpretation(sub, summary_row))}</p>

      <h2>Serie temporal de indicadores</h2>
      <div style="overflow-x:auto">
      <table>
        <thead>
          <tr>
            <th>Año</th>
            <th>Población total</th>
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
          {build_table(sub)}
        </tbody>
      </table>
      </div>

      <h2>Implicaciones</h2>
      <p>{esc(build_implications(sub))}</p>

      <h2>Metodología</h2>
      <p>{esc(build_methodology(country))}</p>
    </article>

    <aside>
      <section class="panel">
        <h2>Ficha técnica</h2>
        <ul>
          <li><strong>País:</strong> {esc(country)}</li>
          <li><strong>Periodo cubierto:</strong> {int(first['Año'])}–{int(last['Año'])}</li>
          <li><strong>Unidad de análisis:</strong> país-año</li>
          <li><strong>Último año disponible:</strong> {int(last['Año'])}</li>
          <li><strong>Fuente declarada:</strong> {esc(last['Fuente'])}</li>
          <li><strong>Licencia y citación:</strong> ver DOI del dataset</li>
          <li><strong>URL canónica:</strong> <a href="{esc(canonical_url)}">{esc(canonical_url)}</a></li>
        </ul>
      </section>

      <section class="panel">
        <h2>Indicadores destacados</h2>
        <ul>
          <li><strong>Índice de envejecimiento:</strong> {fmt(last['Indice_Envejecimiento'])}</li>
          <li><strong>Razón de dependencia total:</strong> {fmt(last['Razon_Dependencia_Total'])}</li>
          <li><strong>Población joven (0–14):</strong> {fmt(last['Pct_0_14'])}%</li>
          <li><strong>Población mayor (65+):</strong> {fmt(last['Pct_65_más'])}%</li>
          <li><strong>Bono demográfico:</strong> {fmt(last['Indice_Bono_Demografico'], 4)}</li>
        </ul>
      </section>

      <section class="panel">
        <h2>Países relacionados</h2>
        <p class="micro">Sugerencias automáticas basadas en similitud regional de envejecimiento, dependencia y peso relativo de la población joven.</p>
        {build_cross_links(country, neighbors)}
      </section>

      <section class="panel">
        <h2>Cómo citar</h2>
        <p class="micro">Cita sugerida de esta página:</p>
        <p>{esc(AUTHOR_NAME)} (2026). {esc(title)}. En <em>{esc(SITE_TITLE)}</em>. <a href="{esc(canonical_url)}">{esc(canonical_url)}</a></p>
        <p class="micro">Cita del dataset madre:</p>
        <p>{esc(AUTHOR_NAME)} (2026). {esc(SITE_TITLE)}. Zenodo. <a href="{esc(DOI_DATASET)}">{esc(DOI_DATASET)}</a></p>
      </section>
    </aside>
  </section>

  <section class="panel">
    <h2>Referencias bibliográficas</h2>
    {build_references_html()}
  </section>

  <footer>
    <p>Contenido generado automáticamente a partir del dataset demográfico regional. Esta página está optimizada para indexación, enlazado interno, citación académica y reutilización documental.</p>
  </footer>
</main>
"""
    return page_shell(title, description, keywords, canonical_url, body, json_ld_for_country(country, canonical_url, description, keywords))


def build_index_page(countries: List[str]) -> str:
    canonical_url = f"{SITE_BASE_URL}/pages/countries/index.html"
    title = "Países de América Latina: fichas técnicas demográficas y análisis citable"
    description = "Índice de fichas técnicas demográficas por país con análisis, indicadores, referencias y metadatos preparados para indexación."
    keywords = "países América Latina demografía, fichas técnicas demográficas, envejecimiento poblacional, transición demográfica"

    items = "".join(
        f'<li><a href="{slugify(country)}.html">{esc(country)}</a> — perfil demográfico, transición por edades, indicadores y referencias.</li>'
        for country in countries
    )
    body = f"""
<main class="container">
  <section class="hero">
    <div class="kicker">Índice científico por país</div>
    <h1>{esc(title)}</h1>
    <p>Esta sección reúne fichas técnicas completas y citables para cada país incluido en el dataset regional. Cada página incorpora contexto, resultados, interpretación, referencias y orientación de citación.</p>
  </section>

  <section class="panel">
    <h2>Listado de países</h2>
    <ul>{items}</ul>
  </section>
</main>
"""
    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": canonical_url,
        "about": SITE_TITLE,
    }, ensure_ascii=False, indent=2)
    return page_shell(title, description, keywords, canonical_url, body, ld_json)


def main() -> int:
    base_dir = Path(__file__).resolve().parent.parent
    df, summary_df = load_enriched_data(base_dir)

    countries_dir = base_dir / "docs" / "pages" / "countries"
    ensure_dir(countries_dir)

    countries = sorted(df["País"].dropna().unique())
    for country in countries:
        sub = df[df["País"] == country].copy()
        output = countries_dir / f"{slugify(country)}.html"
        output.write_text(build_country_page(country, sub, summary_df), encoding="utf-8")

    index_file = countries_dir / "index.html"
    index_file.write_text(build_index_page(countries), encoding="utf-8")

    print(f"OK: {index_file}")
    print(f"OK: páginas de países generadas en {countries_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
