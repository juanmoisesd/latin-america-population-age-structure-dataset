from __future__ import annotations

import pandas as pd

INPUT = "data/dataset.csv"
OUTPUT = "data/dataset_with_indicators.csv"

ISO3 = {
    "Argentina": "ARG",
    "Bolivia": "BOL",
    "Brasil": "BRA",
    "Chile": "CHL",
    "Colombia": "COL",
    "Costa Rica": "CRI",
    "Cuba": "CUB",
    "Ecuador": "ECU",
    "El Salvador": "SLV",
    "Guatemala": "GTM",
    "Honduras": "HND",
    "México": "MEX",
    "Nicaragua": "NIC",
    "Panamá": "PAN",
    "Paraguay": "PRY",
    "Perú": "PER",
    "República Dominicana": "DOM",
    "Uruguay": "URY",
    "Venezuela": "VEN",
}

REGION = {
    "Argentina": "Sudamérica",
    "Bolivia": "Sudamérica",
    "Brasil": "Sudamérica",
    "Chile": "Sudamérica",
    "Colombia": "Sudamérica",
    "Costa Rica": "Centroamérica",
    "Cuba": "Caribe",
    "Ecuador": "Sudamérica",
    "El Salvador": "Centroamérica",
    "Guatemala": "Centroamérica",
    "Honduras": "Centroamérica",
    "México": "Norteamérica",
    "Nicaragua": "Centroamérica",
    "Panamá": "Centroamérica",
    "Paraguay": "Sudamérica",
    "Perú": "Sudamérica",
    "República Dominicana": "Caribe",
    "Uruguay": "Sudamérica",
    "Venezuela": "Sudamérica",
}


def clasificacion_envejecimiento(pct_65: float) -> str:
    if pct_65 < 7:
        return "joven"
    if pct_65 < 14:
        return "transición"
    return "envejecida"


def clasificacion_dependencia(rdt: float) -> str:
    if rdt >= 60:
        return "alta"
    if rdt >= 50:
        return "moderada"
    return "baja"


def main() -> None:
    df = pd.read_csv(INPUT)

    # Solo filas totales
    df = df[df["Sexo"].astype(str).str.upper() == "TOTAL"].copy()

    # Renombrado base
    df = df.rename(
        columns={
            "País": "País",
            "Año": "Año",
            "Pob_Total_Millones": "Población_Total_Millones",
        }
    )

    # Agregación de grupos amplios
    df["Pct_0_14"] = df["Pct_0_4"] + df["Pct_5_9"] + df["Pct_10_14"]
    df["Pct_15_24"] = df["Pct_15_19"] + df["Pct_20_24"]
    df["Pct_25_54"] = (
        df["Pct_25_29"]
        + df["Pct_30_34"]
        + df["Pct_35_39"]
        + df["Pct_40_44"]
        + df["Pct_45_49"]
        + df["Pct_50_54"]
    )
    df["Pct_55_64"] = df["Pct_55_59"] + df["Pct_60_64"]
    df["Pct_65_más"] = df["Pct_65_69"] + df["Pct_70_mas"]

    df["Pob_0_14_Miles"] = df["Pob_0_4_k"] + df["Pob_5_9_k"] + df["Pob_10_14_k"]
    df["Pob_15_24_Miles"] = df["Pob_15_19_k"] + df["Pob_20_24_k"]
    df["Pob_25_54_Miles"] = (
        df["Pob_25_29_k"]
        + df["Pob_30_34_k"]
        + df["Pob_35_39_k"]
        + df["Pob_40_44_k"]
        + df["Pob_45_49_k"]
        + df["Pob_50_54_k"]
    )
    df["Pob_55_64_Miles"] = df["Pob_55_59_k"] + df["Pob_60_64_k"]
    df["Pob_65_más_Miles"] = df["Pob_65_69_k"] + df["Pob_70_mas_k"]

    # Metadatos
    df["ISO3"] = df["País"].map(ISO3)
    df["Región"] = df["País"].map(REGION)

    # Derivadas
    df["Pct_Edad_Laboral"] = df["Pct_15_24"] + df["Pct_25_54"] + df["Pct_55_64"]
    df["Pct_Joven_Total"] = df["Pct_0_14"] + df["Pct_15_24"]

    df["Pob_Edad_Laboral_Miles"] = (
        df["Pob_15_24_Miles"] + df["Pob_25_54_Miles"] + df["Pob_55_64_Miles"]
    )
    df["Pob_Dependiente_Miles"] = df["Pob_0_14_Miles"] + df["Pob_65_más_Miles"]

    df["Indice_Envejecimiento"] = (df["Pob_65_más_Miles"] / df["Pob_0_14_Miles"]) * 100
    df["Indice_Juventud"] = df["Pob_0_14_Miles"] / df["Pob_65_más_Miles"]

    df["Razon_Dependencia_Total"] = (
        df["Pob_Dependiente_Miles"] / df["Pob_Edad_Laboral_Miles"]
    ) * 100
    df["Razon_Dependencia_Juvenil"] = (
        df["Pob_0_14_Miles"] / df["Pob_Edad_Laboral_Miles"]
    ) * 100
    df["Razon_Dependencia_Vejez"] = (
        df["Pob_65_más_Miles"] / df["Pob_Edad_Laboral_Miles"]
    ) * 100

    df["Indice_Bono_Demografico"] = (
        df["Pob_Edad_Laboral_Miles"] / df["Pob_Dependiente_Miles"]
    )
    df["Relacion_Jovenes_Mayores"] = df["Indice_Juventud"]
    df["Old_Age_Ratio"] = df["Razon_Dependencia_Vejez"] / 100.0

    # Cambios respecto a 2000 por país
    base2000 = (
        df[df["Año"] == 2000][["País", "Indice_Envejecimiento", "Pct_65_más", "Pct_0_14"]]
        .rename(
            columns={
                "Indice_Envejecimiento": "Base_Indice_Envejecimiento",
                "Pct_65_más": "Base_Pct_65_más",
                "Pct_0_14": "Base_Pct_0_14",
            }
        )
    )

    df = df.merge(base2000, on="País", how="left")

    df["Cambio_Envejecimiento_vs_2000"] = (
        df["Indice_Envejecimiento"] - df["Base_Indice_Envejecimiento"]
    )
    df["Cambio_Pct_65_más_vs_2000"] = df["Pct_65_más"] - df["Base_Pct_65_más"]
    df["Cambio_Pct_0_14_vs_2000"] = df["Pct_0_14"] - df["Base_Pct_0_14"]

    df["Suma_Pct_Grupos"] = (
        df["Pct_0_14"]
        + df["Pct_15_24"]
        + df["Pct_25_54"]
        + df["Pct_55_64"]
        + df["Pct_65_más"]
    )
    df["Pct_Grupos_Validos"] = (df["Suma_Pct_Grupos"] - 100).abs() <= 0.2

    df["Clasificacion_Envejecimiento"] = df["Pct_65_más"].apply(clasificacion_envejecimiento)
    df["Clasificacion_Dependencia"] = df["Razon_Dependencia_Total"].apply(clasificacion_dependencia)

    # Limpieza final
    df = df.rename(columns={"Fuente": "Fuente"})

    cols = [
        "País",
        "Año",
        "Población_Total_Millones",
        "Pct_0_14",
        "Pct_15_24",
        "Pct_25_54",
        "Pct_55_64",
        "Pct_65_más",
        "Pob_0_14_Miles",
        "Pob_15_24_Miles",
        "Pob_25_54_Miles",
        "Pob_55_64_Miles",
        "Pob_65_más_Miles",
        "Fuente",
        "ISO3",
        "Región",
        "Pct_Edad_Laboral",
        "Pct_Joven_Total",
        "Pob_Edad_Laboral_Miles",
        "Pob_Dependiente_Miles",
        "Indice_Envejecimiento",
        "Indice_Juventud",
        "Razon_Dependencia_Total",
        "Razon_Dependencia_Juvenil",
        "Razon_Dependencia_Vejez",
        "Indice_Bono_Demografico",
        "Relacion_Jovenes_Mayores",
        "Old_Age_Ratio",
        "Cambio_Envejecimiento_vs_2000",
        "Cambio_Pct_65_más_vs_2000",
        "Cambio_Pct_0_14_vs_2000",
        "Suma_Pct_Grupos",
        "Pct_Grupos_Validos",
        "Clasificacion_Envejecimiento",
        "Clasificacion_Dependencia",
    ]

    df = df[cols].sort_values(["País", "Año"]).reset_index(drop=True)

    # Redondeo
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df[numeric_cols] = df[numeric_cols].round(2)

    df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    print(f"Archivo generado: {OUTPUT}")


if __name__ == "__main__":
    main()
