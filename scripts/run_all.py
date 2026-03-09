#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Orden de ejecución del pipeline
SCRIPTS = [
    "validate_dataset.py",
    "build_indicators.py",
    "build_atlas_data.py",
    "build_site.py",
    "generate_research_pages.py",
]


def run_script(script: Path, root: Path) -> int:
    print(f"\n>>> Ejecutando {script.name}")
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=False,
    )
    return result.returncode


def main() -> int:
    base = Path(__file__).resolve().parent
    root = base.parent

    print("===================================")
    print("Demographic Dataset Pipeline")
    print("Inicio:", datetime.utcnow().isoformat(), "UTC")
    print("Python:", sys.version.split()[0])
    print("===================================\n")

    failures = []

    for name in SCRIPTS:
        script = base / name

        if not script.exists():
            print(f"ERROR: no se encontró el script {script}", file=sys.stderr)
            failures.append(name)
            continue

        code = run_script(script, root)

        if code != 0:
            print(f"ERROR: fallo en {script.name} con código {code}", file=sys.stderr)
            failures.append(name)

    print("\n===================================")

    if failures:
        print("Pipeline finalizado con errores.")
        print("Scripts con fallo:")
        for f in failures:
            print(f" - {f}")
        return 1

    print("Pipeline completado correctamente.")
    print("Fin:", datetime.utcnow().isoformat(), "UTC")
    print("===================================")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
