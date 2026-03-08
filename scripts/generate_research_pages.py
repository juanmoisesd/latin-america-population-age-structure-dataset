#!/usr/bin/env python3
from __future__ import annotations

import html
import sys

from common import add_indicators, ensure_dir, latest_by_country, parse_args, read_dataset, slugify


def page(title: str, intro: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="../assets/atlas.css">
</head>
<body>
<main class="container">
<h1>{html.escape(title)}</h1>
<p>{intro}</p>
{body}
<p><a href="../index.html">Volver al índice</a></p>
</main>
</body>
</html>'''


def list_html(df, value_col, decimals=2):
    items = []
    for _, row in df.iterrows():
        items.append(
            f'<li><a href="../countries/{slugify(row["País"])}.html">{html.escape(row["País"])}</a>: {round(float(row[value_col]), decimals)}</li>'
        )
    return '<ol>' + ''.join(items) + '</ol>'


def main() -> int:
    parser = parse_args('Genera páginas de investigación con rankings automáticos.')
    args = parser.parse_args()

    research_dir = args.docs_dir / 'research-questions'
    ensure_dir(research_dir)

    df = add_indicators(read_dataset(args.input))
    latest = latest_by_country(df)

    top_aging = latest.sort_values('Indice_Envejecimiento', ascending=False).head(10)
    top_bonus = latest.sort_values('Indice_Bono_Demografico', ascending=False).head(10)
    top_change = latest.sort_values('Cambio_Envejecimiento_vs_2000', ascending=False).head(10)

    pages = [
        ('top-envejecimiento', '¿Qué países presentan mayor envejecimiento demográfico?', 'Ranking basado en el último año disponible por país.', list_html(top_aging, 'Indice_Envejecimiento')),
        ('bono-demografico', '¿Dónde persiste con más fuerza el bono demográfico?', 'Ranking basado en la relación entre población en edad laboral y población dependiente.', list_html(top_bonus, 'Indice_Bono_Demografico', 4)),
        ('envejecimiento-mas-rapido', '¿Qué países envejecen más rápido desde 2000?', 'Ranking basado en el cambio acumulado del índice de envejecimiento frente al primer año disponible por país.', list_html(top_change, 'Cambio_Envejecimiento_vs_2000')),
    ]

    for slug, title, intro, body in pages:
        (research_dir / f'{slug}.html').write_text(page(title, intro, body), encoding='utf-8')
        print(f'OK: {research_dir / f"{slug}.html"}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
