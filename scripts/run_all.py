#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Orden de ejecución del pipeline
SCRIPTS = [
    "validate_dataset.py",
    "build_indicators.py",
    "build_atlas_data.py",
    "build_site.py",
    "generate_research_pages.py",
]


def main() -> int:
    base = Path(__file__).resolve().parent

    for name in SCRIPTS:
        script = base / name

        if not script.exists():
            print(f"ERROR: no se encontró el script {script}", file=sys.stderr)
            return 1

        print(f">>> Ejecutando {script.name}")
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=base.parent,
            check=False,
        )

        if result.returncode != 0:
            print(f"ERROR: fallo en {script.name} con código {result.returncode}", file=sys.stderr)
            return result.returncode

    print("Pipeline completado correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
