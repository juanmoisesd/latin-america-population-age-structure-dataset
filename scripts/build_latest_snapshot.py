from __future__ import annotations

import pandas as pd

INPUT = "data/dataset_with_indicators.csv"
OUTPUT = "data/latest_snapshot.csv"


def main() -> None:
    df = pd.read_csv(INPUT)

    # Último año disponible por país
    latest = (
        df.sort_values(["País", "Año"])
          .groupby("País", as_index=False)
          .tail(1)
          .sort_values("País")
          .reset_index(drop=True)
    )

    latest.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    print(f"Archivo generado: {OUTPUT}")


if __name__ == "__main__":
    main()
