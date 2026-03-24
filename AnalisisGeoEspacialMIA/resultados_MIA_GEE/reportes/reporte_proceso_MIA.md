# Reporte de Análisis Geoespacial MIA
## Proyecto: Puerto Nuevo Manzanillo, Vaso II Laguna Cuyutlán

---

## Información General

| Parámetro | Valor |
|-----------|-------|
| Fecha de ejecución | 2026-03-24 |
| Hora de inicio | 17:11:46 |
| Hora de fin | 17:19:37 |
| Duración total | 7.84 minutos |
| Período de análisis | 2016 - 2025 |

## Resumen de Pasos Ejecutados

| Paso | Descripción | Duración (s) | Estado |
|------|-------------|--------------|--------|
| 1 | Autenticación Google Earth Engine | 6.22 | ✓ COMPLETADO |
| 2 | Carga del Sistema Ambiental Regional (SAR) | 0.94 | ✓ COMPLETADO |
| 3 | Análisis de Cobertura de Manglar (NOM-022) | 78.42 | ✓ COMPLETADO |
| 4 | Análisis Multitemporal de NDVI (Salud Vegetación) | 242.37 | ✓ COMPLETADO |
| 5 | Análisis de Cambio de Uso de Suelo | 102.86 | ✓ COMPLETADO |
| 6 | Análisis de Cuerpos de Agua (JRC GSW) | 1.71 | ✓ COMPLETADO |
| 7 | Modelo Digital de Elevación y Pendientes (SRTM) | 2.09 | ✓ COMPLETADO |
| 8 | Análisis Climático (Temperatura y Precipitación) | 4.49 | ✓ COMPLETADO |
| 9 | Detección de Incendios Históricos (MODIS Fire) | 13.86 | ✓ COMPLETADO |
| 10 | Generación de Mapa Interactivo HTML | 8.38 | ✓ COMPLETADO |
| 11 | Exportación de Capas GeoTIFF a Google Drive | 9.27 | ✓ COMPLETADO |
| 12 | Generación de Tabla Resumen USV | 0.00 | ✓ COMPLETADO |

## Estadísticas Principales

| Indicador | Valor | Unidad |
|-----------|-------|--------|
| gee_inicializado | True |  |
| area_sar_km2 | 585.9287 |  |
| area_ap_km2 | 3.5061 |  |
| fuente_sar | shapefile |  |
| manglar_sar_ha | 170.0413 |  |
| manglar_ap_ha | 1.1734 |  |
| buffer_proteccion_m | 100 |  |
| fuente_manglar | Clasificación espectral (NDVI+NDWI+CMRI+SRTM+JRC) |  |
| gmw_disponible | False |  |
| ndvi_años_analizados | 5 |  |
| cambio_ndvi | 0.0690 |  |
| tendencia_vegetacion | MEJORA |  |
| perdida_vegetacion_ha | 2266.8260 |  |
| ganancia_vegetacion_ha | 7695.5737 |  |
| balance_neto_ha | 5428.7477 |  |
| agua_permanente_ha | 4568.8825 |  |
| agua_estacional_ha | 1426.2229 |  |
| agua_total_ha | 5995.1054 |  |
| elevacion_media_m | 158.4183 |  |
| elevacion_min_m | -35 |  |
| elevacion_max_m | 1240 |  |
| area_bajo_5m_ha | 11415.1306 |  |
| temperatura_media_C | 30.4148 |  |
| temperatura_max_C | 34.0728 |  |
| precipitacion_anual_mm | 0 |  |
| detecciones_fuego_total | 256.3608 |  |
| detecciones_fuego_max_pixel | 11 |  |
| periodo_analisis | 2016-2025 |  |
| mapa_html | True |  |
| tareas_exportacion | 8 |  |

## Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `mapa_MIA_cuyutlan.html` | Mapa interactivo HTML |
| `uso_suelo_vegetacion.csv` | Uso de suelo y vegetación |
| `cambio_uso_suelo.csv` | Cambio de uso de suelo |
| `estadisticas_ndvi.csv` | Estadísticas NDVI |
| `analisis_manglar.csv` | Análisis de manglar |
| `*.tif` | Capas GeoTIFF para QGIS |

---
*Reporte generado automáticamente por MIA_GEE_Analisis_v1.py*