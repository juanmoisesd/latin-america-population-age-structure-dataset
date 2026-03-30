import pandas as pd
import os
from jinja2 import Template

def slugify(text):
    return text.lower().replace(' ', '_').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á', 'a').replace('ú', 'u').replace('ñ', 'n')

def get_header(level=0):
    p = "" if level == 0 else "../" if level == 1 else "../../"
    pages_p = "pages/" if level == 0 else "" if level == 1 else "../"
    return f"""
    <header>
        <div class="header-container">
            <h1><a href="{p}index.html" style="color: white; text-decoration: none;">América Latina Demográfica</a></h1>
            <nav>
                <a href="{p}index.html">Inicio</a> |
                <a href="{p}index.html#countries">Países</a> |
                <a href="{pages_p}years.html">Años</a> |
                <a href="{pages_p}indicators.html">Indicadores</a> |
                <a href="{pages_p}comparisons.html">Comparativas</a>
            </nav>
        </div>
    </header>
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
    :root { --primary: #2c3e50; --secondary: #34495e; --accent: #1abc9c; --bg: #ecf0f1; --text: #333; }
    body { font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; margin: 0; padding: 0; color: var(--text); background: var(--bg); }
    .header-container, .footer-container, main { max-width: 1200px; margin: auto; padding: 0 20px; }
    header { background: var(--primary); color: #fff; padding: 20px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
    nav a { color: #ecf0f1; margin: 0 10px; text-decoration: none; font-weight: 600; }
    nav a:hover { color: var(--accent); }
    section { margin: 40px 0; padding: 30px; background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    h2 { border-left: 5px solid var(--accent); padding-left: 15px; color: var(--primary); }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
    .card { padding: 20px; border: 1px solid #ddd; border-radius: 8px; transition: transform 0.2s; background: white; }
    .card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    img { max-width: 100%; height: auto; border-radius: 8px; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.9em; }
    th, td { border-bottom: 1px solid #ddd; padding: 12px; text-align: left; }
    th { background: var(--secondary); color: white; }
    tr:hover { background: #f5f5f5; }
    .btn { display: inline-block; padding: 10px 20px; background: var(--accent); color: white; border-radius: 5px; text-decoration: none; font-weight: bold; }
    .search-container { margin-bottom: 20px; }
    #search-box { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #ddd; font-size: 1.1em; }
    footer { background: var(--primary); color: white; padding: 30px 0; margin-top: 60px; text-align: center; }
    .meta-tags { visibility: hidden; position: absolute; }
</style>
"""

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    os.makedirs('docs/pages/countries', exist_ok=True)
    countries = sorted(df['País'].unique())
    country_slugs = {c: slugify(c) for c in countries}

    # API and per-country CSV
    os.makedirs('docs/api', exist_ok=True)
    for country in countries:
        c_df = df[df['País'] == country].sort_values('Año')
        c_df.to_csv(f"docs/api/{country_slugs[country]}.csv", index=False)

    # index.html
    index_tpl = Template(f"""
    <!DOCTYPE html><html><head><meta charset='UTF-8'><title>Portal Demográfico América Latina 2030</title>{BASE_STYLE}</head><body>{get_header(0)}
    <main><section><h2>Explora América Latina</h2><p>Análisis y proyecciones de 19 países hasta 2030.</p>
    <div class="search-container"><input type="text" id="search-box" placeholder="Buscar país..." onkeyup="filterCountries()"></div>
    <div id='countries' class='grid'>{{% for c in countries %}}
    <div class='card country-card' data-name='{{{{ c }}}}'><h3>{{{{ c }}}}</h3><a href='pages/countries/{{{{ country_slugs[c] }}}}.html' class='btn'>Ver Perfil</a></div>
    {{% endfor %}}</div></section></main>
    <script>
    function filterCountries() {{
        let input = document.getElementById('search-box').value.toLowerCase();
        let cards = document.getElementsByClassName('country-card');
        for (let card of cards) {{
            let name = card.getAttribute('data-name').toLowerCase();
            card.style.display = name.includes(input) ? "block" : "none";
        }}
    }}
    </script>
    {get_footer()}</body></html>""")

    # country.html
    country_tpl = Template(f"""
    <!DOCTYPE html><html><head><meta charset='UTF-8'><title>{{{{ country }}}}</title>{BASE_STYLE}</head><body>{get_header(2)}
    <main><section><h2>{{{{ country }}}} ({{{{ iso3 }}}})</h2>
    <div style="margin-bottom: 20px;">
        <a href="../../api/{{{{ slug }}}}.csv" class="btn">Descargar CSV</a>
        <a href="../../api/{{{{ slug }}}}.json" class="btn" style="background: #3498db;">Ver JSON</a>
    </div>
    <div class='grid'>
        <div><h3>Estructura de Edad</h3><img src='../../assets/pyramid_{{{{ slug }}}}_2023.png'></div>
        <div><h3>Dinámica de Grupos</h3><img src='../../assets/evolution_groups_{{{{ slug }}}}.png'></div>
    </div>
    <div class='grid' style='margin-top: 20px;'>
        <div><h3>Tendencias de Dependencia</h3><img src='../../assets/dependency_{{{{ slug }}}}.png'></div>
        <div><h3>Ficha Técnica</h3><ul><li>Esperanza Vida (2023): {{{{ ev2023 }}}} años</li><li>Edad Mediana (2023): {{{{ em2023 }}}} años</li><li>Estado: {{{{ transition }}}}</li></ul></div>
    </div>
    </section>
    <section><h3>Histórico y Proyecciones</h3><table><thead><tr><th>Año</th><th>Pob (M)</th><th>Dependencia (%)</th><th>Esp. Vida</th><th>Urb (%)</th></tr></thead><tbody>
    {{% for r in rows %}}<tr><td>{{{{ r.Año }}}}</td><td>{{{{ r.Pob_Total_Millones }}}}</td><td>{{{{ r.Tasa_Dependencia_Total }}}}</td><td>{{{{ r.Esperanza_Vida }}}}</td><td>{{{{ r.Tasa_Urbanización }}}}</td></tr>{{% endfor %}}
    </tbody></table></section></main>{get_footer()}</body></html>""")

    # Indicators...
    # Comparisons... (with new charts)
    comparisons_tpl = Template(f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Comparativas</title>{BASE_STYLE}</head><body>{get_header(1)}<main><section><h2>Comparativas Regionales</h2><div class='grid'><img src='../assets/dependency_trend.png'><img src='../assets/life_expectancy_trend.png'><img src='../assets/urbanization_aging_scatter.png'><img src='../assets/demographic_bonus_trend.png'></div></section></main>{get_footer()}</body></html>")

    # Generate index
    with open('docs/index.html', 'w') as f: f.write(index_tpl.render(countries=countries, country_slugs=country_slugs))
    with open('docs/pages/comparisons.html', 'w') as f: f.write(comparisons_tpl.render())

    for country in countries:
        c_df = df[df['País'] == country].sort_values('Año')
        r23 = c_df[c_df['Año'] == 2023].iloc[0]
        # Transition logic
        trans = "Joven" if r23['Pct_70_mas'] + r23['Pct_65_69'] < 7 else "En Transición" if r23['Pct_70_mas'] + r23['Pct_65_69'] < 14 else "Envejecida"
        with open(f'docs/pages/countries/{slugify(country)}.html', 'w') as f:
            f.write(country_tpl.render(country=country, iso3=c_df['ISO3'].iloc[0], slug=slugify(country), rows=c_df.to_dict('records'), ev2023=r23.Esperanza_Vida, em2023=r23.Edad_Mediana_Estimada, transition=trans))

    print("Web portal v4 (Final Mega Upgrade) generated.")

if __name__ == "__main__": main()
