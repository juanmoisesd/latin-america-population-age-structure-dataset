import pandas as pd
import os
import json
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
    #map { height: 500px; width: 100%; border-radius: 12px; }
    .btn { display: inline-block; padding: 10px 20px; background: var(--accent); color: white; border-radius: 5px; text-decoration: none; font-weight: bold; }
    footer { background: var(--primary); color: white; padding: 30px 0; margin-top: 60px; text-align: center; }
</style>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
"""

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    os.makedirs('docs/pages/countries', exist_ok=True)
    countries = sorted(df['País'].unique())
    country_slugs = {c: slugify(c) for c in countries}

    # Map markers data
    coords = {
        "México": [23.6345, -102.5528], "Brasil": [-14.235, -51.9253], "Argentina": [-38.4161, -63.6167],
        "Colombia": [4.5709, -74.2973], "Chile": [-35.6751, -71.543], "Perú": [-9.19, -75.0152],
        "Venezuela": [6.4238, -66.5897], "Bolivia": [-16.2902, -63.5887], "Ecuador": [-1.8312, -78.1834],
        "Uruguay": [-32.5228, -55.7658], "Paraguay": [-23.4425, -58.4438], "Costa Rica": [9.7489, -83.7534],
        "Panamá": [8.538, -80.7821], "Nicaragua": [12.8654, -85.2072], "Honduras": [15.1999, -86.2419],
        "El Salvador": [13.7942, -88.8965], "Guatemala": [15.7835, -90.2308], "Cuba": [21.5218, -77.7812],
        "República Dominicana": [18.7357, -70.1627]
    }

    map_data = []
    for c in countries:
        latest = df[(df['País'] == c) & (df['Año'] == 2023)].iloc[0]
        map_data.append({
            "name": c, "lat": coords.get(c, [0,0])[0], "lng": coords.get(c, [0,0])[1],
            "pop": latest.Pob_Total_Millones, "ev": latest.Esperanza_Vida, "slug": country_slugs[c]
        })

    # index.html with Leaflet
    index_tpl = Template(f"""
    <!DOCTYPE html><html><head><meta charset='UTF-8'><title>Portal Demográfico AL</title>{BASE_STYLE}</head><body>{get_header(0)}
    <main><section><h2>Mapa Interactivo Regional</h2><div id="map"></div></section>
    <section><h2>Explora Países</h2><div id='countries' class='grid'>{{% for c in countries %}}
    <div class='card'><h3>{{{{ c }}}}</h3><a href='pages/countries/{{{{ country_slugs[c] }}}}.html' class='btn'>Ver Perfil</a></div>
    {{% endfor %}}</div></section></main>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
    var map = L.map('map').setView([-15, -60], 3);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
    var data = {json.dumps(map_data)};
    data.forEach(c => {{
        L.marker([c.lat, c.lng]).addTo(map)
            .bindPopup(`<b>${{c.name}}</b><br>Pob: ${{c.pop}}M<br>Exp. Vida: ${{c.ev}} años<br><a href="pages/countries/${{c.slug}}.html">Ver más</a>`);
    }});
    </script>
    {get_footer()}</body></html>""")

    # Other pages (keep previous)
    with open('docs/index.html', 'w') as f: f.write(index_tpl.render(countries=countries, country_slugs=country_slugs))

    # Summary API
    os.makedirs('docs/api', exist_ok=True)
    with open('docs/api/summary.json', 'w') as f:
        json.dump(map_data, f, indent=2)

    # Re-generate country pages if needed, but assuming they were fine.
    # Just running the core generation here.

    print("Interactive mapping and summary API updated.")

if __name__ == "__main__": main()
