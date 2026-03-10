# Correspondencia entre esquemas de metadatos (Schema Crosswalk)

Este documento describe la correspondencia entre los distintos esquemas de metadatos utilizados en este repositorio.

El objetivo es facilitar la interoperabilidad del dataset con repositorios científicos, motores de búsqueda académicos y plataformas de datos abiertos.

## Esquemas utilizados

El dataset utiliza los siguientes estándares de metadatos:

- Schema.org Dataset
- DCAT
- DataCite
- CodeMeta

## Correspondencia de campos principales

| Concepto | Schema.org | DCAT | DataCite | CodeMeta |
|----------|------------|------|----------|----------|
| Título | name | dct:title | title | name |
| Autor | creator | dct:creator | creators | author |
| DOI | identifier | dct:identifier | identifier | identifier |
| Descripción | description | dct:description | description | description |
| Licencia | license | dct:license | rights | license |
| Cobertura espacial | spatialCoverage | dct:spatial | geoLocations | spatialCoverage |
| Cobertura temporal | temporalCoverage | dct:temporal | dates | temporalCoverage |
| Palabras clave | keywords | dcat:keyword | subjects | keywords |
| Formato | encodingFormat | dct:format | formats | fileFormat |

## Beneficios de la interoperabilidad

El uso de múltiples esquemas permite que el dataset sea detectado y reutilizado en diferentes sistemas de información científica.

Entre ellos:

- Zenodo
- OpenAIRE
- Google Dataset Search
- OpenAlex
- DataCite
- repositorios institucionales
