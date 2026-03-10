from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Scripts que regeneran todos los derivados del dataset
SCRIPTS = [
    "build_dataset_with_indicators.py",
    "build_latest_snapshot.py",
    "build_indicators_summary_by_country.py",
    "build_indicators_summary_by_year.py",
    "build_atlas_exports.py",
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

        rc = run_script(script, root)

        if rc != 0:
            failures.append(name)

    print("\n===================================")

    if failures:
        print("Pipeline finalizado con errores.")
        print("Scripts fallidos:")
        for f in failures:
            print(" -", f)
        return 1

    print("Pipeline completado correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
