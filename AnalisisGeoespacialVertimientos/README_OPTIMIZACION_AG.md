
# SISTEMA DE OPTIMIZACIÓN DE VERTIMIENTOS CON ALGORITMOS GENÉTICOS

# Puerto Nuevo Manzanillo - Laguna de Cuyutlán, Colima

## &#x20;DESCRIPCIÓN

Sistema de optimización multi-objetivo para encontrar la ubicación óptima
de zonas de vertimiento de material dragado (\~45 millones m³), considerando:

* **Riesgo de tsunami**: Distancia a cañones submarinos (origen del tsunami de 1932)
* **Costo operativo**: Distancia al puerto de Manzanillo
* **Impacto ambiental**: Afectación a ecosistemas bentónicos
* **Estabilidad del fondo**: Pendiente del lecho marino

## 📁 ESTRUCTURA DE ARCHIVOS

```
OptimizacionVertimientos/
│
├── capasSHP/                          # Shapefiles de entrada
│   ├── areaSAR.shp                    # Área del Sistema Ambiental Regional
│   ├── canones\\\_submarinos.shp         # Ubicación de cañones submarinos
│   ├── zona\\\_busqueda\\\_vertimiento.shp  # Área de búsqueda para optimización
│   └── infraestructura\\\_critica.shp    # Instalaciones críticas (opcional)
│
├── resultados\\\_optimizacion\\\_AG/        # Resultados generados
│   ├── soluciones\\\_pareto.geojson      # Soluciones óptimas en formato GeoJSON
│   ├── soluciones\\\_pareto.csv          # Tabla de soluciones con métricas
│   ├── frente\\\_pareto\\\_3d.html          # Visualización 3D interactiva
│   ├── mapa\\\_optimizacion\\\_vertimiento.html  # Mapa con capas GEE
│   └── evolucion\\\_algoritmo.csv        # Estadísticas de convergencia
│
├── _v1.py     # Script principal de optimización
├── _PARETO.py         # Módulo de visualización
└── README.md                          # Este archivo
```

## 🔧 REQUISITOS

### Dependencias Python

```bash
pip install earthengine-api geemap geopandas shapely deap numpy
pip install matplotlib plotly  # Para visualización
```

### Google Earth Engine

1. Crear cuenta en: https://earthengine.google.com/
2. Crear proyecto en Google Cloud Console
3. Habilitar Earth Engine API
4. Autenticarse:

```python
import ee
ee.Authenticate()
ee.Initialize(project='tu-proyecto-gee')
```

## 📊 SHAPEFILES REQUERIDOS

### 1\. areaSAR.shp (Polígono)

Área del Sistema Ambiental Regional que delimita la zona de estudio.

**Atributos mínimos:**

|Campo|Tipo|Descripción|
|-|-|-|
|NOMBRE|String|Nombre del área|
|AREA\_KM2|Double|Área en kilómetros cuadrados|

### 2\. canones\_submarinos.shp (Puntos)

Ubicación de los cañones submarinos que representan riesgo de tsunami.

**Atributos requeridos:**

|Campo|Tipo|Descripción|
|-|-|-|
|NOMBRE|String|Identificador del cañón|
|PROF\_M|Double|Profundidad de la cabecera (metros)|
|RIESGO|String|Nivel de riesgo (ALTO/MEDIO/BAJO)|
|TSUNAMI\_32|Int|1 si está asociado al tsunami de 1932|

**Coordenadas de referencia (Tsunami 1932):**

* Cañón 1: 18°49'0.59"N, 104°3'13.59"W
* Cañón 2: 18°54'13.88"N, 104°15'16.49"W

### 3\. zona\_busqueda\_vertimiento.shp (Polígono)

Área donde el algoritmo buscará ubicaciones óptimas.

**Atributos mínimos:**

|Campo|Tipo|Descripción|
|-|-|-|
|NOMBRE|String|Identificador de la zona|
|PROF\_MIN\_M|Double|Profundidad mínima permitida|
|PROF\_MAX\_M|Double|Profundidad máxima permitida|
|DIST\_COSTA\_M|Double|Distancia mínima a la costa|

### 4\. infraestructura\_critica.shp (Puntos) - Opcional

Instalaciones críticas para análisis de efecto dominó.

**Atributos:**

|Campo|Tipo|Descripción|
|-|-|-|
|NOMBRE|String|Nombre de la instalación|
|TIPO|String|Tipo (GNL/GAS/TANQUE/CFE/etc)|
|BUFFER\_M|Double|Radio de impacto en metros|

## ⚙️ CONFIGURACIÓN

Editar las siguientes variables en `_v1.py`:

```python
# Rutas de archivos
BASE = r"D:\\\\tu\\\\ruta\\\\OptimizacionVertimientos"
SHAPEFILE\\\_ROI = os.path.join(BASE, "capasSHP", "areaSAR.shp")
SHAPEFILE\\\_CANONES = os.path.join(BASE, "capasSHP", "canones\\\_submarinos.shp")

# Credenciales GEE
GEE\\\_PROJECT = 'tu-proyecto-gee'

# Parámetros del algoritmo genético
PARAMS\\\_AG = {
    'tamano\\\_poblacion': 100,  # Más población = mejor exploración
    'num\\\_generaciones': 50,   # Más generaciones = mejor convergencia
    'prob\\\_cruce': 0.85,
    'prob\\\_mutacion': 0.15,
}

# Restricciones del problema
RESTRICCIONES = {
    'distancia\\\_canon\\\_min\\\_m': 7400,     # 7.4 km (MIA actual)
    'distancia\\\_canon\\\_ideal\\\_m': 15000,  # 15 km (recomendación)
    'profundidad\\\_min\\\_m': -50,
    'pendiente\\\_max\\\_grados': 15,
}
```

## 🚀 EJECUCIÓN

### Opción 1: Desde línea de comandos

```bash
python D:\\ownCloud\\Python\\AnalisisGeoespacialVertimientos\\\_v1.py
```

### Opción 2: Desde QGIS

1. Abrir QGIS 3.x
2. Plugins → Python Console
3. Ejecutar:

```python
exec(open(r'D:\\\\ownCloud\\\\Python\\AnalisisGeoespacialVertimientos\\\\\_v1.py').read())
```

### Opción 3: Como módulo

```python
from D:\\\\ownCloud\\\\Python\\AnalisisGeoespacialVertimientos\\\\\_v1 import main, cargar\\\_capas\\\_qgis
main()
cargar\\\_capas\\\_qgis()  # Carga resultados en QGIS
```

## 📈 INTERPRETACIÓN DE RESULTADOS

### Frente de Pareto

El algoritmo NSGA-II genera un conjunto de soluciones **Pareto-óptimas**,
donde ninguna solución es mejor que otra en todos los objetivos simultáneamente.

**Objetivos (todos a minimizar):**

1. **Riesgo**: Combinación de distancia inversa a cañones + pendiente del fondo
2. **Costo**: Distancia al puerto de Manzanillo
3. **Impacto**: Afectación a ecosistemas según profundidad

### Clasificación de soluciones

|Dist. a Cañón|Estado|Color|
|-|-|-|
|≥ 15 km|✅ Cumple distancia IDEAL|Verde|
|7.4 - 15 km|⚠️ Cumple MÍNIMO MIA|Amarillo|
|< 7.4 km|❌ NO cumple|Rojo|

### Archivos de salida

**soluciones\_pareto.csv:**

```csv
ranking,longitud,latitud,dist\\\_canon\\\_km,dist\\\_puerto\\\_km,profundidad\\\_m,pendiente\\\_grados,fitness\\\_1,fitness\\\_2,fitness\\\_3,cumple\\\_restricciones
1,-104.3521,18.8234,18.52,25.31,-95.2,8.3,2.14,25.31,1.5,SI
2,-104.2876,18.8512,15.21,18.74,-82.1,10.1,3.21,18.74,2.1,SI
...
```

**frente\_pareto\_3d.html:**
Visualización interactiva 3D del frente de Pareto con Plotly.

## 🔬 METODOLOGÍA

### Algoritmo NSGA-II (Non-dominated Sorting Genetic Algorithm II)

1. **Inicialización**: Población aleatoria dentro de zona de búsqueda
2. **Evaluación**: Cada individuo se evalúa con GEE (batimetría, pendiente)
3. **Selección**: Por dominancia de Pareto y distancia de crowding
4. **Cruce**: Simulated Binary Crossover (SBX)
5. **Mutación**: Polynomial Mutation
6. **Iteración**: Hasta alcanzar número de generaciones

### Función de evaluación con GEE

```python
def evaluar\\\_individuo(lon, lat):
    # Datos de Google Earth Engine
    profundidad = GEBCO.sample(punto)
    pendiente = ee.Terrain.slope(GEBCO).sample(punto)
    
    # Cálculo de objetivos
    riesgo = f(dist\\\_canon, pendiente, corrientes)
    costo = distancia\\\_puerto(lon, lat)
    impacto = g(profundidad, ecosistemas)
    
    return (riesgo, costo, impacto)
```

## 📚 REFERENCIAS

* Corona, N., \& Ramírez-Herrera, M.T. (2012). Mapping and historical
reconstruction of the great Mexican 22 June 1932 tsunami.
* CENAPRED (2022). Atlas Nacional de Riesgos - Tsunamis.
* Deb, K. (2002). A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II.
* Hühnerbach, V., \& Masson, D.G. (2004). Landslides in the North Atlantic
and its adjacent seas.

## 👥 AUTORES

Basado en NATECHv3.py (sgz) - Mejorado con Algoritmos Genéticos por GAEGRUC
Proyecto: MIA Puerto Nuevo Manzanillo, Colima
Fecha: 2026

## 📄 LICENCIA

Uso académico y profesional para evaluación de impacto ambiental.

