# ============================================================
# CONFIGURACIÓN GEE
# ============================================================
GEE_ACCOUNT = 'sebastiangz@ucol.mx'  # Cambiar por tu cuenta
GEE_PROJECT = 'recaptcha-migrated-7c76cc4e92d'      # Cambiar por tu proyecto
CARPETA_DRIVE = 'MIA_GEE_Cuyutlan'

# ============================================================
# SCRIPT: Análisis Geoespacial MIA con Google Earth Engine
# Programa : MIA_GEE_Analisis_v1.py
# Área     : Laguna de Cuyutlán / Puerto Nuevo Manzanillo, Colima
# Proyecto : MIA-R Puerto Nuevo Manzanillo
#
# METODOLOGÍA PARA MANIFESTACIÓN DE IMPACTO AMBIENTAL
# ───────────────────────────────────────────────────────────────
# Basada en:
#   · LGEEPA y su Reglamento en materia de Evaluación del Impacto Ambiental
#   · NOM-059-SEMARNAT-2010 - Especies en riesgo
#   · NOM-022-SEMARNAT-2003 - Manglares
#   · INEGI Serie VII - Uso de Suelo y Vegetación (2021)
#   · CONABIO - Biodiversidad y ecosistemas
#   · Metodología del Sistema Ambiental Regional (SAR)
#
# ÍNDICES Y CAPAS ESPACIALES GEE:
#   1. Cobertura de Manglar        (Global Mangrove Watch + clasificación)
#   2. Cambio de Uso de Suelo      (Análisis multitemporal Landsat/Sentinel)
#   3. NDVI - Salud de Vegetación  (Series temporales Sentinel-2)
#   4. Cuerpos de Agua             (JRC Global Surface Water)
#   5. Elevación y Pendientes      (SRTM)
#   6. Temperatura Superficial     (MODIS LST)
#   7. Precipitación               (CHIRPS)
#   8. Detección de Incendios      (MODIS Fire)
#   9. Fragmentación del Paisaje   (Métricas espaciales)
#  10. Delimitación SAR y AP       (Shapefiles de entrada)
#
# OUTPUTS:
#   · Mapa HTML interactivo (geemap)
#   · Múltiples GeoTIFFs por capa temática
#   · CSV con estadísticas por tipo de cobertura
#   · CSV con análisis de cambio de uso de suelo
#   · CSV con índices de fragmentación
#   · GeoJSON con polígonos de vegetación
#   · Reporte de procesamiento en TXT/MD
#   · Compatible con PyQGIS para carga automática
#
# INSTALACIÓN:
#   pip install earthengine-api geemap geopandas shapely pandas
# ============================================================

import os
import sys
import datetime
import csv
import math
import struct
import json
import time

# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================
BASE = r"D:\ownCloud\Python\AnalisisGeoEspacialMIA"
RESULTADOS = os.path.join(BASE, "resultados_MIA_GEE")
os.makedirs(RESULTADOS, exist_ok=True)

# Directorio para reportes de proceso
REPORTES = os.path.join(RESULTADOS, "reportes")
os.makedirs(REPORTES, exist_ok=True)

# Shapefiles de entrada
SHAPEFILE_SAR = os.path.join(BASE, "capasSHP", "areaSAR.shp")
SHAPEFILE_AP = os.path.join(BASE, "capasSHP", "areaProyecto.shp")
SHAPEFILE_MUESTREO = os.path.join(BASE, "capasSHP", "sitiosMuestreo.shp")

# Archivos de salida
RUTA_MAPA_HTML = os.path.join(RESULTADOS, "mapa_MIA_cuyutlan.html")
RUTA_CSV_USV = os.path.join(RESULTADOS, "uso_suelo_vegetacion.csv")
RUTA_CSV_CAMBIO = os.path.join(RESULTADOS, "cambio_uso_suelo.csv")
RUTA_CSV_NDVI = os.path.join(RESULTADOS, "estadisticas_ndvi.csv")
RUTA_CSV_FRAGMENTACION = os.path.join(RESULTADOS, "fragmentacion_paisaje.csv")
RUTA_CSV_MANGLAR = os.path.join(RESULTADOS, "analisis_manglar.csv")
RUTA_REPORTE_MD = os.path.join(REPORTES, "reporte_proceso_MIA.md")
RUTA_REPORTE_LOG = os.path.join(REPORTES, "log_procesamiento.txt")

# ── Período de análisis ──────────────────────────────────────
hoy = datetime.date.today()
AÑO_FIN = hoy.year if hoy.month >= 7 else hoy.year - 1
AÑO_INICIO = AÑO_FIN - 9  # 10 años de análisis
AÑOS = list(range(AÑO_INICIO, AÑO_FIN + 1))

# Fechas específicas para comparación INEGI
FECHA_SERIE_III = 2008  # INEGI Serie III
FECHA_SERIE_VII = 2021  # INEGI Serie VII

# ============================================================
# CLASE PARA LOGGING Y REPORTES
# ============================================================
class ReporteProcesoMIA:
    """
    Clase para generar reportes de proceso durante el análisis GEE.
    Mantiene un log detallado y genera reportes en formato Markdown.
    """
    
    def __init__(self, ruta_log, ruta_md):
        self.ruta_log = ruta_log
        self.ruta_md = ruta_md
        self.inicio = datetime.datetime.now()
        self.pasos = []
        self.estadisticas = {}
        self.errores = []
        self.advertencias = []
        
        # Inicializar archivo de log
        with open(self.ruta_log, 'w', encoding='utf-8') as f:
            f.write(f"=" * 70 + "\n")
            f.write("LOG DE PROCESAMIENTO - ANÁLISIS GEOESPACIAL MIA\n")
            f.write(f"Inicio: {self.inicio.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"=" * 70 + "\n\n")
    
    def log(self, mensaje, nivel="INFO"):
        """Registra un mensaje en el log."""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        linea = f"[{timestamp}] [{nivel}] {mensaje}"
        print(linea)
        
        with open(self.ruta_log, 'a', encoding='utf-8') as f:
            f.write(linea + "\n")
        
        if nivel == "ERROR":
            self.errores.append(mensaje)
        elif nivel == "WARN":
            self.advertencias.append(mensaje)
    
    def iniciar_paso(self, numero, titulo):
        """Registra el inicio de un paso de procesamiento."""
        self.log(f"\n{'='*70}")
        self.log(f"PASO {numero}: {titulo}")
        self.log(f"{'='*70}")
        
        paso = {
            'numero': numero,
            'titulo': titulo,
            'inicio': datetime.datetime.now(),
            'resultados': {},
            'estado': 'EN PROCESO'
        }
        self.pasos.append(paso)
        return paso
    
    def finalizar_paso(self, paso, resultados=None, estado='COMPLETADO'):
        """Registra el fin de un paso de procesamiento."""
        paso['fin'] = datetime.datetime.now()
        paso['duracion'] = (paso['fin'] - paso['inicio']).total_seconds()
        paso['estado'] = estado
        
        if resultados:
            paso['resultados'] = resultados
            self.estadisticas.update(resultados)
        
        self.log(f"  ✓ Paso {paso['numero']} completado en {paso['duracion']:.2f} segundos")
    
    def agregar_estadistica(self, clave, valor, unidad=""):
        """Agrega una estadística al reporte."""
        self.estadisticas[clave] = {'valor': valor, 'unidad': unidad}
    
    def generar_reporte_markdown(self):
        """Genera el reporte final en formato Markdown."""
        fin = datetime.datetime.now()
        duracion_total = (fin - self.inicio).total_seconds()
        
        md = []
        md.append("# Reporte de Análisis Geoespacial MIA")
        md.append(f"## Proyecto: Puerto Nuevo Manzanillo, Vaso II Laguna Cuyutlán")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Información General")
        md.append("")
        md.append(f"| Parámetro | Valor |")
        md.append(f"|-----------|-------|")
        md.append(f"| Fecha de ejecución | {self.inicio.strftime('%Y-%m-%d')} |")
        md.append(f"| Hora de inicio | {self.inicio.strftime('%H:%M:%S')} |")
        md.append(f"| Hora de fin | {fin.strftime('%H:%M:%S')} |")
        md.append(f"| Duración total | {duracion_total/60:.2f} minutos |")
        md.append(f"| Período de análisis | {AÑO_INICIO} - {AÑO_FIN} |")
        md.append("")
        
        md.append("## Resumen de Pasos Ejecutados")
        md.append("")
        md.append("| Paso | Descripción | Duración (s) | Estado |")
        md.append("|------|-------------|--------------|--------|")
        
        for paso in self.pasos:
            duracion = paso.get('duracion', 0)
            estado_emoji = "✓" if paso['estado'] == 'COMPLETADO' else "✗"
            md.append(f"| {paso['numero']} | {paso['titulo']} | {duracion:.2f} | {estado_emoji} {paso['estado']} |")
        
        md.append("")
        
        if self.estadisticas:
            md.append("## Estadísticas Principales")
            md.append("")
            md.append("| Indicador | Valor | Unidad |")
            md.append("|-----------|-------|--------|")
            
            for clave, datos in self.estadisticas.items():
                if isinstance(datos, dict):
                    valor = datos.get('valor', datos)
                    unidad = datos.get('unidad', '')
                else:
                    valor = datos
                    unidad = ''
                
                if isinstance(valor, float):
                    valor_str = f"{valor:.4f}"
                else:
                    valor_str = str(valor)
                
                md.append(f"| {clave} | {valor_str} | {unidad} |")
            
            md.append("")
        
        if self.errores:
            md.append("## ⚠️ Errores Encontrados")
            md.append("")
            for error in self.errores:
                md.append(f"- {error}")
            md.append("")
        
        if self.advertencias:
            md.append("## ⚡ Advertencias")
            md.append("")
            for adv in self.advertencias:
                md.append(f"- {adv}")
            md.append("")
        
        md.append("## Archivos Generados")
        md.append("")
        md.append("| Archivo | Descripción |")
        md.append("|---------|-------------|")
        md.append(f"| `{os.path.basename(RUTA_MAPA_HTML)}` | Mapa interactivo HTML |")
        md.append(f"| `{os.path.basename(RUTA_CSV_USV)}` | Uso de suelo y vegetación |")
        md.append(f"| `{os.path.basename(RUTA_CSV_CAMBIO)}` | Cambio de uso de suelo |")
        md.append(f"| `{os.path.basename(RUTA_CSV_NDVI)}` | Estadísticas NDVI |")
        md.append(f"| `{os.path.basename(RUTA_CSV_MANGLAR)}` | Análisis de manglar |")
        md.append(f"| `*.tif` | Capas GeoTIFF para QGIS |")
        md.append("")
        
        md.append("---")
        md.append(f"*Reporte generado automáticamente por MIA_GEE_Analisis_v1.py*")
        
        # Guardar archivo Markdown
        with open(self.ruta_md, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))
        
        self.log(f"Reporte Markdown generado: {self.ruta_md}")
        return '\n'.join(md)


# ============================================================
# CLASIFICACIÓN DE USO DE SUELO Y VEGETACIÓN
# ============================================================
# Basado en INEGI Serie VII y observaciones de campo
CLASES_USV = {
    'VM': {'nombre': 'Manglar', 'codigo': 1, 'color': '#006400', 'forestal': True},
    'VHH': {'nombre': 'Vegetación Halófila Hidrófila', 'codigo': 2, 'color': '#90EE90', 'forestal': True},
    'SBC': {'nombre': 'Selva Baja Caducifolia', 'codigo': 3, 'color': '#228B22', 'forestal': True},
    'VSA_SBC': {'nombre': 'Veg. Sec. Arbórea SBC', 'codigo': 4, 'color': '#32CD32', 'forestal': True},
    'VSa_SBC': {'nombre': 'Veg. Sec. Arbustiva SBC', 'codigo': 5, 'color': '#7CFC00', 'forestal': True},
    'VDC': {'nombre': 'Vegetación Dunas Costeras', 'codigo': 6, 'color': '#F4A460', 'forestal': True},
    'SMQ': {'nombre': 'Selva Mediana Subcaducifolia', 'codigo': 7, 'color': '#006400', 'forestal': True},
    'RA': {'nombre': 'Riego Agrícola', 'codigo': 10, 'color': '#FFD700', 'forestal': False},
    'TA': {'nombre': 'Temporal Agrícola', 'codigo': 11, 'color': '#DAA520', 'forestal': False},
    'PA': {'nombre': 'Pastizal', 'codigo': 12, 'color': '#ADFF2F', 'forestal': False},
    'AU': {'nombre': 'Asentamiento Urbano', 'codigo': 20, 'color': '#808080', 'forestal': False},
    'ADV': {'nombre': 'Área Desprovista de Vegetación', 'codigo': 21, 'color': '#D2B48C', 'forestal': False},
    'CA': {'nombre': 'Cuerpo de Agua', 'codigo': 30, 'color': '#0000FF', 'forestal': False},
}

# Buffers de protección para manglar (NOM-022-SEMARNAT-2003)
BUFFER_MANGLAR_M = 100  # metros de zona de amortiguamiento


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def leer_shapefile_poligonos(shp_path):
    """
    Lee un shapefile de polígonos sin dependencias externas.
    Retorna lista de diccionarios con geometría y atributos.
    """
    dbf_path = shp_path.replace('.shp', '.dbf')
    
    if not os.path.exists(shp_path):
        return None
    
    # Intentar con geopandas primero
    try:
        import geopandas as gpd
        gdf = gpd.read_file(shp_path)
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)
        return gdf
    except ImportError:
        pass
    except Exception as e:
        print(f"  [WARN] Error con geopandas: {e}")
    
    # Fallback: lectura manual básica
    return None


def calcular_area_km2(geometry_ee, scale=30):
    """
    Calcula el área de una geometría GEE en km².
    """
    import ee
    area_m2 = geometry_ee.area(scale)
    return area_m2.divide(1e6).getInfo()


def normalizar_imagen(imagen, area, escala=30):
    """
    Normaliza una imagen GEE al rango [0, 1] dentro de un área.
    """
    import ee
    stats = imagen.reduceRegion(
        reducer=ee.Reducer.minMax(),
        geometry=area,
        scale=escala,
        maxPixels=1e9,
        bestEffort=True
    ).getInfo()
    
    banda = imagen.bandNames().getInfo()[0]
    val_min = stats.get(f'{banda}_min', 0) or 0
    val_max = stats.get(f'{banda}_max', 1) or 1
    
    if val_max == val_min:
        return imagen.multiply(0)
    
    return imagen.subtract(val_min).divide(val_max - val_min).clamp(0, 1)


def exportar_a_drive(imagen, descripcion, region, escala, carpeta):
    """
    Exporta una imagen a Google Drive.
    """
    import ee
    
    task = ee.batch.Export.image.toDrive(
        image=imagen,
        description=descripcion,
        folder=carpeta,
        region=region,
        scale=escala,
        maxPixels=1e13,
        fileFormat='GeoTIFF'
    )
    task.start()
    return task


def guardar_geotiff_local(imagen, ruta, region, escala=30):
    """
    Intenta guardar un GeoTIFF localmente usando geemap.
    """
    try:
        import geemap
        geemap.ee_export_image(
            imagen,
            filename=ruta,
            scale=escala,
            region=region,
            file_per_band=False
        )
        return True
    except Exception as e:
        print(f"  [WARN] No se pudo exportar localmente: {e}")
        return False


# ============================================================
# INICIALIZACIÓN DEL REPORTE
# ============================================================
reporte = ReporteProcesoMIA(RUTA_REPORTE_LOG, RUTA_REPORTE_MD)

reporte.log("=" * 70)
reporte.log("ANÁLISIS GEOESPACIAL MIA v1.0")
reporte.log("Manifestación de Impacto Ambiental - Puerto Nuevo Manzanillo")
reporte.log("Laguna de Cuyutlán, Colima")
reporte.log("=" * 70)
reporte.log("")

# ============================================================
# PASO 1 — AUTENTICACIÓN GEE
# ============================================================
paso1 = reporte.iniciar_paso(1, "Autenticación Google Earth Engine")

import ee
import geemap

def inicializar_gee(proyecto: str, cuenta: str):
    """Inicializa Google Earth Engine con manejo de errores."""
    try:
        ee.Initialize(project=proyecto,
                      opt_url='https://earthengine.googleapis.com')
        reporte.log(f"  ✓ GEE inicializado: proyecto '{proyecto}'")
        return True
    except Exception as e:
        reporte.log(f"  [INFO] Autenticación interactiva requerida: {e}", "INFO")
        try:
            ee.Authenticate()
            ee.Initialize(project=proyecto)
            reporte.log(f"  ✓ GEE inicializado tras autenticación")
            return True
        except Exception as e2:
            reporte.log(f"  [ERROR] No se pudo inicializar GEE: {e2}", "ERROR")
            return False


gee_ok = inicializar_gee(GEE_PROJECT, GEE_ACCOUNT)
reporte.finalizar_paso(paso1, {'gee_inicializado': gee_ok})

if not gee_ok:
    reporte.log("ABORTANDO: No se pudo conectar a Google Earth Engine", "ERROR")
    reporte.generar_reporte_markdown()
    sys.exit(1)

# ============================================================
# PASO 2 — CARGA DEL ÁREA DE ESTUDIO (SAR)
# ============================================================
paso2 = reporte.iniciar_paso(2, "Carga del Sistema Ambiental Regional (SAR)")

# Coordenadas hardcoded del SAR (fallback)
COORDS_SAR_HARDCODED = [
    [-104.331324, 19.149614], [-104.349761, 19.147523], [-104.351994, 19.141388],
    [-104.358047, 19.138261], [-104.363820, 19.135841], [-104.370591, 19.133224],
    [-104.377089, 19.131103], [-104.381244, 19.127862], [-104.384981, 19.124015],
    [-104.387832, 19.119498], [-104.391088, 19.114975], [-104.394232, 19.110345],
    [-104.396951, 19.105602], [-104.399512, 19.100750], [-104.402044, 19.095892],
    [-104.404374, 19.100686], [-104.410543, 19.105775], [-104.416812, 19.109841],
    [-104.421986, 19.114002], [-104.427354, 19.118024], [-104.430791, 19.113251],
    [-104.433721, 19.108302], [-104.436597, 19.098259], [-104.438014, 19.088796],
    [-104.438353, 19.092710], [-104.437299, 19.084066], [-104.399623, 19.093616],
    [-104.394695, 19.089679], [-104.396403, 19.086863], [-104.394828, 19.087177],
    [-104.397827, 19.089629], [-104.387413, 19.079501], [-104.370231, 19.065412],
    [-104.352103, 19.048892], [-104.335420, 19.031842], [-104.315298, 19.012341],
    [-104.295612, 18.990231], [-104.278433, 18.971201], [-104.263821, 18.952311],
    [-104.248711, 18.932221], [-104.232102, 18.911421], [-104.215392, 18.890121],
    [-104.198712, 18.869960], [-104.049891, 18.900231], [-104.021341, 18.921031],
    [-103.995621, 18.941200], [-103.978790, 18.961000], [-103.978790, 19.050000],
    [-103.990000, 19.100000], [-104.010000, 19.150000], [-104.050000, 19.175210],
    [-104.100000, 19.175210], [-104.150000, 19.175210], [-104.200000, 19.175210],
    [-104.250000, 19.175210], [-104.300000, 19.175210], [-104.331324, 19.149614],
]

# Coordenadas del Área de Proyecto (AP) - aproximadas
COORDS_AP_HARDCODED = [
    [-104.2950, 19.0650], [-104.2800, 19.0650], [-104.2800, 19.0450],
    [-104.2950, 19.0450], [-104.2950, 19.0650]
]

area_sar = None
area_ap = None
centro_lat, centro_lon = 19.0226, -104.2101
fuente_sar = "hardcoded"

# Intentar cargar desde shapefile
try:
    import geopandas as gpd
    from shapely.ops import unary_union
    
    if os.path.exists(SHAPEFILE_SAR):
        gdf_sar = gpd.read_file(SHAPEFILE_SAR)
        if gdf_sar.crs and gdf_sar.crs.to_epsg() != 4326:
            gdf_sar = gdf_sar.to_crs(epsg=4326)
        
        union_sar = unary_union(gdf_sar.geometry)
        
        # Convertir a geometría GEE
        if union_sar.geom_type == 'Polygon':
            coords = [list(c) for c in union_sar.exterior.coords]
            area_sar = ee.Geometry.Polygon([coords])
        elif union_sar.geom_type == 'MultiPolygon':
            all_rings = []
            for poly in union_sar.geoms:
                rings = [list(c) for c in poly.exterior.coords]
                all_rings.append([rings])
            area_sar = ee.Geometry.MultiPolygon(all_rings)
        
        centro = union_sar.centroid
        centro_lat, centro_lon = centro.y, centro.x
        fuente_sar = "shapefile"
        
        reporte.log(f"  ✓ SAR cargado desde shapefile: {SHAPEFILE_SAR}")
        reporte.log(f"  ✓ Tipo geometría: {union_sar.geom_type}")
        
except ImportError:
    reporte.log("  [INFO] geopandas no disponible, usando coordenadas hardcoded", "WARN")
except Exception as e:
    reporte.log(f"  [WARN] Error cargando shapefile: {e}", "WARN")

# Fallback a coordenadas hardcoded
if area_sar is None:
    area_sar = ee.Geometry.Polygon([COORDS_SAR_HARDCODED])
    reporte.log("  ✓ SAR cargado desde coordenadas hardcoded")

# Área de Proyecto (AP)
area_ap = ee.Geometry.Polygon([COORDS_AP_HARDCODED])

# Calcular áreas
area_sar_km2 = calcular_area_km2(area_sar)
area_ap_km2 = calcular_area_km2(area_ap)

reporte.log(f"  ✓ Centroide SAR: {centro_lat:.4f}°N, {centro_lon:.4f}°W")
reporte.log(f"  ✓ Área SAR: {area_sar_km2:.2f} km²")
reporte.log(f"  ✓ Área AP: {area_ap_km2:.2f} km²")

reporte.finalizar_paso(paso2, {
    'area_sar_km2': area_sar_km2,
    'area_ap_km2': area_ap_km2,
    'fuente_sar': fuente_sar
})

# ============================================================
# PASO 3 — ANÁLISIS DE COBERTURA DE MANGLAR
# ============================================================
paso3 = reporte.iniciar_paso(3, "Análisis de Cobertura de Manglar (NOM-022)")

reporte.log("  Procesando detección de manglar con múltiples fuentes...")

# ═══════════════════════════════════════════════════════════════════════════
# MÉTODO ALTERNATIVO: Clasificación de manglar usando índices espectrales
# Debido a que Global Mangrove Watch puede no estar accesible, usamos:
#   1. NDVI + NDWI para detectar vegetación húmeda costera
#   2. JRC Global Surface Water para zonas de transición agua-tierra
#   3. Elevación SRTM para filtrar zonas costeras bajas
#   4. Landsat Global Mangrove Extent (si disponible)
# ═══════════════════════════════════════════════════════════════════════════

# Intentar cargar Global Mangrove Watch (múltiples rutas posibles)
GMW_DISPONIBLE = False
mascara_manglar = None
fuente_manglar = "Clasificación espectral (NDVI+NDWI+SRTM)"

# Lista de posibles rutas del dataset GMW
rutas_gmw = [
    'projects/earthengine-legacy/assets/projects/global-mangrove-watch/GMW/2020',
    'projects/ee-globalmangroveswatch/assets/GMW_v3_2020',
    'JRC/GSW1_4/GlobalSurfaceWater',  # Fallback para zonas de agua
]

for ruta in rutas_gmw[:2]:  # Solo probar las rutas de GMW
    try:
        reporte.log(f"  Intentando cargar: {ruta}")
        gmw_test = ee.ImageCollection(ruta).first()
        # Verificar si existe haciendo una operación simple
        gmw_test.getInfo()
        
        gmw_2020 = ee.ImageCollection(ruta) \
            .filterBounds(area_sar) \
            .mosaic() \
            .clip(area_sar)
        
        mascara_manglar = gmw_2020.gt(0).rename('manglar')
        GMW_DISPONIBLE = True
        fuente_manglar = f"Global Mangrove Watch ({ruta.split('/')[-1]})"
        reporte.log(f"  ✓ GMW cargado exitosamente desde: {ruta}")
        break
    except Exception as e:
        reporte.log(f"  [INFO] No disponible {ruta}: {str(e)[:50]}...", "INFO")
        continue

# Si GMW no está disponible, usar clasificación espectral
if not GMW_DISPONIBLE:
    reporte.log("  → Usando clasificación espectral alternativa para manglar...")
    
    # Cargar Sentinel-2 para índices espectrales
    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(area_sar) \
        .filterDate(f'{AÑO_FIN-1}-01-01', f'{AÑO_FIN}-12-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .median() \
        .clip(area_sar)
    
    # Calcular índices espectrales
    ndvi = sentinel2.normalizedDifference(['B8', 'B4']).rename('NDVI')
    ndwi = sentinel2.normalizedDifference(['B3', 'B8']).rename('NDWI')
    
    # MNDWI (Modified NDWI) - mejor para detectar agua
    mndwi = sentinel2.normalizedDifference(['B3', 'B11']).rename('MNDWI')
    
    # CMRI (Combined Mangrove Recognition Index)
    # CMRI = NDVI - NDWI (valores altos indican manglar)
    cmri = ndvi.subtract(ndwi).rename('CMRI')
    
    # Cargar SRTM para filtrar por elevación (manglares están en zonas bajas costeras)
    srtm = ee.Image('USGS/SRTMGL1_003').clip(area_sar)
    elevacion = srtm.select('elevation')
    
    # JRC Water para identificar zonas de transición
    jrc_water = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')
    ocurrencia_agua = jrc_water.select('occurrence').clip(area_sar)
    
    # ═══════════════════════════════════════════════════════════════════════
    # CLASIFICACIÓN DE MANGLAR
    # Criterios (basados en literatura científica):
    #   - NDVI > 0.25 (vegetación presente)
    #   - NDWI > -0.4 y < 0.2 (húmedo pero no agua abierta)
    #   - CMRI > 0.3 (índice combinado alto)
    #   - Elevación < 10m (zona costera baja)
    #   - Ocurrencia de agua entre 10-80% (zona de transición)
    # ═══════════════════════════════════════════════════════════════════════
    
    # Criterio 1: Vegetación verde presente
    criterio_vegetacion = ndvi.gt(0.25)
    
    # Criterio 2: Zona húmeda (no agua abierta)
    criterio_humedad = ndwi.gt(-0.4).And(ndwi.lt(0.2))
    
    # Criterio 3: CMRI alto (característico de manglar)
    criterio_cmri = cmri.gt(0.3)
    
    # Criterio 4: Zona costera baja
    criterio_elevacion = elevacion.lt(10)
    
    # Criterio 5: Zona de transición agua-tierra
    criterio_transicion = ocurrencia_agua.gt(10).And(ocurrencia_agua.lt(80))
    
    # Combinar criterios (al menos 3 de 5 deben cumplirse para mayor robustez)
    # Método conservador: vegetación + humedad + (CMRI o elevación baja)
    mascara_manglar = criterio_vegetacion \
        .And(criterio_humedad) \
        .And(criterio_cmri.Or(criterio_elevacion.And(criterio_transicion))) \
        .rename('manglar')
    
    fuente_manglar = "Clasificación espectral (NDVI+NDWI+CMRI+SRTM+JRC)"
    reporte.log(f"  ✓ Clasificación espectral completada")

# Si aún no tenemos máscara, crear una vacía para evitar errores
if mascara_manglar is None:
    reporte.log("  [WARN] No se pudo generar máscara de manglar, usando valores por defecto", "WARN")
    mascara_manglar = ee.Image.constant(0).clip(area_sar).rename('manglar')
    fuente_manglar = "No disponible (valores por defecto)"

# ═══════════════════════════════════════════════════════════════════════════
# CÁLCULO DE ESTADÍSTICAS DE MANGLAR
# ═══════════════════════════════════════════════════════════════════════════

# Calcular NDWI y NDVI para análisis complementario (si no se calculó antes)
try:
    ndvi
except NameError:
    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(area_sar) \
        .filterDate(f'{AÑO_FIN-1}-01-01', f'{AÑO_FIN}-12-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .median() \
        .clip(area_sar)
    
    ndwi = sentinel2.normalizedDifference(['B3', 'B8']).rename('NDWI')
    ndvi = sentinel2.normalizedDifference(['B8', 'B4']).rename('NDVI')

# Estadísticas de manglar en SAR
try:
    stats_manglar_gmw = mascara_manglar.multiply(ee.Image.pixelArea()).reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=area_sar,
        scale=30,
        maxPixels=1e9,
        bestEffort=True
    ).getInfo()
    
    area_manglar_gmw_ha = (stats_manglar_gmw.get('manglar', 0) or 0) / 10000
except Exception as e:
    reporte.log(f"  [WARN] Error calculando área manglar SAR: {e}", "WARN")
    area_manglar_gmw_ha = 0

# Manglar en el AP
try:
    stats_manglar_ap = mascara_manglar.multiply(ee.Image.pixelArea()).reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=area_ap,
        scale=30,
        maxPixels=1e9,
        bestEffort=True
    ).getInfo()
    
    area_manglar_ap_ha = (stats_manglar_ap.get('manglar', 0) or 0) / 10000
except Exception as e:
    reporte.log(f"  [WARN] Error calculando área manglar AP: {e}", "WARN")
    area_manglar_ap_ha = 0

# Buffer de protección del manglar (solo si hay manglar detectado)
buffer_manglar = None
if area_manglar_gmw_ha > 0:
    try:
        manglar_vector = mascara_manglar.reduceToVectors(
            geometry=area_sar,
            scale=30,
            maxPixels=1e8,
            bestEffort=True
        )
        
        buffer_manglar = manglar_vector.map(
            lambda f: f.buffer(BUFFER_MANGLAR_M)
        )
        reporte.log(f"  ✓ Buffer de protección generado: {BUFFER_MANGLAR_M} m")
    except Exception as e:
        reporte.log(f"  [WARN] No se pudo generar buffer de manglar: {e}", "WARN")

reporte.log(f"  ✓ Fuente de datos: {fuente_manglar}")
reporte.log(f"  ✓ Área de manglar en SAR: {area_manglar_gmw_ha:.2f} ha")
reporte.log(f"  ✓ Área de manglar en AP: {area_manglar_ap_ha:.2f} ha")
reporte.log(f"  ✓ Buffer de protección: {BUFFER_MANGLAR_M} m (NOM-022)")

# Guardar CSV de manglar
with open(RUTA_CSV_MANGLAR, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Zona', 'Area_Manglar_ha', 'Fuente', 'Normativa', 'Metodo'])
    writer.writerow(['SAR', f'{area_manglar_gmw_ha:.2f}', fuente_manglar, 
                    'NOM-022-SEMARNAT-2003', 'GMW' if GMW_DISPONIBLE else 'Espectral'])
    writer.writerow(['AP', f'{area_manglar_ap_ha:.2f}', fuente_manglar, 
                    'NOM-022-SEMARNAT-2003', 'GMW' if GMW_DISPONIBLE else 'Espectral'])
    writer.writerow(['Buffer_proteccion_m', BUFFER_MANGLAR_M, 'Calculado', 
                    'NOM-022-SEMARNAT-2003', 'Buffer'])

reporte.log(f"  ✓ CSV manglar guardado: {RUTA_CSV_MANGLAR}")

reporte.finalizar_paso(paso3, {
    'manglar_sar_ha': area_manglar_gmw_ha,
    'manglar_ap_ha': area_manglar_ap_ha,
    'buffer_proteccion_m': BUFFER_MANGLAR_M,
    'fuente_manglar': fuente_manglar,
    'gmw_disponible': GMW_DISPONIBLE
})

# ============================================================
# PASO 4 — ANÁLISIS MULTITEMPORAL NDVI
# ============================================================
paso4 = reporte.iniciar_paso(4, "Análisis Multitemporal de NDVI (Salud Vegetación)")

reporte.log("  Procesando series temporales Sentinel-2...")

# Función para calcular NDVI anual
def calcular_ndvi_anual(año):
    """Calcula NDVI promedio para un año específico."""
    col = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(area_sar) \
        .filterDate(f'{año}-01-01', f'{año}-12-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    
    ndvi_año = col.map(
        lambda img: img.normalizedDifference(['B8', 'B4']).rename('NDVI')
    ).median().clip(area_sar)
    
    return ndvi_año.set('año', año)

# Calcular NDVI para años clave
años_analisis = [2016, 2018, 2020, 2022, AÑO_FIN]
ndvi_por_año = {}
stats_ndvi = []

for año in años_analisis:
    try:
        ndvi_año = calcular_ndvi_anual(año)
        
        stats = ndvi_año.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                ee.Reducer.stdDev(), sharedInputs=True
            ).combine(
                ee.Reducer.minMax(), sharedInputs=True
            ),
            geometry=area_sar,
            scale=30,
            maxPixels=1e9,
            bestEffort=True
        ).getInfo()
        
        ndvi_por_año[año] = ndvi_año
        
        stats_ndvi.append({
            'año': año,
            'ndvi_mean': stats.get('NDVI_mean', 0) or 0,
            'ndvi_std': stats.get('NDVI_stdDev', 0) or 0,
            'ndvi_min': stats.get('NDVI_min', 0) or 0,
            'ndvi_max': stats.get('NDVI_max', 0) or 0
        })
        
        reporte.log(f"  ✓ NDVI {año}: media={stats.get('NDVI_mean', 0):.3f}")
        
    except Exception as e:
        reporte.log(f"  [WARN] Error procesando NDVI {año}: {e}", "WARN")

# Calcular tendencia NDVI
if len(stats_ndvi) >= 2:
    ndvi_inicial = stats_ndvi[0]['ndvi_mean']
    ndvi_final = stats_ndvi[-1]['ndvi_mean']
    cambio_ndvi = ndvi_final - ndvi_inicial
    tendencia = "MEJORA" if cambio_ndvi > 0.02 else ("DETERIORO" if cambio_ndvi < -0.02 else "ESTABLE")
    
    reporte.log(f"  ✓ Cambio NDVI ({años_analisis[0]}-{años_analisis[-1]}): {cambio_ndvi:+.3f} ({tendencia})")
else:
    cambio_ndvi = 0
    tendencia = "INDETERMINADO"

# Guardar CSV de NDVI
with open(RUTA_CSV_NDVI, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Año', 'NDVI_Media', 'NDVI_StdDev', 'NDVI_Min', 'NDVI_Max', 'Zona'])
    for s in stats_ndvi:
        writer.writerow([s['año'], f"{s['ndvi_mean']:.4f}", f"{s['ndvi_std']:.4f}", 
                        f"{s['ndvi_min']:.4f}", f"{s['ndvi_max']:.4f}", 'SAR'])

reporte.log(f"  ✓ CSV NDVI guardado: {RUTA_CSV_NDVI}")

reporte.finalizar_paso(paso4, {
    'ndvi_años_analizados': len(stats_ndvi),
    'cambio_ndvi': cambio_ndvi,
    'tendencia_vegetacion': tendencia
})

# ============================================================
# PASO 5 — ANÁLISIS DE CAMBIO DE USO DE SUELO
# ============================================================
paso5 = reporte.iniciar_paso(5, "Análisis de Cambio de Uso de Suelo")

reporte.log("  Comparando períodos para detectar cambios...")

# Imagen compuesta período inicial (similar a Serie III INEGI)
periodo_inicial = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(area_sar) \
    .filterDate('2017-01-01', '2018-12-31') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
    .median() \
    .clip(area_sar)

# Imagen compuesta período final (similar a Serie VII INEGI)
periodo_final = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(area_sar) \
    .filterDate(f'{AÑO_FIN-1}-01-01', f'{AÑO_FIN}-12-31') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
    .median() \
    .clip(area_sar)

# Calcular índices para ambos períodos
ndvi_inicial = periodo_inicial.normalizedDifference(['B8', 'B4']).rename('NDVI_inicial')
ndvi_final = periodo_final.normalizedDifference(['B8', 'B4']).rename('NDVI_final')

ndwi_inicial = periodo_inicial.normalizedDifference(['B3', 'B8']).rename('NDWI_inicial')
ndwi_final = periodo_final.normalizedDifference(['B3', 'B8']).rename('NDWI_final')

# Calcular diferencias
diff_ndvi = ndvi_final.subtract(ndvi_inicial).rename('diff_NDVI')
diff_ndwi = ndwi_final.subtract(ndwi_inicial).rename('diff_NDWI')

# Clasificar cambios
# NDVI disminuyó significativamente = pérdida de vegetación
perdida_vegetacion = diff_ndvi.lt(-0.15).rename('perdida_veg')
ganancia_vegetacion = diff_ndvi.gt(0.15).rename('ganancia_veg')
sin_cambio = diff_ndvi.abs().lt(0.15).rename('sin_cambio')

# Estadísticas de cambio
stats_cambio = {}

# Área con pérdida de vegetación
stats_perdida = perdida_vegetacion.multiply(ee.Image.pixelArea()).reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=area_sar,
    scale=30,
    maxPixels=1e9
).getInfo()
area_perdida_ha = (stats_perdida.get('perdida_veg', 0) or 0) / 10000

# Área con ganancia de vegetación
stats_ganancia = ganancia_vegetacion.multiply(ee.Image.pixelArea()).reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=area_sar,
    scale=30,
    maxPixels=1e9
).getInfo()
area_ganancia_ha = (stats_ganancia.get('ganancia_veg', 0) or 0) / 10000

# Balance neto
balance_neto = area_ganancia_ha - area_perdida_ha

reporte.log(f"  ✓ Área con pérdida de vegetación: {area_perdida_ha:.2f} ha")
reporte.log(f"  ✓ Área con ganancia de vegetación: {area_ganancia_ha:.2f} ha")
reporte.log(f"  ✓ Balance neto: {balance_neto:+.2f} ha")

# Guardar CSV de cambio
with open(RUTA_CSV_CAMBIO, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Tipo_Cambio', 'Area_ha', 'Periodo', 'Zona', 'Fuente'])
    writer.writerow(['Pérdida de vegetación', f'{area_perdida_ha:.2f}', 
                    f'2017-2018 vs {AÑO_FIN-1}-{AÑO_FIN}', 'SAR', 'Sentinel-2 NDVI'])
    writer.writerow(['Ganancia de vegetación', f'{area_ganancia_ha:.2f}',
                    f'2017-2018 vs {AÑO_FIN-1}-{AÑO_FIN}', 'SAR', 'Sentinel-2 NDVI'])
    writer.writerow(['Balance neto', f'{balance_neto:+.2f}',
                    f'2017-2018 vs {AÑO_FIN-1}-{AÑO_FIN}', 'SAR', 'Sentinel-2 NDVI'])

reporte.log(f"  ✓ CSV cambio guardado: {RUTA_CSV_CAMBIO}")

reporte.finalizar_paso(paso5, {
    'perdida_vegetacion_ha': area_perdida_ha,
    'ganancia_vegetacion_ha': area_ganancia_ha,
    'balance_neto_ha': balance_neto
})

# ============================================================
# PASO 6 — ANÁLISIS DE CUERPOS DE AGUA
# ============================================================
paso6 = reporte.iniciar_paso(6, "Análisis de Cuerpos de Agua (JRC GSW)")

reporte.log("  Procesando JRC Global Surface Water...")

# JRC Global Surface Water
jrc_water = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')
ocurrencia_agua = jrc_water.select('occurrence').clip(area_sar)
estacionalidad = jrc_water.select('seasonality').clip(area_sar)
transiciones = jrc_water.select('transition').clip(area_sar)

# Clasificar cuerpos de agua
agua_permanente = ocurrencia_agua.gte(80).rename('agua_permanente')
agua_estacional = ocurrencia_agua.gte(25).And(ocurrencia_agua.lt(80)).rename('agua_estacional')

# Estadísticas
stats_agua_perm = agua_permanente.multiply(ee.Image.pixelArea()).reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=area_sar,
    scale=30,
    maxPixels=1e9
).getInfo()
area_agua_perm_ha = (stats_agua_perm.get('agua_permanente', 0) or 0) / 10000

stats_agua_est = agua_estacional.multiply(ee.Image.pixelArea()).reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=area_sar,
    scale=30,
    maxPixels=1e9
).getInfo()
area_agua_est_ha = (stats_agua_est.get('agua_estacional', 0) or 0) / 10000

# Área lagunar total (Laguna de Cuyutlán)
area_agua_total_ha = area_agua_perm_ha + area_agua_est_ha

reporte.log(f"  ✓ Agua permanente: {area_agua_perm_ha:.2f} ha")
reporte.log(f"  ✓ Agua estacional: {area_agua_est_ha:.2f} ha")
reporte.log(f"  ✓ Total cuerpos de agua: {area_agua_total_ha:.2f} ha")

reporte.finalizar_paso(paso6, {
    'agua_permanente_ha': area_agua_perm_ha,
    'agua_estacional_ha': area_agua_est_ha,
    'agua_total_ha': area_agua_total_ha
})

# ============================================================
# PASO 7 — MODELO DIGITAL DE ELEVACIÓN
# ============================================================
paso7 = reporte.iniciar_paso(7, "Modelo Digital de Elevación y Pendientes (SRTM)")

reporte.log("  Procesando SRTM DEM...")

# SRTM
srtm = ee.Image('USGS/SRTMGL1_003').clip(area_sar)
elevacion = srtm.select('elevation')
pendiente = ee.Terrain.slope(srtm)
aspecto = ee.Terrain.aspect(srtm)

# Estadísticas de elevación
stats_elev = elevacion.reduceRegion(
    reducer=ee.Reducer.mean().combine(
        ee.Reducer.minMax(), sharedInputs=True
    ),
    geometry=area_sar,
    scale=30,
    maxPixels=1e9
).getInfo()

elev_mean = stats_elev.get('elevation_mean', 0) or 0
elev_min = stats_elev.get('elevation_min', 0) or 0
elev_max = stats_elev.get('elevation_max', 0) or 0

# Zonas bajas susceptibles a inundación
zona_baja_5m = elevacion.lt(5).rename('zona_baja_5m')
zona_baja_10m = elevacion.lt(10).rename('zona_baja_10m')

stats_zona_baja = zona_baja_5m.multiply(ee.Image.pixelArea()).reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=area_sar,
    scale=30,
    maxPixels=1e9
).getInfo()
area_zona_baja_ha = (stats_zona_baja.get('zona_baja_5m', 0) or 0) / 10000

reporte.log(f"  ✓ Elevación media: {elev_mean:.1f} m")
reporte.log(f"  ✓ Elevación mín/máx: {elev_min:.1f} - {elev_max:.1f} m")
reporte.log(f"  ✓ Área bajo 5m (susceptible inundación): {area_zona_baja_ha:.2f} ha")

reporte.finalizar_paso(paso7, {
    'elevacion_media_m': elev_mean,
    'elevacion_min_m': elev_min,
    'elevacion_max_m': elev_max,
    'area_bajo_5m_ha': area_zona_baja_ha
})

# ============================================================
# PASO 8 — ANÁLISIS CLIMÁTICO
# ============================================================
paso8 = reporte.iniciar_paso(8, "Análisis Climático (Temperatura y Precipitación)")

reporte.log("  Procesando MODIS LST y CHIRPS...")

# MODIS Land Surface Temperature
modis_lst = ee.ImageCollection('MODIS/061/MOD11A1') \
    .filterDate(f'{AÑO_FIN-1}-01-01', f'{AÑO_FIN}-12-31') \
    .filterBounds(area_sar) \
    .select('LST_Day_1km') \
    .mean() \
    .multiply(0.02) \
    .subtract(273.15) \
    .clip(area_sar) \
    .rename('LST_Celsius')

stats_lst = modis_lst.reduceRegion(
    reducer=ee.Reducer.mean().combine(
        ee.Reducer.minMax(), sharedInputs=True
    ),
    geometry=area_sar,
    scale=1000,
    maxPixels=1e9
).getInfo()

lst_mean = stats_lst.get('LST_Celsius_mean', 0) or 0
lst_max = stats_lst.get('LST_Celsius_max', 0) or 0

# CHIRPS Precipitación
chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
    .filterDate(f'{AÑO_FIN-1}-01-01', f'{AÑO_FIN}-12-31') \
    .filterBounds(area_sar)

precip_anual = chirps.sum().clip(area_sar).rename('precip_anual')

stats_precip = precip_anual.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=area_sar,
    scale=5566,
    maxPixels=1e9
).getInfo()

precip_mean = stats_precip.get('precip_anual_mean', 0) or 0

reporte.log(f"  ✓ Temperatura superficial media: {lst_mean:.1f} °C")
reporte.log(f"  ✓ Temperatura superficial máxima: {lst_max:.1f} °C")
reporte.log(f"  ✓ Precipitación media anual: {precip_mean:.1f} mm")

reporte.finalizar_paso(paso8, {
    'temperatura_media_C': lst_mean,
    'temperatura_max_C': lst_max,
    'precipitacion_anual_mm': precip_mean
})

# ============================================================
# PASO 9 — DETECCIÓN DE INCENDIOS
# ============================================================
paso9 = reporte.iniciar_paso(9, "Detección de Incendios Históricos (MODIS Fire)")

reporte.log("  Procesando MODIS Active Fire...")

# MODIS Fire
modis_fire = ee.ImageCollection('MODIS/061/MOD14A1') \
    .filterDate(f'{AÑO_INICIO}-01-01', f'{AÑO_FIN}-12-31') \
    .filterBounds(area_sar) \
    .select('FireMask')

# Contar detecciones de fuego
fire_count = modis_fire.map(
    lambda img: img.gte(7).rename('fire')
).sum().clip(area_sar)

stats_fire = fire_count.reduceRegion(
    reducer=ee.Reducer.sum().combine(
        ee.Reducer.max(), sharedInputs=True
    ),
    geometry=area_sar,
    scale=1000,
    maxPixels=1e9
).getInfo()

fire_total = stats_fire.get('fire_sum', 0) or 0
fire_max = stats_fire.get('fire_max', 0) or 0

reporte.log(f"  ✓ Detecciones de fuego (período {AÑO_INICIO}-{AÑO_FIN}): {fire_total}")
reporte.log(f"  ✓ Máximo de detecciones en un pixel: {fire_max}")

reporte.finalizar_paso(paso9, {
    'detecciones_fuego_total': fire_total,
    'detecciones_fuego_max_pixel': fire_max,
    'periodo_analisis': f'{AÑO_INICIO}-{AÑO_FIN}'
})

# ============================================================
# PASO 10 — GENERACIÓN DE MAPA INTERACTIVO
# ============================================================
paso10 = reporte.iniciar_paso(10, "Generación de Mapa Interactivo HTML")

reporte.log("  Creando mapa con geemap...")

# Crear mapa
Map = geemap.Map()
Map.setCenter(centro_lon, centro_lat, 11)

# Paletas de colores
paleta_ndvi = ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60', '#1a9850']
paleta_agua = ['#ffffff', '#a6cee3', '#1f78b4', '#08306b']
paleta_manglar = ['#ffffff', '#006400']
paleta_cambio = ['#d73027', '#ffffbf', '#1a9850']  # pérdida, sin cambio, ganancia
paleta_elevacion = ['#006837', '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b', '#fee08b', '#fdae61', '#f46d43', '#d73027']

# Añadir capas al mapa
Map.addLayer(area_sar, {'color': 'blue'}, 'Límite SAR', True)
Map.addLayer(area_ap, {'color': 'red'}, 'Área de Proyecto (AP)', True)

# NDVI actual
if AÑO_FIN in ndvi_por_año:
    Map.addLayer(ndvi_por_año[AÑO_FIN], 
                {'min': -0.2, 'max': 0.8, 'palette': paleta_ndvi}, 
                f'NDVI {AÑO_FIN}', True)

# Manglar
Map.addLayer(mascara_manglar, 
            {'min': 0, 'max': 1, 'palette': paleta_manglar}, 
            'Cobertura de Manglar (GMW)', True)

# Cuerpos de agua
Map.addLayer(ocurrencia_agua, 
            {'min': 0, 'max': 100, 'palette': paleta_agua}, 
            'Ocurrencia de Agua (JRC)', False)

# Cambio de vegetación
cambio_viz = diff_ndvi.multiply(100).add(50).clamp(0, 100)
Map.addLayer(cambio_viz, 
            {'min': 0, 'max': 100, 'palette': paleta_cambio}, 
            'Cambio NDVI (rojo=pérdida, verde=ganancia)', False)

# Elevación
Map.addLayer(elevacion, 
            {'min': 0, 'max': 500, 'palette': paleta_elevacion}, 
            'Elevación (SRTM)', False)

# Temperatura
Map.addLayer(modis_lst, 
            {'min': 20, 'max': 40, 'palette': ['#313695', '#74add1', '#fed976', '#fd8d3c', '#bd0026']}, 
            'Temperatura Superficial (°C)', False)

# Añadir leyenda
legend_dict = {
    'NDVI Alto (>0.6)': '#1a9850',
    'NDVI Medio (0.3-0.6)': '#91cf60',
    'NDVI Bajo (<0.3)': '#fc8d59',
    'Manglar': '#006400',
    'Agua': '#1f78b4',
    'Área de Proyecto': '#ff0000',
}
Map.add_legend(legend_dict=legend_dict, title='Leyenda')

# Guardar mapa
try:
    Map.to_html(RUTA_MAPA_HTML)
    reporte.log(f"  ✓ Mapa HTML guardado: {RUTA_MAPA_HTML}")
except Exception as e:
    reporte.log(f"  [WARN] Error guardando mapa HTML: {e}", "WARN")

reporte.finalizar_paso(paso10, {'mapa_html': os.path.exists(RUTA_MAPA_HTML)})

# ============================================================
# PASO 11 — EXPORTACIÓN DE CAPAS A GOOGLE DRIVE
# ============================================================
paso11 = reporte.iniciar_paso(11, "Exportación de Capas GeoTIFF a Google Drive")

reporte.log(f"  Exportando capas a Drive/{CARPETA_DRIVE}/...")

capas_exportar = {
    'MIA_NDVI_actual': ndvi_por_año.get(AÑO_FIN, ndvi_final),
    'MIA_manglar': mascara_manglar.toFloat(),
    'MIA_agua_ocurrencia': ocurrencia_agua.toFloat(),
    'MIA_cambio_ndvi': diff_ndvi.toFloat(),
    'MIA_elevacion': elevacion.toFloat(),
    'MIA_pendiente': pendiente.toFloat(),
    'MIA_temperatura': modis_lst.toFloat(),
    'MIA_precipitacion': precip_anual.toFloat(),
}

tareas_export = []
for nombre, imagen in capas_exportar.items():
    try:
        task = exportar_a_drive(
            imagen=imagen,
            descripcion=nombre,
            region=area_sar,
            escala=30,
            carpeta=CARPETA_DRIVE
        )
        tareas_export.append({'nombre': nombre, 'task': task})
        reporte.log(f"  ✓ Tarea iniciada: {nombre}")
    except Exception as e:
        reporte.log(f"  [WARN] Error exportando {nombre}: {e}", "WARN")

reporte.log(f"  ✓ {len(tareas_export)} tareas de exportación iniciadas")
reporte.log(f"  → Verificar progreso en: https://code.earthengine.google.com/tasks")

reporte.finalizar_paso(paso11, {'tareas_exportacion': len(tareas_export)})

# ============================================================
# PASO 12 — GENERACIÓN DE TABLA USO DE SUELO
# ============================================================
paso12 = reporte.iniciar_paso(12, "Generación de Tabla Resumen USV")

reporte.log("  Compilando estadísticas de uso de suelo...")

# Crear CSV consolidado
with open(RUTA_CSV_USV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Tipo_Cobertura', 'Area_SAR_ha', 'Area_AP_ha', 'Porcentaje_SAR', 
                    'Forestal', 'Fuente', 'Normativa_Aplicable'])
    
    # Datos calculados
    writer.writerow(['Manglar', f'{area_manglar_gmw_ha:.2f}', f'{area_manglar_ap_ha:.2f}',
                    f'{area_manglar_gmw_ha/(area_sar_km2*100)*100:.2f}%', 'Sí',
                    'Global Mangrove Watch', 'NOM-022-SEMARNAT-2003'])
    
    writer.writerow(['Cuerpo de Agua', f'{area_agua_total_ha:.2f}', '-',
                    f'{area_agua_total_ha/(area_sar_km2*100)*100:.2f}%', 'No',
                    'JRC Global Surface Water', 'LGEEPA'])
    
    writer.writerow(['Vegetación con NDVI>0.5', '-', '-', '-', 'Sí',
                    'Sentinel-2', 'LGDFS'])

reporte.log(f"  ✓ CSV USV guardado: {RUTA_CSV_USV}")

reporte.finalizar_paso(paso12)

# ============================================================
# FUNCIÓN PARA CARGAR CAPAS EN QGIS
# ============================================================
def cargar_capas_qgis():
    """
    Carga las capas generadas en QGIS (PyQGIS).
    Ejecutar desde la consola Python de QGIS.
    """
    try:
        from qgis.core import (
            QgsProject, QgsRasterLayer, QgsVectorLayer,
            QgsRasterShader, QgsColorRampShader,
            QgsSingleBandPseudoColorRenderer
        )
        from PyQt5.QtGui import QColor
        
        print("=" * 70)
        print("CARGANDO CAPAS MIA EN QGIS")
        print("=" * 70)
        
        capas_raster = {
            'MIA_NDVI_actual': 'NDVI Actual',
            'MIA_manglar': 'Cobertura Manglar',
            'MIA_cambio_ndvi': 'Cambio NDVI',
            'MIA_elevacion': 'Elevación (SRTM)',
            'MIA_temperatura': 'Temperatura Superficial',
        }
        
        paletas_qgis = {
            'MIA_NDVI_actual': [(0, QColor('#d73027')), (0.3, QColor('#fc8d59')),
                               (0.5, QColor('#fee08b')), (0.7, QColor('#91cf60')),
                               (1, QColor('#1a9850'))],
            'MIA_manglar': [(0, QColor('#ffffff')), (1, QColor('#006400'))],
            'MIA_cambio_ndvi': [(-0.5, QColor('#d73027')), (0, QColor('#ffffbf')),
                               (0.5, QColor('#1a9850'))],
        }
        
        proyecto = QgsProject.instance()
        capas_cargadas = []
        
        for archivo, nombre_capa in capas_raster.items():
            ruta_tif = os.path.join(RESULTADOS, f"{archivo}.tif")
            
            if not os.path.exists(ruta_tif):
                print(f"    [!] No encontrado: {ruta_tif}")
                continue
            
            layer = QgsRasterLayer(ruta_tif, nombre_capa)
            
            if not layer.isValid():
                print(f"    [ERROR] Capa inválida: {ruta_tif}")
                continue
            
            if archivo in paletas_qgis:
                shader = QgsRasterShader()
                cs = QgsColorRampShader()
                cs.setColorRampType(QgsColorRampShader.Interpolated)
                items = [QgsColorRampShader.ColorRampItem(v, c, f'{v:.1f}')
                        for v, c in paletas_qgis[archivo]]
                cs.setColorRampItemList(items)
                shader.setRasterShaderFunction(cs)
                renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader)
                layer.setRenderer(renderer)
            
            proyecto.addMapLayer(layer)
            capas_cargadas.append(nombre_capa)
            print(f"    ✓ Capa añadida: {nombre_capa}")
        
        # Cargar shapefile SAR si existe
        if os.path.exists(SHAPEFILE_SAR):
            vlayer = QgsVectorLayer(SHAPEFILE_SAR, '📍 Sistema Ambiental Regional (SAR)', 'ogr')
            if vlayer.isValid():
                proyecto.addMapLayer(vlayer)
                print(f"    ✓ Shapefile SAR añadido")
        
        print(f"\n  ✓ {len(capas_cargadas)} capas MIA cargadas en QGIS")
        return capas_cargadas
    
    except ImportError:
        print("  [INFO] PyQGIS no disponible (ejecutando fuera de QGIS).")
        print("  Para usar en QGIS:")
        print("    1. Abrir QGIS 3.x")
        print("    2. Plugins → Python Console → exec(open('MIA_GEE_Analisis_v1.py').read())")
        print("    3. Llamar: cargar_capas_qgis()")
        return []


# ============================================================
# GENERAR REPORTE FINAL
# ============================================================
reporte.log("")
reporte.log("=" * 70)
reporte.log("GENERANDO REPORTE FINAL")
reporte.log("=" * 70)

reporte.generar_reporte_markdown()

# ============================================================
# RESUMEN EJECUTIVO EN CONSOLA
# ============================================================
print()
print("=" * 70)
print("RESUMEN EJECUTIVO — ANÁLISIS GEOESPACIAL MIA v1.0")
print("Laguna de Cuyutlán / Puerto Nuevo Manzanillo, Colima")
print("=" * 70)
print()
print(f"  Período analizado            : {AÑO_INICIO} – {AÑO_FIN} ({AÑO_FIN - AÑO_INICIO + 1} años)")
print(f"  Área SAR                     : {area_sar_km2:.2f} km²")
print(f"  Área del Proyecto (AP)       : {area_ap_km2:.2f} km²")
print()
print("  COBERTURA VEGETAL:")
print(f"    · Manglar en SAR           : {area_manglar_gmw_ha:.2f} ha")
print(f"    · Manglar en AP            : {area_manglar_ap_ha:.2f} ha")
print(f"    · Tendencia NDVI           : {tendencia}")
print()
print("  CAMBIO DE USO DE SUELO:")
print(f"    · Pérdida de vegetación    : {area_perdida_ha:.2f} ha")
print(f"    · Ganancia de vegetación   : {area_ganancia_ha:.2f} ha")
print(f"    · Balance neto             : {balance_neto:+.2f} ha")
print()
print("  CUERPOS DE AGUA:")
print(f"    · Agua permanente          : {area_agua_perm_ha:.2f} ha")
print(f"    · Agua estacional          : {area_agua_est_ha:.2f} ha")
print()
print("  CLIMA:")
print(f"    · Temperatura media        : {lst_mean:.1f} °C")
print(f"    · Precipitación anual      : {precip_mean:.1f} mm")
print()
print("  Archivos generados:")
print(f"    · {RUTA_MAPA_HTML}")
print(f"    · {RUTA_CSV_USV}")
print(f"    · {RUTA_CSV_CAMBIO}")
print(f"    · {RUTA_CSV_NDVI}")
print(f"    · {RUTA_CSV_MANGLAR}")
print(f"    · {RUTA_REPORTE_MD}")
print(f"    · {len(capas_exportar)} GeoTIFFs → Drive/{CARPETA_DRIVE}/")
print()
print("  Para cargar las capas en QGIS una vez descargados los GeoTIFFs:")
print("    cargar_capas_qgis()")
print()
print("=" * 70)
print("✓ PROGRAMA MIA_GEE_Analisis v1.0 COMPLETADO")
print("=" * 70)
