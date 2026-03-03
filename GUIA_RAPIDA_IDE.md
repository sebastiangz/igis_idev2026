# 📋 GUÍA RÁPIDA DE REFERENCIA
## InfraestructuraGIS - Universidad de Colima

---

## 🔗 ACCESOS RÁPIDOS

| Servicio | URL |
|----------|-----|
| **GeoNetwork** (Catálogo) | https://gis.infraestructuragis.com/geonetwork |
| **GeoServer** (Mapas) | https://gis.infraestructuragis.com/geoserver |

---

## 🚀 TAREAS COMUNES

### 1️⃣ BUSCAR DATOS
```
1. Ir a GeoNetwork
2. Escribir en el buscador (ej: "Colima")
3. Click en resultado para ver detalles
4. Descargar o usar el servicio WMS/WFS
```

### 2️⃣ SUBIR UN SHAPEFILE
```
PASO 1: Subir archivo al servidor
  1. Usar WinSCP o FileZilla
  2. Conectar a: 192.168.40.100 (usuario: igis)
  3. Subir ZIP a: /home/igis/uploads/

PASO 2: Importar en GeoServer
  1. GeoServer → Login → Importer
  2. Choose data source: "Server files"
  3. Navegar a /home/igis/uploads/
  4. Seleccionar tu ZIP → Next
  5. Workspace: infraestructuragis
  6. Import
  
Alternativa: Enviar archivo por email a admin
```

### 3️⃣ CREAR METADATOS
```
1. GeoNetwork → Login
2. Contribuir → Añadir nuevo registro
3. Llenar formulario (mínimo: título, resumen, palabras clave)
4. Guardar → Publicar
```

### 4️⃣ CAMBIAR ESTILO DE CAPA
```
1. GeoServer → Styles → Add new style
2. Nombre: mi_estilo
3. Format: CSS
4. Escribir estilo (ver ejemplos abajo)
5. Submit
6. Layers → Tu capa → Publishing → Default Style → Seleccionar
7. Save
```

### 5️⃣ USAR EN QGIS
```
1. QGIS → Capa → Añadir capa WMS/WMTS
2. Nueva conexión:
   - Nombre: InfraestructuraGIS
   - URL: https://gis.infraestructuragis.com/geoserver/wms
3. Conectar → Seleccionar capas → Añadir
```

### 6️⃣ USAR EN ARCGIS/ARCMAP
```
ArcMap:
1. Add Data → GIS Servers
2. Add WMS Server
3. URL: https://gis.infraestructuragis.com/geoserver/wms
4. Get Layers → OK
5. Doble click en conexión → Seleccionar capas

ArcGIS Pro:
1. Catalog → Servers → New WMS Server
2. URL: https://gis.infraestructuragis.com/geoserver/wms
3. OK → Arrastrar capas al mapa
```

### 7️⃣ DESCARGAR COMO SHAPEFILE (Para usar offline)
```
1. GeoServer → Layer Preview
2. Buscar tu capa
3. Formato: Shapefile
4. Se descarga ZIP
5. Descomprimir y usar en QGIS/ArcGIS
```

---

## 🎨 ESTILOS CSS RÁPIDOS

### Líneas (carreteras, ríos):
```css
* {
  stroke: #0066cc;
  stroke-width: 2px;
}
```

### Polígonos (municipios, predios):
```css
* {
  fill: #ffcc00;
  fill-opacity: 0.6;
  stroke: #333;
  stroke-width: 1px;
}
```

### Puntos (ciudades, sitios):
```css
* {
  mark: symbol(circle);
  mark-size: 10px;
  mark-fill: #ff0000;
}
```

### Por categorías (ejemplo: por población):
```css
[poblacion < 10000] {
  mark-size: 6px;
  mark-fill: #yellow;
}

[poblacion >= 10000] [poblacion < 50000] {
  mark-size: 10px;
  mark-fill: #orange;
}

[poblacion >= 50000] {
  mark-size: 14px;
  mark-fill: #red;
}
```

---

## 📐 ANÁLISIS WPS COMUNES

### Buffer (área de influencia):
```
Process: geo:buffer
Input: Tu capa
Distance: 500 (metros)
```

### Intersección:
```
Process: geo:Intersect
First feature: Capa 1
Second feature: Capa 2
```

### Calcular área:
```
Process: geo:Area
Features: Tu capa de polígonos
```

---

## 🗂️ SISTEMAS DE COORDENADAS COMUNES

| Código EPSG | Nombre | Uso |
|-------------|--------|-----|
| **EPSG:4326** | WGS84 | GPS, Google Earth, uso general |
| **EPSG:3857** | Web Mercator | Google Maps, OpenStreetMap |
| **EPSG:6372** | ITRF2008 México | Proyección oficial México |
| **EPSG:32614** | UTM Zona 14N | Colima y occidente de México |

---

## 📂 FORMATOS DE DATOS SOPORTADOS

### Vectoriales:
- ✅ **Shapefile** (.shp + archivos asociados en ZIP)
- ✅ **GeoJSON** (.geojson)
- ✅ **KML/KMZ** (Google Earth)
- ✅ **GML** (Geography Markup Language)
- ✅ **GPX** (GPS tracks)

### Raster:
- ✅ **GeoTIFF** (.tif, .tiff)
- ✅ **ECW** (ER Mapper)
- ✅ **JPEG2000** (.jp2)
- ✅ **PNG/JPG** (con world file)
- ✅ **ASCII Grid** (.asc)

---

## 🔑 SERVICIOS OGC

### WMS (Web Map Service):
```
URL: https://gis.infraestructuragis.com/geoserver/wms
Uso: Ver mapas como imágenes
GetCapabilities: ?request=GetCapabilities&service=WMS
```

### WFS (Web Feature Service):
```
URL: https://gis.infraestructuragis.com/geoserver/wfs
Uso: Descargar datos vectoriales
GetCapabilities: ?request=GetCapabilities&service=WFS
```

### CSW (Catalog Service):
```
URL: https://gis.infraestructuragis.com/geoserver/csw
Uso: Buscar metadatos
GetCapabilities: ?request=GetCapabilities&service=CSW
```

### WPS (Web Processing Service):
```
URL: https://gis.infraestructuragis.com/geoserver/wps
Uso: Análisis espacial
GetCapabilities: ?request=GetCapabilities&service=WPS
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS RÁPIDOS

| Problema | Solución |
|----------|----------|
| No puedo iniciar sesión | Verifica usuario/contraseña. Contacta admin si olvidaste |
| No puedo subir archivo en Importer | Importer solo lee del servidor. Usa WinSCP para subir archivo primero a /home/igis/uploads/ |
| Mi archivo no sube por FTP | Verifica credenciales SSH. Contacta admin si no tienes acceso |
| El archivo es muy grande (>100MB) | Envía por Google Drive/Dropbox al admin o divide en partes |
| La capa no se ve | Verifica sistema de coordenadas (debe tener .prj) |
| Estilo no se aplica | Verifica sintaxis CSS. Usa "Validate" antes de Submit |
| WMS no funciona en QGIS | Verifica URL exacta con /wms al final |
| WMS no funciona en ArcMap | Verifica firewall. Intenta descargar como Shapefile |
| Error "Connection refused" | Verifica que la URL sea https:// (no http://) |

---

## 📞 CONTACTO

**Soporte Técnico**:
- 📧 Email: sgonzalez@infraestructuragis.com
- 🌐 Portal: https://gis.infraestructuragis.com

**Documentación**:
- 📖 Manual completo: MANUAL_USUARIO_IDE.md
- 📖 GeoServer docs: https://docs.geoserver.org
- 📖 GeoNetwork docs: https://geonetwork-opensource.org

---

## ✅ CHECKLIST ANTES DE PUBLICAR DATOS

- [ ] Archivo en formato correcto (ZIP para shapefile)
- [ ] Sistema de coordenadas definido (.prj incluido)
- [ ] Nombre de archivo sin espacios ni caracteres especiales
- [ ] Tamaño menor a 100 MB
- [ ] Metadatos creados en GeoNetwork
- [ ] Estilo asignado en GeoServer
- [ ] Previsualizó la capa (Layer Preview)
- [ ] Probó el servicio WMS en QGIS
- [ ] Verificó permisos de acceso

---

**Imprime esta guía y manténla a mano** 🖨️

---

**Versión**: 1.0  
**Fecha**: Marzo 2026  
**Universidad de Colima - InfraestructuraGIS**
