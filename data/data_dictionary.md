Diccionario de Datos

Conjunto de Datos de Estructura de Edad de la Población en América Latina (1995–2030)

Autor: Juan Moisés de la Serna
ORCID: 0000-0002-8401-8018

Licencia: CC BY 4.0

Este documento describe las variables incluidas en el conjunto de datos utilizado en el proyecto Estructura de Edad de la Población en América Latina.

El conjunto de datos contiene indicadores demográficos para múltiples países latinoamericanos en diferentes años, incluyendo la estructura poblacional por grupos de edad y por sexo.

Unidad de Observación del Conjunto de Datos

Cada fila corresponde a:

país + año

Esto significa que cada registro representa la estructura demográfica de un país específico en un año determinado.

Variables
PasAo

Tipo: texto (string)

Descripción
Nombre del país.

Ejemplos
Argentina
Chile
México
Perú

Año

Tipo: entero (integer)

Descripción
Año de referencia de la observación demográfica.

Ejemplos

1995
2000
2005
2010
2015
2020

PoblaciónTotalMillones

Tipo: numérico (decimal)
Unidad: millones de habitantes

Descripción
Población total del país en el año indicado.

Ejemplo

126.7 = 126,7 millones de habitantes

Variables de estructura por edad

Estas variables representan la distribución porcentual de la población por grupos de edad.

Pct014

Tipo: porcentaje (%)

Descripción
Porcentaje de población con edades entre 0 y 14 años.

Pct1524

Tipo: porcentaje (%)

Descripción
Porcentaje de población con edades entre 15 y 24 años.

Pct2554

Tipo: porcentaje (%)

Descripción
Porcentaje de población con edades entre 25 y 54 años.

Pct5564

Tipo: porcentaje (%)

Descripción
Porcentaje de población con edades entre 55 y 64 años.

Pct65ms

Tipo: porcentaje (%)

Descripción
Porcentaje de población con 65 años o más.

Variables por sexo dentro de cada grupo de edad

Estas variables representan la distribución por sexo dentro de cada grupo de edad.

Pct014H

Tipo: porcentaje (%)

Descripción
Porcentaje de hombres de 0 a 14 años.

Pct014M

Tipo: porcentaje (%)

Descripción
Porcentaje de mujeres de 0 a 14 años.

Pct1524H

Tipo: porcentaje (%)

Descripción
Porcentaje de hombres de 15 a 24 años.

Pct1524M

Tipo: porcentaje (%)

Descripción
Porcentaje de mujeres de 15 a 24 años.

Pct2554H

Tipo: porcentaje (%)

Descripción
Porcentaje de hombres de 25 a 54 años.

Pct2554M

Tipo: porcentaje (%)

Descripción
Porcentaje de mujeres de 25 a 54 años.

Pct5564H

Tipo: porcentaje (%)

Descripción
Porcentaje de hombres de 55 a 64 años.

Pct5564M

Tipo: porcentaje (%)

Descripción
Porcentaje de mujeres de 55 a 64 años.

Pct65H

Tipo: porcentaje (%)

Descripción
Porcentaje de hombres de 65 años o más.

Pct65M

Tipo: porcentaje (%)

Descripción
Porcentaje de mujeres de 65 años o más.

Fuente

Tipo: texto (string)

Descripción
Fuente principal de los datos utilizados para construir el conjunto de datos.

Valores posibles

CEPAL
CEPAL-BBVA
Institutos nacionales de estadística
Banco Mundial

Reglas de consistencia interna

El conjunto de datos sigue restricciones demográficas básicas.

Consistencia de la estructura por edad

La distribución por edad debe sumar aproximadamente 100 %.

Pct014
Pct1524
Pct2554
Pct5564
Pct65ms

≈ 100 %

Pequeñas diferencias pueden aparecer debido al redondeo.

Consistencia por sexo

Cada grupo de edad se descompone por sexo.

Pct014 ≈ Pct014H + Pct014M
Pct1524 ≈ Pct1524H + Pct1524M
Pct2554 ≈ Pct2554H + Pct2554M
Pct5564 ≈ Pct5564H + Pct5564M
Pct65ms ≈ Pct65H + Pct65M

Pequeñas diferencias pueden aparecer debido al redondeo.

Usos del conjunto de datos

Este conjunto de datos está diseñado para análisis de:

transición demográfica

envejecimiento poblacional

índice de dependencia demográfica

bono demográfico

visualización de pirámides poblacionales

comparaciones demográficas entre países

análisis demográfico por sexo

Productos derivados

Este conjunto de datos alimenta:

Atlas Demográfico Interactivo

pirámides de población

cálculos del índice de envejecimiento

paneles comparativos entre países

Cómo citar el conjunto de datos

De la Serna, J. M. (2026).
Estructura de Edad de la Población en América Latina (1995–2030).

DOI:
https://doi.org/10.5281/zenodo.18883431
