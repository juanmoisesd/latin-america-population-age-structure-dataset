# Metodología de construcción del dataset

## Fuentes de datos

La información demográfica se recopiló a partir de diversas fuentes internacionales y regionales:

- CEPAL (Comisión Económica para América Latina y el Caribe)
- Banco Mundial
- BBVA Research
- institutos nacionales de estadística

## Proceso de compilación

1. Recopilación de datos demográficos publicados por las fuentes oficiales.
2. Selección de variables relevantes para el análisis de estructura de edad.
3. Homogeneización de formatos y unidades de medida.
4. Conversión de datos a un formato tabular uniforme.
5. Verificación de consistencia interna.

## Variables incluidas

El dataset incluye:

- población total
- estructura por grupos de edad
- distribución por sexo dentro de cada grupo etario
- fuente de los datos

## Control de consistencia

Se aplicaron las siguientes verificaciones:

- La suma de porcentajes por grupos de edad debe aproximarse al 100 %.
- La suma de porcentajes por sexo debe aproximarse al total del grupo etario correspondiente.

## Formato del dataset

El dataset se distribuye en formato:

CSV (Comma Separated Values)

Este formato permite su uso en múltiples entornos analíticos, incluyendo:

- Python
- R
- Excel
- SPSS
- Stata
