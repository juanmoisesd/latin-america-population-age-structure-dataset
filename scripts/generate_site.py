import pandas as pd
import os
import json
from jinja2 import Template
from datetime import datetime

def slugify(text):
    return text.lower().replace(' ', '_').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á', 'a').replace('ú', 'u').replace('ñ', 'n')

def get_header(level=0):
    p = "" if level == 0 else "../" if level == 1 else "../../"
    pages_p = "pages/" if level == 0 else "" if level == 1 else "../"
    return f"""
    <header>
        <div class="header-container">
            <h1><a href="{p}index.html" style="color: white; text-decoration: none;">LATAM Demográfico v6</a></h1>
            <nav>
                <a href="{p}index.html">Dashboard</a> | <a href="{pages_p}comparisons.html">Rankings</a> | <a href="{pages_p}indicators.html">Glosario</a>
            </nav>
        </div>
    </header>
    """

def get_citation_block(country=None):
    date = datetime.now().strftime("%Y-%m-%d")
    subject = f" - {country}" if country else ""
    return f"""
    <section class="citation-block">
        <h3>Cómo Citar / How to Cite</h3>
        <p>Para citar este recurso{subject}, utilice el siguiente formato:</p>
        <div class="citation-box">
            <strong>APA:</strong> de la Serna Tuya, J. M. (2026). <em>Estructura de Edad de la Población de América Latina 2000-2030{subject}</em> (Versión 6.0.0) [Conjunto de datos]. https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/<br><br>
            <strong>BibTeX:</strong><br>
            <code>@dataset{{delaserna2026{slugify(country) if country else 'regional'},<br>
            &nbsp;&nbsp;author = {{de la Serna Tuya, Juan Moisés}},<br>
            &nbsp;&nbsp;title = {{Estructura de Edad de la Población de América Latina 2000-2030{subject}}},<br>
            &nbsp;&nbsp;year = {{2026}},<br>
            &nbsp;&nbsp;url = {{https://juanmoisesd.github.io/latin-america-population-age-structure-dataset/}}<br>
            }}</code>
        </div>
        <p><small>Accedido el: {date}</small></p>
    </section>
    """

def get_footer():
    return """
    <footer>
        <div class="footer-container">
            <p>© 2026 Juan Moisés de la Serna Tuya. <a href="https://github.com/juanmoisesd/latin-america-population-age-structure-dataset">GitHub</a> | <a href="/docs/api/">JSON API</a></p>
        </div>
    </footer>
    """

BASE_STYLE = """
<style>
    :root { --primary: #1a2a6c; --secondary: #b21f1f; --accent: #fdbb2d; --bg: #f4f7f6; --text: #2d3436; }
    body { font-family: 'Inter', system-ui, sans-serif; line-height: 1.6; margin: 0; color: var(--text); background: var(--bg); }
    .header-container, .footer-container, main { max-width: 1200px; margin: auto; padding: 0 20px; }
    header { background: linear-gradient(to right, #1a2a6c, #b21f1f, #fdbb2d); color: #fff; padding: 30px 0; }
    nav a { color: #fff; margin: 0 15px; text-decoration: none; font-weight: bold; }
    .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }
    .stat-card { background: #fff; padding: 25px; border-radius: 16px; box-shadow: 0 10px 15px rgba(0,0,0,0.05); text-align: center; border-bottom: 4px solid var(--accent); }
    .stat-card h3 { margin: 10px 0; color: var(--primary); font-size: 2.5em; }
    section { margin: 50px 0; padding: 30px; background: #fff; border-radius: 16px; box-shadow: 0 10px 15px rgba(0,0,0,0.05); }
    .citation-block { background: #f9f9f9; border-left: 5px solid var(--primary); }
    .citation-box { background: #eee; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 0.9em; margin-top: 10px; }
    .country-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; }
    .country-link { display: block; padding: 15px; background: #fff; border-radius: 10px; text-decoration: none; color: var(--primary); font-weight: 600; text-align: center; }
    .country-link:hover { background: var(--primary); color: #fff; }
    footer { background: #2d3436; color: white; padding: 40px 0; text-align: center; margin-top: 80px; }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
"""

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    with open('docs/api/narratives.json', 'r', encoding='utf-8') as f:
        narratives = json.load(f)
    os.makedirs('docs/pages/countries', exist_ok=True)
    countries = sorted(df['País'].unique())

    total_pop_2023 = round(df[df['Año'] == 2023]['Pob_Total_Millones'].sum(), 1)
    avg_ev_2023 = round(df[df['Año'] == 2023]['Esperanza_Vida'].mean(), 1)

    index_tpl = Template(f"""
    <!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dashboard LATAM</title>{BASE_STYLE}</head><body>{get_header(0)}
    <main>
        <section class="dashboard-grid">
            <div class="stat-card"><h3>{{{{ total_pop }}}}M</h3><p>Población Regional (2023)</p></div>
            <div class="stat-card"><h3>{{{{ avg_ev }}}}</h3><p>Exp. Vida Promedio</p></div>
        </section>
        <section>
            <h2>Explorar Naciones</h2>
            <div class="country-grid">
                {{% for c in countries %}}<a href="pages/countries/{{{{ slugs[c] }}}}.html" class="country-link">{{{{ c }}}}</a>{{% endfor %}}
            </div>
        </section>
        {get_citation_block()}
    </main>
    {get_footer()}</body></html>""")

    country_tpl = Template(f"""
    <!DOCTYPE html><html><head><meta charset='UTF-8'><title>{{{{ country }}}}</title>{BASE_STYLE}</head><body>{get_header(2)}
    <main>
        <section>
            <h2>{{{{ country }}}}</h2>
            <p><em>"{{{{ narrative }}}}"</em></p>
            <div class="dashboard-grid">
                <div class="stat-card"><h3>{{{{ pop2023 }}}}M</h3><p>Población</p></div>
                <div class="stat-card"><h3>{{{{ ev2023 }}}}</h3><p>Exp. Vida</p></div>
            </div>
        </section>
        <section><h3>Crecimiento y Estructura</h3><canvas id="popChart"></canvas></section>
        {{{{ citation_block }}}}
    </main>
    <script>
    new Chart(document.getElementById('popChart'), {{
        type: 'line',
        data: {{
            labels: {list(range(2000, 2031))},
            datasets: [{{ label: 'Población (M)', data: {{{{ pop_data }}}}, borderColor: '#b21f1f', tension: 0.3 }}]
        }}
    }});
    </script>
    {get_footer()}</body></html>""")

    with open('docs/index.html', 'w') as f:
        f.write(index_tpl.render(total_pop=total_pop_2023, avg_ev=avg_ev_2023, countries=countries, slugs={c: slugify(c) for c in countries}))

    for c in countries:
        c_df = df[df['País'] == c].sort_values('Año')
        r23 = c_df[c_df['Año'] == 2023].iloc[0]
        with open(f'docs/pages/countries/{slugify(c)}.html', 'w') as f:
            f.write(country_tpl.render(
                country=c, pop2023=r23.Pob_Total_Millones, ev2023=r23.Esperanza_Vida,
                narrative=narratives.get(c, ""), pop_data=c_df.Pob_Total_Millones.tolist(),
                citation_block=get_citation_block(c)
            ))

    print("Academic citation features integrated.")

if __name__ == "__main__": main()
