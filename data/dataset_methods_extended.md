# Metodología ampliada del dataset

## Fuentes de datos

Los datos utilizados en la construcción del dataset proceden de:

- Comisión Económica para América Latina y el Caribe (CEPAL)
- Banco Mundial
- BBVA Research
- institutos nacionales de estadística

Estas fuentes proporcionan estimaciones demográficas comparables a nivel internacional.

---

# Procesamiento de datos

El proceso de construcción del dataset incluyó las siguientes etapas:

1. Recopilación de datos demográficos de las fuentes originales.
2. Estandarización de variables y formatos.
3. Verificación de consistencia interna.
4. Integración en un formato tabular uniforme.

---

# Normalización de variables

Para garantizar comparabilidad entre países se aplicaron las siguientes reglas:

- todos los porcentajes se expresan sobre la población total
- los grupos etarios siguen una estructura uniforme
- los datos se transformaron a formato CSV para facilitar su reutilización

---

# Validación de los datos

Se aplicaron varias verificaciones de consistencia:

- suma de porcentajes por grupos de edad cercana a 100 %
- coherencia entre porcentajes totales y distribución por sexo
- ausencia de valores inconsistentes

---

# Formato del dataset

El dataset se distribuye en formato CSV para facilitar su utilización en entornos de análisis de datos como:

- Python
- R
- Excel
- SPSS
- Stata
