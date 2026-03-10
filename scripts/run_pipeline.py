from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "build_dataset_with_indicators.py",
    "build_latest_snapshot.py",
    "build_indicators_summary_by_country.py",
    "build_indicators_summary_by_year.py",
]


def run(script: str) -> None:
    print(f"\n>>> Ejecutando {script}")
    result = subprocess.run(
        [sys.executable, f"scripts/{script}"],
        check=False,
    )

    if result.returncode != 0:
        print(f"ERROR ejecutando {script}")
        sys.exit(result.returncode)


def main() -> None:
    print("===================================")
    print("Demographic Dataset Pipeline")
    print("===================================")

    for script in SCRIPTS:
        run(script)

    print("\nPipeline completado correctamente.")


if __name__ == "__main__":
    main()
