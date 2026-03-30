import pandas as pd
import os
from jinja2 import Template

def slugify(text):
    return text.lower().replace(' ', '_').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á', 'a').replace('ú', 'u').replace('ñ', 'n')

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    os.makedirs('docs/countries', exist_ok=True)

    index_template = Template("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Demografía América Latina 2000-2030</title>
        <link rel="stylesheet" href="style.css">
        <style>
            body { font-family: sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
            header { background: #333; color: #fff; padding: 10px 20px; margin-bottom: 20px; }
            nav a { color: #fff; margin-right: 15px; text-decoration: none; }
            main { display: flex; flex-wrap: wrap; gap: 20px; }
            section { flex: 1; min-width: 300px; }
            .viz-grid { display: flex; flex-wrap: wrap; gap: 10px; }
            .viz-grid img { max-width: 100%; border: 1px solid #ddd; }
            ul { list-style: none; padding: 0; }
            li { margin-bottom: 5px; }
            footer { margin-top: 40px; border-top: 1px solid #ccc; padding-top: 10px; font-size: 0.8em; }
        </style>
    </head>
    <body>
        <header>
            <h1>Portal Demográfico de América Latina</h1>
            <nav>
                <a href="index.html">Inicio</a> |
                <a href="https://github.com/juanmoisesd/latin-america-population-age-structure-dataset">GitHub Repository</a>
            </nav>
        </header>

        <main>
            <section>
                <h2>Selecciona un País / Select a Country</h2>
                <ul>
                {% for country in countries %}
                    <li><a href="countries/{{ country_slugs[country] }}.html">{{ country }}</a></li>
                {% endfor %}
                </ul>
            </section>
            <section>
                <h2>Visualizaciones Regionales / Regional Visualizations</h2>
                <div class="viz-grid">
                    <img src="assets/dependency_trend.png" alt="Tendencia de Dependencia">
                    <img src="assets/aging_regional_bar.png" alt="Envejecimiento por País">
                </div>
            </section>
        </main>

        <footer>
            <p>© 2026 Juan Moisés de la Serna Tuya. Todos los derechos reservados / All rights reserved.</p>
        </footer>
    </body>
    </html>
    """)

    country_template = Template("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Demografía: {{ country }}</title>
        <link rel="stylesheet" href="../style.css">
        <style>
            body { font-family: sans-serif; line-height: 1.6; padding: 20px; }
            header { background: #444; color: #fff; padding: 10px 20px; }
            nav a { color: #fff; text-decoration: none; }
            .chart-section { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px; }
            .chart-section img { max-width: 450px; border: 1px solid #eee; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            footer { margin-top: 40px; font-size: 0.8em; }
        </style>
    </head>
    <body>
        <header>
            <h1>Portal Demográfico: {{ country }}</h1>
            <nav>
                <a href="../index.html">Volver al Inicio</a>
            </nav>
        </header>

        <main>
            <h2>Análisis de {{ country }} ({{ iso3 }})</h2>

            <section class="chart-section">
                <div>
                    <h3>Pirámide de Edad (2000 vs 2023)</h3>
                    <img src="../assets/pyramid_{{ slug }}_2000.png" alt="2000">
                    <img src="../assets/pyramid_{{ slug }}_2023.png" alt="2023">
                </div>
                <div>
                    <h3>Tendencia de Dependencia (2000-2030)</h3>
                    <img src="../assets/dependency_{{ slug }}.png" alt="Tendencia">
                </div>
            </section>

            <h3>Datos Estadísticos</h3>
            <table>
                <thead>
                    <tr>
                        <th>Año</th>
                        <th>Pob (Millones)</th>
                        <th>Dependencia Total (%)</th>
                        <th>Esperanza Vida</th>
                        <th>Edad Mediana</th>
                    </tr>
                </thead>
                <tbody>
                {% for row in rows %}
                    <tr>
                        <td>{{ row['Año'] }}</td>
                        <td>{{ row['Pob_Total_Millones'] }}</td>
                        <td>{{ row['Tasa_Dependencia_Total'] }}</td>
                        <td>{{ row['Esperanza_Vida'] }}</td>
                        <td>{{ row['Edad_Mediana_Estimada'] }}</td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </main>

        <footer>
            <p>© 2026 Juan Moisés de la Serna Tuya.</p>
        </footer>
    </body>
    </html>
    """)

    countries = sorted(df['País'].unique())
    country_slugs = {c: slugify(c) for c in countries}

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(index_template.render(countries=countries, country_slugs=country_slugs))

    for country in countries:
        c_df = df[df['País'] == country].sort_values('Año')
        rows = c_df.to_dict('records')
        iso3 = c_df['ISO3'].iloc[0]
        slug = country_slugs[country]
        with open(f'docs/countries/{slug}.html', 'w', encoding='utf-8') as f:
            f.write(country_template.render(country=country, iso3=iso3, rows=rows, slug=slug))

    print("Web portal generated in docs/")

if __name__ == "__main__":
    main()
