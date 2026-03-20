# Guía de conexión WMS para ArcMap

Servicio WMS con mapas base (ESRI, Google, OSM) disponible para uso en ArcMap y ArcGIS Desktop.

## URL del servicio

```
http://gis.infraestructuragis.com/qgis/qgis_mapserv.fcgi
```

## Capas disponibles

| Capa | Descripción |
|------|-------------|
| ESRI World Imagery | Imágenes satelitales de alta resolución |
| ESRI World Topo | Mapa topográfico mundial |
| ESRI World Street | Mapa de calles mundial |
| OpenStreetMap | Mapa colaborativo |
| OpenTopoMap | Topográfico con curvas de nivel |
| CartoDB Positron | Mapa claro minimalista |
| CartoDB Dark Matter | Mapa oscuro minimalista |
| Google Satellite | Imágenes satelitales de Google |
| Google Hybrid | Satélite con etiquetas de Google |

---

## Conexión en ArcMap 10.x

### Paso 1: Abrir ArcCatalog

Desde ArcMap: **Windows → Catalog** (o presionar el botón de Catalog en la barra de herramientas)

### Paso 2: Agregar servidor WMS

1. En el panel de Catalog, expandir **GIS Servers**
2. Doble clic en **Add WMS Server**

### Paso 3: Configurar conexión

En el diálogo que aparece:

| Campo | Valor |
|-------|-------|
| **URL** | `http://gis.infraestructuragis.com/qgis/qgis_mapserv.fcgi` |
| **User** | *(dejar vacío)* |
| **Password** | *(dejar vacío)* |

3. Clic en **Get Layers** para verificar la conexión
4. Clic en **OK**

### Paso 4: Agregar capa al mapa

1. En el Catalog, expandir el servidor WMS recién agregado
2. Verás la lista de capas disponibles
3. Arrastrar la capa deseada al mapa, o clic derecho → **Add To Current Map**

---

## Configuración importante del Dataframe

⚠️ **Las capas pueden aparecer desplazadas si el sistema de coordenadas no está configurado correctamente.**

### Configurar Web Mercator

1. Clic derecho en el nombre del **Dataframe** (generalmente "Layers") → **Properties**
2. Ir a la pestaña **Coordinate System**
3. Navegar a: **Projected Coordinate Systems → World → WGS 1984 Web Mercator (Auxiliary Sphere)**
4. Clic en **OK**

---

## Solución de problemas

### La capa aparece en blanco

- Verificar conexión a Internet
- Hacer zoom a una escala razonable (las capas de tiles requieren cierto nivel de zoom)
- Verificar que el dataframe esté en Web Mercator (EPSG:3857)

### La capa aparece como grupo vacío

En la tabla de contenidos:
1. Expandir el grupo con la flecha ▶
2. Activar el checkbox de la subcapa interior

### Error "WMS request returned an exception"

- Verificar que la URL esté correcta
- Verificar acceso a la red (firewall, proxy)
- Probar acceso desde navegador: abrir la URL del servicio + `?SERVICE=WMS&REQUEST=GetCapabilities`

### Las capas están desplazadas

- Configurar el dataframe en **WGS 1984 Web Mercator (Auxiliary Sphere)**
- NO usar sistemas de coordenadas locales o geográficas para estas capas

---

## Propiedades recomendadas de la capa

Para mejorar la visualización:

1. Clic derecho en la capa → **Properties**
2. Pestaña **Display**:
   - **Resample during display using:** Bilinear Interpolation
3. Pestaña **General**:
   - Desactivar **Use scale-dependent rendering** si quieres ver la capa a todas las escalas
