#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Orden de ejecución del pipeline
SCRIPTS = [
    'validate_dataset.py',
    'build_indicators.py',
    'build_atlas_data.py',
    'build_site.py',
    'generate_research_pages.py',
]


def main() -> int:
    base = Path(__file__).resolve().parent
    for name in SCRIPTS:
        script = base / name
        print(f'>>> Ejecutando {script.name}')
        result = subprocess.run([sys.executable, str(script)], check=False)
        if result.returncode != 0:
            print(f'Fallo en {script.name} con código {result.returncode}')
            return result.returncode
    print('Pipeline completado correctamente.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
