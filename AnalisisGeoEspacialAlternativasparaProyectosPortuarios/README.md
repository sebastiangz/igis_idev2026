# 🌊 Evaluación Comparativa de Alternativas para Proyectos Portuarios

**Optimización Multi-criterio con Algoritmos Genéticos, Google Earth Engine y QGIS**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GEE](https://img.shields.io/badge/Google%20Earth%20Engine-Enabled-brightgreen.svg)](https://earthengine.google.com/)

---

## 📋 Descripción

Este repositorio contiene una **metodología integral de evaluación comparativa de alternativas** para proyectos de desarrollo costero y portuario, aplicada específicamente al caso del **Puerto Nuevo Manzanillo en el Vaso II de la Laguna Cuyutlán, Colima, México** (311 hectáreas).

El sistema implementa técnicas avanzadas de optimización multi-objetivo mediante:

- 🧬 **Algoritmos Genéticos (NSGA-II)** - Optimización multi-objetivo y búsqueda de soluciones Pareto-óptimas
- 🛰️ **Google Earth Engine** - Análisis geoespacial de gran escala para criterios ambientales
- 🗺️ **QGIS Integration** - Análisis espacial y visualización cartográfica
- 📊 **PROMETHEE II** - Ranking robusto de alternativas con preferencias difusas
- 🎯 **Evaluación Multi-criterio** - 16 criterios en 4 categorías (Ambiental, Técnico, Social, Económico)

---

## 🎯 Objetivo

Proporcionar una **evaluación objetiva, transparente y científicamente fundamentada** de alternativas de ubicación para proyectos portuarios, cumpliendo con los requisitos de la **Manifestación de Impacto Ambiental (MIA)** en México, específicamente:

> "Presentar una evaluación comparativa de alternativas de al menos 3 sitios adicionales para la construcción del proyecto, incluyendo necesariamente la alternativa 'cero' (no construcción), variantes de ubicación y diseño."

---

## 🌟 Características Principales

### Evaluación Integral
- ✅ **5 Alternativas** evaluadas (incluyendo alternativa 0 y variantes de ubicación)
- ✅ **16 Criterios cuantitativos** organizados en 4 categorías
- ✅ **Ponderación por categoría**: Ambiental (60%), Técnico (30%), Social (15%), Económico (15%)
- ✅ **Normalización automática** de scores a escala [0-1]

### Criterios Ambientales (60%)
1. **Alteración Hidrodinámica** (15%) - Impacto en circulación y prisma de marea
2. **Calidad del Agua** (10%) - Degradación de parámetros fisicoquímicos
3. **Biodiversidad** (10%) - Especies afectadas (NOM-059)
4. **Superficie de Manglar** (15%) - Hectáreas de hábitat crítico afectado
5. **Residuos y Emisiones** (5%) - Generación de contaminantes
6. **Riesgo Inundación/Erosión** (5%) - Susceptibilidad a eventos extremos

### Tecnologías Utilizadas
- **Python 3.8+** - Lenguaje principal
- **DEAP** - Distributed Evolutionary Algorithms
- **Google Earth Engine API** - Análisis geoespacial
- **GeoPandas** - Manipulación de datos espaciales
- **NumPy/Pandas** - Procesamiento numérico y datos
- **Plotly** - Visualizaciones interactivas
- **Leaflet.js** - Mapas web interactivos

---

## 📁 Estructura del Proyecto

```
├── GA_ALTERNATIVAS_PUERTO_311HA.py          # Script principal
├── GA_VISUALIZACION_ALTERNATIVAS.py         # Módulo de visualización
├── PROPUESTA_MATRIZ_EVALUACION.docx         # Documentación metodológica
├── README.md                                # Este archivo
├── requirements.txt                         # Dependencias Python
├── capasSHP/                               # Shapefiles de entrada
│   ├── areaSAR.shp                         # Sistema Ambiental Regional
│   ├── manglar_distribucion.shp            # Distribución de manglar
│   ├── zona_busqueda_alternativas.shp      # Áreas de búsqueda
│   └── comunidades_locales.shp             # Poblaciones
├── capasRaster/                            # Datos raster
│   └── batimetria.tif                      # Modelo batimétrico
└── resultados_evaluacion_alternativas/     # Outputs generados
    ├── matriz_comparativa_alternativas.csv
    ├── ranking_promethee_alternativas.csv
    ├── tablas_comparativas_alternativas.xlsx
    ├── alternativas_evaluadas.geojson
    └── mapas_comparativos_alternativas.html
```

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- Cuenta de Google Earth Engine ([Registrarse aquí](https://earthengine.google.com/signup/))
- Node.js (para visualizaciones)

### Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/evaluacion-alternativas-puerto.git
cd evaluacion-alternativas-puerto
```

### Instalar Dependencias

```bash
# Instalar paquetes Python
pip install -r requirements.txt

# Autenticar Google Earth Engine (primera vez)
earthengine authenticate
```

### Archivo `requirements.txt`

```txt
earthengine-api>=0.1.350
geemap>=0.30.0
geopandas>=0.12.0
shapely>=2.0.0
deap>=1.4.0
numpy>=1.23.0
pandas>=1.5.0
matplotlib>=3.6.0
plotly>=5.14.0
openpyxl>=3.1.0
scikit-learn>=1.2.0
```

---

## 💻 Uso

### Ejecución Básica

```bash
python GA_ALTERNATIVAS_PUERTO_311HA.py
```

### Parámetros Configurables

Editar el script principal para ajustar:

```python
# Ubicación de datos
BASE = r"ruta/a/tus/datos"

# Configuración GEE
GEE_ACCOUNT = 'tu-email@example.com'
GEE_PROJECT = 'tu-proyecto-gee'

# Alternativas a evaluar
ALTERNATIVAS = [...]  # Modificar coordenadas y descripción

# Pesos de criterios
CRITERIOS = [...]  # Ajustar pesos según prioridades
```

### Flujo de Trabajo

1. **Preparar Datos de Entrada**
   - Shapefiles de áreas de interés
   - Distribución de manglar
   - Batimetría
   - Comunidades locales

2. **Ejecutar Evaluación**
   ```bash
   python GA_ALTERNATIVAS_PUERTO_311HA.py
   ```

3. **Revisar Resultados**
   - Tablas CSV/Excel con matriz de evaluación
   - Ranking PROMETHEE II
   - Mapas interactivos HTML
   - GeoJSON para visualización en QGIS

4. **Generar Visualizaciones**
   ```python
   from GA_VISUALIZACION_ALTERNATIVAS import generar_mapa_comparativo_html
   
   generar_mapa_comparativo_html(alternativas, evaluador, 'mapa.html')
   ```

---

## 📊 Salidas Generadas

### 1. Matriz de Evaluación CSV
Valores de todos los criterios para cada alternativa.

| Criterio | Categoría | Peso | ALT-0 | ALT-1 | ALT-2 | ALT-3 | ALT-4 |
|----------|-----------|------|-------|-------|-------|-------|-------|
| AMB-01   | Ambiental | 15%  | 0.0   | 7.5   | 6.0   | 3.0   | 5.5   |
| ...      | ...       | ...  | ...   | ...   | ...   | ...   | ...   |

### 2. Ranking PROMETHEE II

```
Ranking | Alternativa              | Flujo Neto | Score
--------|--------------------------|------------|-------
   1    | ALT-3 Zona Costera       |   0.2845   | 0.7234
   2    | ALT-2 Zona Norte         |   0.1523   | 0.6891
   3    | ALT-1 Vaso II (MIA)      |  -0.0234   | 0.6245
   4    | ALT-4 Zona Sur           |  -0.1456   | 0.5834
   5    | ALT-0 No Construcción    |  -0.2678   | 0.5000
```

### 3. Mapas Comparativos Interactivos

- Ubicación de alternativas con código de colores según score
- Capas de manglar, batimetría, comunidades
- Popups con información detallada
- Gráficos de radar y barras comparativos

### 4. Exportación a Excel Multi-hoja

- **Hoja 1**: Matriz de Evaluación
- **Hoja 2**: Scores Normalizados
- **Hoja 3**: Ranking PROMETHEE
- **Hoja 4**: Resumen por Categoría

---

## 🔬 Metodología

### 1. Algoritmo Genético NSGA-II

Optimización multi-objetivo que identifica el **frente de Pareto** de soluciones no dominadas:

- **Población**: 100 individuos
- **Generaciones**: 50
- **Operadores**: Cruce (85%), Mutación (15%)
- **Selección**: Torneo de 3 individuos

### 2. Google Earth Engine

Análisis geoespacial para criterios ambientales:

```python
# Ejemplo: Análisis de manglar afectado
manglar = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
area_afectada = manglar.clip(zona_proyecto).reduceRegion(
    reducer=ee.Reducer.sum(),
    scale=30
)
```

### 3. Normalización de Scores

Para criterios a **minimizar**:
```
score = (max - valor) / (max - min)
```

Para criterios a **maximizar**:
```
score = (valor - min) / (max - min)
```

### 4. PROMETHEE II

Cálculo de flujos de preferencia:

- **Flujo Positivo** Φ⁺(a): Suma de preferencias de 'a' sobre otras alternativas
- **Flujo Negativo** Φ⁻(a): Suma de preferencias de otras sobre 'a'
- **Flujo Neto** Φ(a) = Φ⁺(a) - Φ⁻(a)

Ranking final ordenado por flujo neto descendente.

---

## 🗺️ Integración con QGIS

### Cargar Resultados en QGIS

```python
# Importar capas desde Python
from qgis.core import QgsVectorLayer, QgsProject

# Cargar GeoJSON de alternativas
layer = QgsVectorLayer('alternativas_evaluadas.geojson', 
                       'Alternativas', 'ogr')
QgsProject.instance().addMapLayer(layer)

# Simbolizar por score
# (código de simbolización...)
```

### Visualización Recomendada

1. **Capa Base**: Imagen satelital o OpenStreetMap
2. **Capa de Alternativas**: Puntos con tamaño proporcional a score
3. **Capas de Contexto**: Manglar, batimetría, comunidades
4. **Etiquetas**: Mostrar ID y score de cada alternativa

---

## 📈 Análisis de Sensibilidad

El sistema incluye análisis de sensibilidad para evaluar robustez del ranking:

```python
# Variar peso de categoría Ambiental ±20%
for delta in [-20, -10, 0, 10, 20]:
    peso_ambiental_ajustado = 60 + delta
    # Recalcular scores...
    # Observar cambios en ranking
```

---

## 🔧 Personalización

### Agregar Nuevos Criterios

```python
CRITERIOS.append(
    CriterioEvaluacion(
        id_criterio="AMB-07",
        nombre="Captura de Carbono",
        categoria="Ambiental",
        peso=5.0,
        unidad="Ton CO2/año",
        tipo="maximizar",
        descripcion="Capacidad de captura de carbono del ecosistema"
    )
)
```

### Modificar Alternativas

```python
ALTERNATIVAS.append(
    Alternativa(
        id_alt="ALT-5",
        nombre="Alternativa 5 - Zona Este",
        descripcion="Nueva ubicación en zona este...",
        lon_centro=-104.2000,
        lat_centro=18.9500,
        area_ha=311.0
    )
)
```

### Ajustar Pesos de Categorías

Modificar los pesos individuales de criterios manteniendo suma = 100%:

```python
# Ejemplo: Mayor énfasis en criterios ambientales
criterio_amb01.peso = 20.0  # de 15.0 a 20.0
criterio_eco01.peso = 5.0   # de 7.0 a 5.0
# ... ajustar otros para mantener suma en 100%
```

---

## 🧪 Casos de Uso

### 1. Evaluación de Impacto Ambiental (MIA)

Cumplir con requisitos de autoridades ambientales para:
- Manifestaciones de Impacto Ambiental Modalidad Regional
- Estudios de Riesgo Ambiental
- Análisis de Alternativas (LGEEPA Art. 30)

### 2. Planificación Territorial

Selección óptima de ubicación para:
- Puertos y terminales marítimas
- Infraestructura costera
- Parques industriales
- Desarrollos turísticos

### 3. Análisis Costo-Beneficio

Comparación integral considerando:
- Costos de construcción y operación
- Beneficios sociales (empleo)
- Impactos ambientales (monetizados)
- Viabilidad técnica

### 4. Participación Ciudadana

Presentación transparente de alternativas para:
- Consultas públicas
- Talleres participativos
- Informes a comunidades locales

---

## 📚 Referencias

### Metodología
- Deb, K. et al. (2002). "A fast and elitist multiobjective genetic algorithm: NSGA-II". *IEEE Transactions on Evolutionary Computation*, 6(2), 182-197.
- Brans, J.P. & Vincke, P. (1985). "A Preference Ranking Organisation Method". *Management Science*, 31(6), 647-656.

### Aplicaciones Ambientales
- Corona, N. & Ramírez-Herrera, M.T. (2012). "Mapping and historical reconstruction of the tsunami event of 1932". *Natural Hazards*, 63, 1385-1402.
- CENAPRED (2022). "Riesgo de tsunami por deslizamiento submarino en la costa de Colima".

### Google Earth Engine
- Gorelick, N. et al. (2017). "Google Earth Engine: Planetary-scale geospatial analysis for everyone". *Remote Sensing of Environment*, 202, 18-27.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. **Fork** el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un **Pull Request**

### Áreas de Mejora

- [ ] Integración con más fuentes de datos (INEGI, CONABIO)
- [ ] Modelado hidrodinámico con Delft3D/MIKE
- [ ] Análisis de incertidumbre Monte Carlo
- [ ] Dashboard web interactivo
- [ ] Exportación automática a formatos MIA

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2026 [GAEGRUC]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [@tu-github](https://github.com/sebastiangz)

### Basado en
- **GA_VERTIMIENTOS_CUYUTLAN_v1.py** - Análisis de optimización de vertimientos con AG

---

## 📞 Contacto

- **Email**: sgonzalez@infraestructuragis.com
- **Proyecto**: [https://github.com/sebastiangz/evaluacion-alternativas-puerto](https://github.com/tu-usuario/evaluacion-alternativas-puerto)
- **Issues**: [https://github.com/sebastiangz/evaluacion-alternativas-puerto/issues](https://github.com/tu-usuario/evaluacion-alternativas-puerto/issues)

---

## 🙏 Agradecimientos

- Google Earth Engine por proporcionar acceso a datos geoespaciales
- Comunidad DEAP por las herramientas de algoritmos evolutivos
- QGIS Development Team por el software GIS de código abierto


---

## 📝 Changelog

### [1.0.0] - 2024-01-XX
#### Agregado
- Evaluación multi-criterio de 5 alternativas
- 16 criterios en 4 categorías
- Algoritmo NSGA-II para optimización
- Método PROMETHEE II para ranking
- Integración con Google Earth Engine
- Mapas interactivos HTML
- Exportación a Excel multi-hoja
- Documentación completa

#### Por Hacer
- Modelado hidrodinámico avanzado
- Integración con bases de datos CONABIO
- API REST para consultas
- Dashboard web interactivo

---

## 🔍 Keywords

`evaluación-ambiental` `algoritmos-genéticos` `nsga-ii` `promethee` `google-earth-engine` `qgis` `optimización-multiobjetivo` `analisis-espacial` `desarrollo-sostenible` `manifestación-impacto-ambiental` `evaluación-alternativas` `planificación-territorial` `infraestructura-costera` `python-geoespacial`

---

<div align="center">

**⭐ Si este proyecto te fue útil, por favor considera darle una estrella ⭐**

[Reportar Bug](https://github.com/tu-usuario/evaluacion-alternativas-puerto/issues) · [Solicitar Feature](https://github.com/tu-usuario/evaluacion-alternativas-puerto/issues) · [Documentación](https://github.com/tu-usuario/evaluacion-alternativas-puerto/wiki)

</div>
