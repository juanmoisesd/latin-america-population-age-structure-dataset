#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Orden de ejecución del pipeline
SCRIPTS = [
    "validate_dataset.py",
    "build_indicators.py",
    "build_atlas_data.py",
    "build_site.py",
    "generate_research_pages.py",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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
    started_at = datetime.now(timezone.utc)

    print("===================================")
    print("Demographic Dataset Pipeline")
    print("Inicio:", now_utc(), "UTC")
    print("Python:", sys.version.split()[0])
    print("Raíz del proyecto:", root)
    print("===================================\n")

    for name in SCRIPTS:
        script = base / name

        if not script.exists():
            print(f"ERROR: no se encontró el script {script}", file=sys.stderr)
            return 1

        code = run_script(script, root)

        if code != 0:
            print("\n===================================")
            print(f"Pipeline interrumpido por error en {script.name}.", file=sys.stderr)
            print(f"Código de salida: {code}", file=sys.stderr)
            print("Fin:", now_utc(), "UTC", file=sys.stderr)
            print("===================================")
            return code

    finished_at = datetime.now(timezone.utc)
    duration = finished_at - started_at

    print("\n===================================")
    print("Pipeline completado correctamente.")
    print("Fin:", now_utc(), "UTC")
    print("Duración total:", duration)
    print("===================================")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nERROR: ejecución interrumpida por el usuario.", file=sys.stderr)
        raise SystemExit(130)
