# 📚 MANUAL DE USUARIO - INFRAESTRUCTURAGIS
## Guía para usuarios GAEGRUC: GeoNetwork y GeoServer

---

## 🎯 ¿QUÉ ES INFRAESTRUCTURAGIS?

**InfraestructuraGIS** es una plataforma que te permite:
- 📂 **Buscar** datos geográficos (mapas, capas, imágenes satelitales)
- 🗺️ **Visualizar** información en mapas interactivos
- 📥 **Descargar** datos para usarlos en tu trabajo
- 📤 **Publicar** tus propios datos geográficos
- 📊 **Analizar** información espacial

### Componentes principales:

| Herramienta | ¿Para qué sirve? | URL |
|-------------|------------------|-----|
| **GeoNetwork** | Catálogo para buscar y organizar datos | https://gis.infraestructuragis.com/geonetwork |
| **GeoServer** | Servidor para publicar y compartir mapas | https://gis.infraestructuragis.com/geoserver |

---

## 👤 PASO 1: ACCEDER AL SISTEMA

### 1.1 Abrir el Navegador

- Usa **Google Chrome**, **Firefox** o **Edge** (recomendado)
- Copia y pega esta dirección en tu navegador:
  ```
  https://gis.infraestructuragis.com
  ```

### 1.2 Iniciar Sesión

#### En GeoNetwork:
1. Ve a: https://gis.infraestructuragis.com/geonetwork
2. Click en **"Iniciar sesión"** (esquina superior derecha)
3. Ingresa:
   - **Usuario**: Tu correo (ejemplo: mauri@ucol.mx)
   - **Contraseña**: La que te proporcionó el administrador
4. Click en **"Entrar"**

#### En GeoServer:
1. Ve a: https://gis.infraestructuragis.com/geoserver/web
2. Click en **"Login"** (esquina superior derecha)
3. Ingresa las mismas credenciales
4. Click en **"Login"**

---

## 🔍 PARTE 1: USAR GEONETWORK (CATÁLOGO DE DATOS)

### ¿Qué puedo hacer en GeoNetwork?
- ✅ Buscar mapas y datos geográficos
- ✅ Ver información sobre los datos (metadatos)
- ✅ Descargar datos
- ✅ Publicar mis propios datos

---

### 📖 BUSCAR DATOS EN EL CATÁLOGO

#### Búsqueda Simple:

1. En la página principal de GeoNetwork
2. Escribe en el cuadro de búsqueda, por ejemplo:
   - "Colima"
   - "carreteras"
   - "límites municipales"
3. Presiona **Enter** o click en el ícono 🔍

#### Búsqueda Avanzada:

1. Click en **"Búsqueda avanzada"**
2. Puedes filtrar por:
   - **Categoría**: Mapas base, infraestructura, medio ambiente
   - **Tipo**: Vectorial, raster, servicios
   - **Fecha**: Cuándo se creó o actualizó
   - **Área geográfica**: Selecciona un área en el mapa

#### Ver Detalles de un Dato:

1. En los resultados, click en el **nombre** del dato
2. Verás información como:
   - 📝 Descripción: ¿Qué contiene?
   - 📅 Fecha: ¿Cuándo se creó?
   - 👤 Autor: ¿Quién lo hizo?
   - 📏 Extensión: ¿Qué área cubre?
   - 🔗 Enlaces: ¿Cómo descargarlo?

---

### 📥 DESCARGAR DATOS

1. En la página de detalles del dato
2. Ve a la sección **"Descargar y enlaces"**
3. Opciones disponibles:

   **Opción A: Descargar archivo completo**
   - Click en **"Descargar"** o **"Download"**
   - Elige el formato:
     - **Shapefile** (.zip) - Para QGIS, ArcGIS
     - **KML** - Para Google Earth
     - **GeoJSON** - Para aplicaciones web
   - El archivo se descargará en tu carpeta de Descargas

   **Opción B: Usar en un programa GIS**
   - Copia la URL del servicio **WMS** o **WFS**
   - Pégala en QGIS, ArcGIS o tu software favorito

---

### 📤 PUBLICAR TUS PROPIOS DATOS

#### PASO 1: Preparar tus datos

**Formatos aceptados:**
- ✅ Shapefile (.shp + .shx + .dbf + .prj en un ZIP)
- ✅ GeoTIFF (.tif, .tiff)
- ✅ KML/KMZ
- ✅ GeoJSON

**Verificar antes de subir:**
- ¿Tiene sistema de coordenadas definido?
- ¿Los nombres de archivos NO tienen espacios ni acentos?
- ¿El archivo es menor a 100 MB? (Si es mayor, contacta al administrador)

#### PASO 2: Crear metadatos en GeoNetwork

1. **Iniciar sesión** en GeoNetwork
2. Click en **"Contribuir"** (arriba)
3. Click en **"Añadir nuevo registro"**
4. Selecciona una plantilla:
   - **"Plantilla de datos vectoriales"** - Para shapefiles, KML
   - **"Plantilla de datos raster"** - Para imágenes, satélite

5. **Llenar la información:**

   📋 **Pestaña: Identificación**
   - **Título**: Nombre descriptivo (ej: "Límites Municipales de Colima 2024")
   - **Resumen**: Describe qué contiene (mínimo 50 palabras)
   - **Palabras clave**: carreteras, colima, infraestructura (separadas por coma)
   - **Categoría**: Selecciona la más apropiada

   📅 **Pestaña: Temporal**
   - **Fecha de creación**: ¿Cuándo se creó?
   - **Fecha de publicación**: ¿Cuándo se publicó?

   📍 **Pestaña: Espacial**
   - **Sistema de coordenadas**: EPSG:4326 (WGS84) o el que uses
   - **Extensión geográfica**: Dibuja un rectángulo en el mapa

   📞 **Pestaña: Contacto**
   - **Nombre**: Tu nombre
   - **Email**: Tu correo
   - **Organización**: Universidad de Colima

6. Click en **"Guardar"** (arriba a la derecha)
7. Click en **"Publicar"**

---

## 🗺️ PARTE 2: USAR GEOSERVER (PUBLICAR MAPAS)

### ¿Qué puedo hacer en GeoServer?
- ✅ Subir datos geográficos (shapefiles, GeoTIFF)
- ✅ Convertir datos en servicios web (WMS, WFS)
- ✅ Crear estilos para visualizar datos
- ✅ Publicar mapas en internet

---

### 📤 PUBLICAR UN SHAPEFILE

**IMPORTANTE**: GeoServer está instalado en un servidor remoto, por lo que hay dos formas de publicar datos:

#### OPCIÓN A: Subir archivo al servidor PRIMERO (RECOMENDADO para principiantes)

**Paso 1: Subir tu archivo al servidor**

Necesitas transferir tu archivo al servidor usando una de estas opciones:

**Opción 1A: Usar WinSCP (Windows) o FileZilla**
1. Descarga e instala **WinSCP** (https://winscp.net) o **FileZilla**
2. Conecta al servidor:
   - **Host**: 192.168.40.100
   - **Puerto**: 22
   - **Usuario**: igis
   - **Contraseña**: [Solicítala al administrador]
3. Navega a: `/home/igis/uploads/` (o la carpeta que te indiquen)
4. Arrastra tu archivo ZIP desde tu computadora a esta carpeta
5. ¡Listo! Tu archivo ya está en el servidor

**Opción 1B: Usar scp desde línea de comandos (Linux/Mac)**
```bash
scp mi_shapefile.zip igis@192.168.40.100:/home/igis/uploads/
```

**Paso 2: Usar el Importer en GeoServer**

1. **Iniciar sesión** en GeoServer: https://gis.infraestructuragis.com/geoserver/web
2. En el menú izquierdo, click en **"Importer"**
3. Click en **"Importar datos"** o **"Import data"**

4. **Seleccionar archivo del servidor:**
   - En **"Choose a data source"** selecciona: **"Server files"**
   - Navega a la carpeta donde subiste tu archivo: `/home/igis/uploads/`
   - Selecciona tu archivo ZIP
   - Click en **"Siguiente"** o **"Next"**

5. **Configurar:**
   - **Workspace**: Selecciona `infraestructuragis` (o el que te asignaron)
   - **Store**: Se creará automáticamente
   - **Layer name**: Pon un nombre sin espacios (ej: `municipios_colima`)
   - **Projection**: Verifica que sea correcta (ej: EPSG:4326)
   - Click en **"Importar"** o **"Import"**

6. **¡Listo!** Tu capa ya está publicada

**NOTA**: Si no tienes acceso SSH al servidor, solicita al administrador que cree una carpeta de carga compartida o que suba tus archivos por ti.

---

#### OPCIÓN B: Método Manual (Sin necesidad de SSH)

Este método NO requiere subir archivos por SSH, pero es más técnico:

1. **Crear un Data Store:**
   - Menú izquierdo → **"Stores"** (Almacenes)
   - Click en **"Add new Store"**
   - Selecciona el tipo de dato:
     - **"Shapefile"** - Para archivos .shp
     - **"Directory of spatial files"** - Para múltiples shapefiles
     - **"PostGIS"** - Si tus datos ya están en PostgreSQL
     - **"GeoTIFF"** - Para imágenes raster

2. **Configurar el Store:**
   
   **Para Shapefile:**
   - **Data Source Name**: `mi_shapefile_2024`
   - **URL**: Escribe la ruta donde el administrador subió tu archivo
     - Ejemplo: `file:///home/igis/uploads/mi_archivo.shp`
   - Click en **"Save"**

   **Para PostGIS (si tus datos están en la base de datos):**
   - **Data Source Name**: `mi_datos_postgis`
   - **host**: `127.0.0.1`
   - **port**: `5432`
   - **database**: `geodata_mia`
   - **user**: [Tu usuario de base de datos]
   - **password**: [Tu contraseña]
   - Click en **"Save"**

3. **Publicar la capa:**
   - Te redirigirá a "New Layer"
   - Click en **"Publish"** junto a tu capa
   - **Llenar información básica:**
     - **Name**: Nombre técnico sin espacios (ej: `carreteras_col`)
     - **Title**: Nombre descriptivo (ej: "Red Carretera de Colima")
     - **Abstract**: Descripción breve
   - **Pestaña "Data"**:
     - Click en **"Compute from data"** (Native Bounding Box)
     - Click en **"Compute from native bounds"** (Lat/Lon Bounding Box)
   - **Pestaña "Publishing"**:
     - Verifica el sistema de coordenadas (SRS)
     - Selecciona un estilo por defecto
   - Click en **"Save"** (abajo)

---

#### OPCIÓN C: Solicitar al Administrador (MÁS SIMPLE)

Si no te sientes cómodo con las opciones anteriores:

1. Envía tu archivo ZIP por email a: sgonzalez@infraestructuragis.com
2. Incluye en el email:
   - Nombre que quieres para la capa
   - Descripción breve
   - Sistema de coordenadas (si lo sabes)
   - Si debe ser pública o privada
3. El administrador lo publicará y te enviará el enlace WMS/WFS

---

1. **Crear un Data Store:**
   - Menú izquierdo → **"Stores"** (Almacenes)
   - Click en **"Add new Store"**
   - Selecciona **"Shapefile"** o el tipo de dato que tienes
   - **Data Source Name**: `mi_shapefile_2024`
   - **Connection Parameters**:
     - **URL**: Click en **"Browse"** y sube tu archivo
   - Click en **"Save"**

2. **Publicar la capa:**
   - Te redirigirá a "New Layer"
   - Click en **"Publish"** junto a tu capa
   - **Llenar información básica:**
     - **Name**: Nombre técnico sin espacios
     - **Title**: Nombre descriptivo
     - **Abstract**: Descripción breve
   - **Pestaña "Data"**:
     - Click en **"Compute from data"** (Native Bounding Box)
     - Click en **"Compute from native bounds"** (Lat/Lon Bounding Box)
   - Click en **"Save"** (abajo)

---

### 🎨 CREAR ESTILOS PARA MAPAS

Los estilos controlan cómo se ven tus datos en el mapa (colores, grosor de líneas, símbolos).

#### Estilo Básico con el Editor Visual:

1. **Ir a Styles:**
   - Menú izquierdo → **"Styles"** (Estilos)
   - Click en **"Add a new style"**

2. **Configurar:**
   - **Name**: `estilo_carreteras_azul`
   - **Workspace**: `infraestructuragis`
   - **Format**: Selecciona **"CSS"** (más fácil que SLD)

3. **Escribir el estilo:**

   **Para líneas (carreteras, ríos):**
   ```css
   * {
     stroke: #0066cc;
     stroke-width: 2px;
   }
   ```

   **Para polígonos (municipios, predios):**
   ```css
   * {
     fill: #ffcc00;
     fill-opacity: 0.5;
     stroke: #333333;
     stroke-width: 1px;
   }
   ```

   **Para puntos (ciudades, sitios):**
   ```css
   * {
     mark: symbol(circle);
     mark-size: 8px;
     mark-fill: #ff0000;
     mark-stroke: white;
     mark-stroke-width: 1px;
   }
   ```

4. Click en **"Validate"** para verificar
5. Click en **"Submit"** para guardar

#### Aplicar el estilo a una capa:

1. Menú izquierdo → **"Layers"** (Capas)
2. Click en tu capa
3. Pestaña **"Publishing"**
4. En **"Default Style"**: Selecciona tu estilo
5. Click en **"Save"**

---

### 🔍 USAR WPS (ANÁLISIS ESPACIAL)

WPS te permite hacer análisis directamente en el servidor sin descargar datos.

#### Ejemplo: Crear un Buffer (Área de Influencia)

1. Menú izquierdo → **"Demos"**
2. Click en **"WPS Request Builder"**
3. **Seleccionar proceso:**
   - En "Choose process": Busca **"geo:buffer"**
4. **Configurar parámetros:**
   - **features**: Selecciona tu capa de entrada
   - **distance**: Distancia del buffer (ejemplo: 100 para 100 metros)
5. Click en **"Execute process"**
6. Los resultados se pueden:
   - Visualizar en el mapa
   - Descargar como shapefile
   - Guardar como nueva capa

#### Otros análisis disponibles:

- **Intersección**: ¿Qué elementos se cruzan?
- **Unión**: Combinar dos capas
- **Clip**: Recortar una capa con otra
- **Centroide**: Calcular el centro de polígonos
- **Área**: Calcular áreas y perímetros

---

## 🔗 USAR TUS DATOS EN OTRAS APLICACIONES

### Conectar con QGIS:

**QGIS** es un software GIS gratuito y de código abierto. Descárgalo en: https://qgis.org

#### Agregar capa WMS en QGIS:

1. Abrir QGIS
2. Menú **"Capa"** → **"Añadir capa"** → **"Añadir capa WMS/WMTS"**
3. Click en **"Nuevo"** para crear una conexión
4. **Configurar:**
   - **Nombre**: InfraestructuraGIS
   - **URL**: `https://gis.infraestructuragis.com/geoserver/wms`
5. Click en **"Aceptar"**
6. Click en **"Conectar"**
7. Selecciona las capas que quieres agregar
8. Click en **"Añadir"**

#### Agregar capa WFS en QGIS (para edición):

1. Menú **"Capa"** → **"Añadir capa"** → **"Añadir capa WFS"**
2. Click en **"Nuevo"**
3. **Configurar:**
   - **Nombre**: InfraestructuraGIS WFS
   - **URL**: `https://gis.infraestructuragis.com/geoserver/wfs`
   - **Versión**: 2.0.0
4. Click en **"Aceptar"**
5. Click en **"Conectar"**
6. Selecciona tus capas
7. Click en **"Añadir"**

**Ventaja de WFS**: Puedes descargar los datos como shapefile para trabajar offline.

---

### Conectar con ArcGIS Desktop / ArcMap:

**ArcGIS Desktop** es el software GIS profesional de ESRI.

#### Agregar capa WMS en ArcMap:

1. Abrir ArcMap
2. Click en el botón **"Add Data"** (ícono +)
3. En el diálogo, click en **"GIS Servers"** (en el panel izquierdo)
4. Doble click en **"Add WMS Server"**
5. **Configurar:**
   - **URL**: `https://gis.infraestructuragis.com/geoserver/wms`
   - Click en **"Get Layers"** (Obtener capas)
6. Click en **"OK"**
7. Ahora en "GIS Servers" verás tu conexión
8. Doble click en ella y selecciona las capas a agregar
9. Click en **"Add"**

#### Agregar capa WFS en ArcMap:

1. En ArcCatalog (o desde ArcMap: Windows → Catalog)
2. Navega a **"Interoperability Connections"**
3. Right-click → **"Add Interoperability Connection"**
4. **Configurar:**
   - **Format**: WFS
   - **Dataset**: `https://gis.infraestructuragis.com/geoserver/wfs`
5. Click en **"OK"**
6. Las capas WFS ahora aparecerán en el catálogo
7. Arrastra la capa que necesites a tu mapa

**NOTA**: Para WFS en ArcMap necesitas tener instalada la extensión **"Data Interoperability"**.

#### Alternativa: Descargar y usar como Shapefile

Si no tienes Data Interoperability:

1. En GeoServer, ve a tu capa
2. Click en **"Layer Preview"**
3. En el menú desplegable, selecciona **"Shapefile"**
4. El archivo ZIP se descarga automáticamente
5. Descomprímelo
6. En ArcMap: Add Data → Selecciona el .shp descargado

---

### Conectar con ArcGIS Pro:

**ArcGIS Pro** es la versión moderna de ESRI.

#### Agregar servidor WMS en ArcGIS Pro:

1. En el panel **"Catalog"**, right-click en **"Servers"**
2. Selecciona **"New WMS Server"**
3. **Configurar:**
   - **Server URL**: `https://gis.infraestructuragis.com/geoserver/wms`
   - **Nombre**: InfraestructuraGIS
4. Click en **"OK"**
5. Expande "Servers" → Tu conexión → Selecciona capas
6. Arrastra las capas al mapa o right-click → **"Add to Current Map"**

#### Agregar servidor WFS en ArcGIS Pro:

1. En el panel **"Catalog"**, right-click en **"Servers"**
2. Selecciona **"New WFS Server"**
3. **Configurar:**
   - **Server URL**: `https://gis.infraestructuragis.com/geoserver/wfs`
   - **Version**: 2.0.0
   - **Nombre**: InfraestructuraGIS WFS
4. Click en **"OK"**
5. Expande la conexión y arrastra las capas al mapa

**Ventajas en ArcGIS Pro**:
- Mejor rendimiento con WFS
- Soporte nativo para WFS 2.0
- No requiere Data Interoperability

---

### Ver en Google Earth:

1. En GeoServer, ve a tu capa
2. Click en **"Layer Preview"** (menú izquierdo)
3. Busca tu capa en la lista
4. En la columna **"Common Formats"**, click en **"KML"**
5. El archivo .kml se descarga automáticamente
6. Doble click en el archivo
7. Google Earth se abrirá automáticamente con tu capa

**Alternativa - KMZ (comprimido):**
- Usa **"KMZ"** en lugar de KML si tu capa tiene muchos datos
- Es más rápido de cargar en Google Earth

---

### Usar en aplicaciones web personalizadas:

Si tienes una página web propia y quieres integrar los mapas:

#### Con OpenLayers (JavaScript):

```javascript
// Agregar capa WMS
var wmsLayer = new ol.layer.Tile({
  source: new ol.source.TileWMS({
    url: 'https://gis.infraestructuragis.com/geoserver/wms',
    params: {
      'LAYERS': 'infraestructuragis:mi_capa',
      'TILED': true
    }
  })
});

map.addLayer(wmsLayer);
```

#### Con Leaflet (JavaScript):

```javascript
// Agregar capa WMS
var wmsLayer = L.tileLayer.wms(
  'https://gis.infraestructuragis.com/geoserver/wms', {
    layers: 'infraestructuragis:mi_capa',
    format: 'image/png',
    transparent: true
  }
);

map.addLayer(wmsLayer);
```

#### Con ArcGIS API for JavaScript:

```javascript
// Agregar capa WMS
var wmsLayer = new WMSLayer({
  url: "https://gis.infraestructuragis.com/geoserver/wms",
  sublayers: [{
    name: "infraestructuragis:mi_capa"
  }]
});

map.add(wmsLayer);
```

---

## 📋 BUENAS PRÁCTICAS

### ✅ Al nombrar archivos y capas:

- ✅ Usa minúsculas: `municipios_colima`
- ✅ Usa guiones bajos en lugar de espacios: `red_carreteras`
- ✅ Sé descriptivo: `infraestructura_educativa_2024`
- ❌ Evita: `Mapa Final (1) copia.shp`

### ✅ Al crear metadatos:

- ✅ Título claro y descriptivo
- ✅ Resumen de al menos 100 palabras
- ✅ Incluye palabras clave relevantes
- ✅ Especifica la fuente de los datos
- ✅ Indica la fecha de los datos

### ✅ Al publicar datos:

- ✅ Verifica que el sistema de coordenadas sea correcto
- ✅ Prueba la visualización antes de compartir
- ✅ Documenta qué contiene cada campo de la tabla de atributos
- ✅ Asigna permisos apropiados (público/privado)

---

## ❓ PREGUNTAS FRECUENTES

### P: ¿Puedo ver los datos sin iniciar sesión?
**R**: Sí, los datos públicos se pueden ver sin cuenta. Solo necesitas cuenta para publicar datos.

### P: ¿Qué tamaño máximo tienen los archivos?
**R**: Generalmente hasta 100 MB por archivo. Para archivos más grandes, contacta al administrador.

### P: ¿En qué sistema de coordenadas debo subir mis datos?
**R**: Lo ideal es EPSG:4326 (WGS84) o EPSG:6372 (ITRF2008 México). Si usas otro, GeoServer puede reproyectar automáticamente.

### P: ¿Cómo sé si mis datos se publicaron correctamente?
**R**: Ve a "Layer Preview" en GeoServer y visualiza tu capa. Si se ve bien, está correcta.

### P: ¿Puedo editar datos ya publicados?
**R**: Sí, puedes actualizar tanto los datos como los metadatos en cualquier momento.

### P: Olvidé mi contraseña, ¿qué hago?
**R**: Contacta al administrador del sistema para que la restablezca.

### P: ¿Cómo elimino una capa que ya no necesito?
**R**: En GeoServer, ve a "Layers", selecciona tu capa y click en "Remove". IMPORTANTE: Primero elimina de GeoServer, luego de GeoNetwork.

---

## 🆘 SOPORTE TÉCNICO

### ¿Necesitas ayuda?

📧 **Email**: sgonzalez@infraestructuragis.com
🌐 **Portal**: https://gis.infraestructuragis.com
📞 **Teléfono**: [Agregar número]

### Recursos adicionales:

- 📖 Documentación GeoNetwork: https://geonetwork-opensource.org/manuals/trunk/en/user-guide/
- 📖 Documentación GeoServer: https://docs.geoserver.org/stable/en/user/
- 🎥 Tutoriales en video: [Agregar enlaces]

---

## 📝 GLOSARIO DE TÉRMINOS

| Término | Significado |
|---------|-------------|
| **Shapefile** | Formato de archivo vectorial para almacenar ubicaciones y atributos de puntos, líneas y polígonos |
| **GeoTIFF** | Formato de imagen georreferenciada (con coordenadas) |
| **WMS** | Web Map Service - Servicio para ver mapas como imágenes |
| **WFS** | Web Feature Service - Servicio para descargar datos vectoriales |
| **CSW** | Catalog Service for the Web - Servicio de catálogo para buscar metadatos |
| **WPS** | Web Processing Service - Servicio para análisis espacial en línea |
| **Capa** | Conjunto de datos geográficos (ej: capa de carreteras, capa de municipios) |
| **Metadatos** | Información sobre los datos (quién, cuándo, dónde, cómo) |
| **Buffer** | Área de influencia alrededor de un elemento geográfico |
| **EPSG** | Código numérico que identifica un sistema de coordenadas |
| **Workspace** | Espacio de trabajo para organizar capas en GeoServer |

---

## ✨ CASOS DE USO COMUNES

### Caso 1: "Quiero compartir mi mapa con un colega"

1. Publica tu shapefile en GeoServer (Importador)
2. Ve a "Layer Preview"
3. Copia la URL del servicio WMS
4. Envía la URL a tu colega
5. Tu colega puede ver el mapa en QGIS o en un navegador

### Caso 2: "Necesito calcular áreas de influencia de 500m alrededor de escuelas"

1. Publica tu capa de escuelas en GeoServer
2. Usa WPS → Process "geo:buffer"
3. Distancia: 500 metros
4. Ejecuta el proceso
5. Descarga el resultado como shapefile

### Caso 3: "Quiero encontrar todos los mapas de Colima"

1. Ve a GeoNetwork
2. Búsqueda simple: "Colima"
3. Filtra por tipo de dato si es necesario
4. Explora los resultados
5. Descarga los que necesites

---

**Última actualización**: Marzo 2026  
**Versión del manual**: 1.0  
**Elaborado por**: InfraestructuraGIS - MIA
