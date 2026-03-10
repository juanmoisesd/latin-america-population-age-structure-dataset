from __future__ import annotations

import pandas as pd

INPUT = "data/dataset_with_indicators.csv"
OUTPUT = "data/indicators_summary_by_country.csv"


def main() -> None:
    df = pd.read_csv(INPUT)

    # Promedio de indicadores por país
    summary = (
        df.groupby("País")
        .agg(
            Indice_Envejecimiento=("Indice_Envejecimiento", "mean"),
            Razon_Dependencia_Total=("Razon_Dependencia_Total", "mean"),
            Razon_Dependencia_Juvenil=("Razon_Dependencia_Juvenil", "mean"),
            Razon_Dependencia_Vejez=("Razon_Dependencia_Vejez", "mean"),
            Indice_Bono_Demografico=("Indice_Bono_Demografico", "mean"),
        )
        .reset_index()
    )

    summary = summary.round(2)

    summary = summary.sort_values(
        by="Indice_Envejecimiento",
        ascending=False
    )

    summary.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

    print(f"Archivo generado: {OUTPUT}")


if __name__ == "__main__":
    main()
