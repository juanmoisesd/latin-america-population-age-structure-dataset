from __future__ import annotations

import pandas as pd

INPUT = "data/dataset_with_indicators.csv"
OUTPUT = "data/indicators_summary_by_year.csv"


def main() -> None:
    df = pd.read_csv(INPUT)

    # Promedio regional por año
    summary = (
        df.groupby("Año")
        .agg(
            Indice_Envejecimiento=("Indice_Envejecimiento", "mean"),
            Razon_Dependencia_Total=("Razon_Dependencia_Total", "mean"),
            Razon_Dependencia_Juvenil=("Razon_Dependencia_Juvenil", "mean"),
            Razon_Dependencia_Vejez=("Razon_Dependencia_Vejez", "mean"),
            Indice_Bono_Demografico=("Indice_Bono_Demografico", "mean"),
        )
        .reset_index()
    )

    # redondeo
    summary = summary.round(2)

    # ordenar cronológicamente
    summary = summary.sort_values("Año")

    summary.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

    print(f"Archivo generado: {OUTPUT}")


if __name__ == "__main__":
    main()
