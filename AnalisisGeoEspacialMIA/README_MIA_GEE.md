# Análisis Geoespacial MIA con Google Earth Engine
## Puerto Nuevo Manzanillo - Laguna de Cuyutlán, Colima

**Versión:** 1.1  
**Última actualización:** Marzo 2026

---

## Descripción

Este programa Python realiza un análisis geoespacial completo para la **Manifestación de Impacto Ambiental (MIA) Modalidad Regional** del proyecto "Desarrollo del Puerto Nuevo Manzanillo, en el Vaso II de la Laguna Cuyutlán".

El script está diseñado siguiendo la estructura del programa `NATECHv3.py` y genera reportes detallados de cada proceso.

---

## Requisitos

### Software
- Python 3.8+
- Google Earth Engine (cuenta activa)
- QGIS 3.x (opcional, para visualización)

### Bibliotecas Python
```bash
pip install earthengine-api geemap geopandas shapely pandas
```

### Autenticación GEE
```bash
earthengine authenticate
```

---

## Configuración

Antes de ejecutar, modificar las siguientes variables en el archivo:

```python
# Línea 59-60: Rutas de trabajo
BASE = r"D:\ownCloud\Python\AnalisisGeoEspacialMIA"  # Cambiar a tu ruta

# Línea 86-87: Credenciales GEE
GEE_ACCOUNT = 'tu_cuenta@gmail.com'    # Tu cuenta de Google
GEE_PROJECT = 'tu-proyecto-gee'         # Tu proyecto en GEE
```

### Estructura de carpetas esperada
```
AnalisisGeoEspacialMIA/
├── capasSHP/
│   ├── areaSAR.shp          # Polígono del Sistema Ambiental Regional
│   ├── areaProyecto.shp     # Polígono del Área de Proyecto
│   └── sitiosMuestreo.shp   # Puntos de muestreo (opcional)
├── resultados_MIA_GEE/      # Se crea automáticamente
│   ├── reportes/
│   │   ├── reporte_proceso_MIA.md
│   │   └── log_procesamiento.txt
│   ├── mapa_MIA_cuyutlan.html
│   ├── uso_suelo_vegetacion.csv
│   ├── cambio_uso_suelo.csv
│   ├── estadisticas_ndvi.csv
│   └── analisis_manglar.csv
└── MIA_GEE_Analisis_v1.py
```

---

## Ejecución

### Desde línea de comandos
```bash
python MIA_GEE_Analisis_v1.py
```

### Desde QGIS (consola Python)
```python
exec(open('ruta/MIA_GEE_Analisis_v1.py').read())
# Después de completar, cargar capas:
cargar_capas_qgis()
```

---

## Capas Generadas

| Capa | Descripción | Fuente |
|------|-------------|--------|
| `MIA_NDVI_actual` | NDVI más reciente | Sentinel-2 |
| `MIA_manglar` | Cobertura de manglar | GMW o Clasificación Espectral |
| `MIA_agua_ocurrencia` | Frecuencia de inundación | JRC Global Surface Water |
| `MIA_cambio_ndvi` | Cambio en vegetación | Sentinel-2 multitemporal |
| `MIA_elevacion` | Modelo digital de elevación | SRTM |
| `MIA_pendiente` | Pendientes del terreno | SRTM derivado |
| `MIA_temperatura` | Temperatura superficial | MODIS LST |
| `MIA_precipitacion` | Precipitación acumulada | CHIRPS |

---

## Reportes de Proceso

El programa genera reportes detallados:

### Log de procesamiento (`log_procesamiento.txt`)
Registro cronológico de cada operación con timestamps.

### Reporte Markdown (`reporte_proceso_MIA.md`)
Resumen ejecutivo con:
- Información general de la ejecución
- Resumen de pasos ejecutados
- Estadísticas principales
- Errores y advertencias
- Lista de archivos generados

---

## Metodología

### Análisis realizados:

1. **Cobertura de Manglar (Paso 3)** ⚡ *Actualizado v1.1*
   - **Fuente primaria:** Global Mangrove Watch (GMW)
   - **Fuente alternativa:** Clasificación espectral automática (si GMW no está disponible)
   - **Normativa:** NOM-022-SEMARNAT-2003
   - **Buffer de protección:** 100 m
   
   > **Nota v1.1:** El programa ahora detecta automáticamente si GMW está accesible. Si no lo está, utiliza una clasificación espectral basada en índices (NDVI, NDWI, CMRI) combinados con datos de elevación SRTM y ocurrencia de agua JRC.

2. **NDVI Multitemporal (Paso 4)**
   - Fuente: Sentinel-2 (2016-presente)
   - Indicador: Salud de vegetación
   - Detección de tendencias

3. **Cambio de Uso de Suelo (Paso 5)**
   - Comparación de períodos
   - Detección de pérdida/ganancia de vegetación
   - Balance neto

4. **Cuerpos de Agua (Paso 6)**
   - Fuente: JRC Global Surface Water
   - Clasificación: permanente vs estacional

5. **Elevación y Pendientes (Paso 7)**
   - Fuente: SRTM 30m
   - Zonas susceptibles a inundación (<5m)

6. **Análisis Climático (Paso 8)**
   - Temperatura: MODIS LST
   - Precipitación: CHIRPS

7. **Detección de Incendios (Paso 9)**
   - Fuente: MODIS Active Fire
   - Período: 10 años

---

## Detección de Manglar - Metodología Alternativa

Cuando Global Mangrove Watch (GMW) no está disponible, el programa utiliza una **clasificación espectral multi-criterio** basada en literatura científica:

### Índices Espectrales Utilizados

| Índice | Fórmula | Criterio | Justificación |
|--------|---------|----------|---------------|
| **NDVI** | (NIR - Red) / (NIR + Red) | > 0.25 | Detecta vegetación verde activa |
| **NDWI** | (Green - NIR) / (Green + NIR) | -0.4 a 0.2 | Identifica zonas húmedas sin ser agua abierta |
| **CMRI** | NDVI - NDWI | > 0.3 | Índice combinado específico para manglar |
| **MNDWI** | (Green - SWIR) / (Green + SWIR) | Auxiliar | Mejor discriminación de agua |

### Criterios de Clasificación

```
Manglar = (NDVI > 0.25) AND (NDWI entre -0.4 y 0.2) AND 
          [(CMRI > 0.3) OR (Elevación < 10m AND Ocurrencia agua 10-80%)]
```

### Fuentes de Datos Complementarias

| Dato | Fuente GEE | Uso |
|------|------------|-----|
| Elevación | `USGS/SRTMGL1_003` | Filtrar zonas costeras bajas (<10m) |
| Ocurrencia agua | `JRC/GSW1_4/GlobalSurfaceWater` | Identificar zonas de transición (10-80%) |
| Imágenes ópticas | `COPERNICUS/S2_SR_HARMONIZED` | Calcular índices espectrales |

### Validación Recomendada

La clasificación espectral debe validarse con:
- Datos de campo del Capítulo IV y VIII de la MIA
- Cartografía INEGI Serie VII de Uso de Suelo y Vegetación
- Polígonos de manglar de CONABIO/CONAFOR

---

## Integración con Capítulos de la MIA

| Capítulo MIA | Análisis GEE relacionado |
|--------------|--------------------------|
| IV - Descripción del Sistema Ambiental | NDVI, Manglar, Cuerpos de agua, Clima |
| V - Identificación de Impactos | Cambio de uso de suelo, Fragmentación |
| VI - Medidas de Mitigación | Buffer de manglar, Zonas sensibles |
| VII - Pronósticos Ambientales | Tendencias NDVI, Series temporales |
| VIII - Identificación de Instrumentos | Normatividad aplicable |

---

## Normatividad Considerada

- **LGEEPA** - Ley General del Equilibrio Ecológico y Protección al Ambiente
- **REIA** - Reglamento en materia de Evaluación del Impacto Ambiental
- **NOM-022-SEMARNAT-2003** - Especificaciones para la preservación de humedales costeros
- **NOM-059-SEMARNAT-2010** - Protección de especies nativas
- **LGDFS** - Ley General de Desarrollo Forestal Sustentable
- **INEGI Serie VII** - Uso de Suelo y Vegetación (2021)

---

## Solución de Problemas

### Error de autenticación GEE
```bash
earthengine authenticate --auth_mode=notebook
```

### geopandas no disponible
El programa usa coordenadas hardcoded como fallback.

### Exportación a Drive lenta
Verificar progreso en: https://code.earthengine.google.com/tasks

### ⚡ Error: "ImageCollection asset not found" (Global Mangrove Watch)
**Causa:** El dataset GMW puede no estar accesible en tu cuenta de GEE o cambió de ubicación.

**Solución:** El programa v1.1 detecta automáticamente este error y utiliza clasificación espectral como alternativa. El log mostrará:
```
[INFO] No disponible projects/global-mangrove-watch/GMW/2020: ...
→ Usando clasificación espectral alternativa para manglar...
✓ Clasificación espectral completada
✓ Fuente de datos: Clasificación espectral (NDVI+NDWI+CMRI+SRTM+JRC)
```

### Error en cálculo de estadísticas
El programa incluye manejo de errores con `try/except` y valores por defecto para evitar que falle completamente.

---

## Historial de Cambios

### v1.1 (Marzo 2026)
- ✅ Añadido sistema de fallback para detección de manglar
- ✅ Clasificación espectral alternativa (NDVI, NDWI, CMRI)
- ✅ Manejo robusto de errores con `try/except`
- ✅ Mejor logging de fuentes de datos utilizadas
- ✅ CSV de manglar incluye columna "Metodo"

### v1.0 (Marzo 2026)
- Versión inicial basada en NATECHv3.py
- 12 pasos de análisis geoespacial
- Generación de reportes MD y LOG

---

## Autor

Generado para el proyecto MIA-R Puerto Nuevo Manzanillo  
Basado en la estructura de NATECHv3.py

---

## Licencia

Uso interno para proyecto de Manifestación de Impacto Ambiental.
