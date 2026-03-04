# 📤 GUÍA: CÓMO SUBIR ARCHIVOS AL SERVIDOR
## InfraestructuraGIS - Universidad de Colima

---

## 🎯 ¿POR QUÉ NECESITO SUBIR ARCHIVOS?

GeoServer está instalado en un **servidor remoto** (no en tu computadora). Para que GeoServer pueda acceder a tus datos, primero debes transferir los archivos desde tu computadora al servidor.

**Proceso completo:**
```
Tu Computadora → Servidor (vía FTP/SSH) → GeoServer lee archivos → Publica capas
```

---

## 🖥️ OPCIÓN 1: USAR WINSCP (Windows - RECOMENDADO)

WinSCP es un programa gratuito para transferir archivos de forma visual (drag & drop).

### Paso 1: Descargar e Instalar WinSCP

1. Ve a: https://winscp.net/eng/download.php
2. Descarga **"Installation package"**
3. Ejecuta el instalador
4. Siguiente → Siguiente → Instalar
5. Abre WinSCP

### Paso 2: Conectar al Servidor

1. En la ventana de **Login**:
   - **File protocol**: SFTP
   - **Host name**: `gis.infraestructuragis.com`
   - **Port number**: `22`
   - **User name**: `igis`
   - **Password**: [Solicita al administrador]

2. Click en **"Save"** para guardar la conexión
   - **Site name**: InfraestructuraGIS
   - Click en **"OK"**

3. Click en **"Login"**

4. Si aparece "Warning - Unknown server key":
   - Click en **"Yes"** (solo la primera vez)

### Paso 3: Subir Archivos

1. **Panel izquierdo**: Tu computadora
2. **Panel derecho**: El servidor

3. En el **panel derecho**, navega a la carpeta de carga:
   ```
   /home/igis/uploads/
   ```

4. En el **panel izquierdo**, navega a la carpeta donde tienes tu archivo ZIP

5. **Arrastra** tu archivo ZIP desde el panel izquierdo al derecho

6. Espera a que se complete la transferencia
   - Verás una barra de progreso

7. **¡Listo!** Tu archivo ya está en el servidor

### Consejos WinSCP:
- ✅ Puedes crear carpetas en el servidor: Right-click → New → Directory
- ✅ Puedes subir múltiples archivos a la vez
- ✅ Guarda tu sesión para no volver a configurar

---

## 🖥️ OPCIÓN 2: USAR FILEZILLA (Windows/Mac/Linux)

FileZilla es otra alternativa gratuita multiplataforma.

### Paso 1: Descargar e Instalar

1. Ve a: https://filezilla-project.org/download.php?type=client
2. Descarga **"FileZilla Client"** (NO Server)
3. Instala el programa

### Paso 2: Conectar

1. Abre FileZilla
2. En la parte superior, completa:
   - **Host**: `sftp://gis.infraestructuragis.com`
   - **Username**: `igis`
   - **Password**: [Tu contraseña]
   - **Port**: `22`
3. Click en **"Quickconnect"**

4. Si aparece "Unknown host key":
   - Marca "Always trust this host"
   - Click en **"OK"**

### Paso 3: Subir Archivos

1. **Panel izquierdo (Local site)**: Tu computadora
2. **Panel derecho (Remote site)**: El servidor

3. En el panel derecho, navega a:
   ```
   /home/igis/uploads/
   ```

4. En el panel izquierdo, encuentra tu archivo ZIP

5. **Right-click** en el archivo → **Upload**
   - O simplemente **arrastra** el archivo al panel derecho

6. Espera a que termine la transferencia

---

## 💻 OPCIÓN 3: LÍNEA DE COMANDOS (Linux/Mac)

Si usas Linux o Mac, puedes usar `scp` desde la terminal.

### Comando básico:

```bash
scp ruta/a/mi_archivo.zip igis@gis.infraestruccturagis.com:/home/igis/uploads/
```

### Ejemplo real:

```bash
# Si tu archivo está en el Escritorio
scp ~/Desktop/municipios_colima.zip igis@gis.infraestruccturagis.com:/home/igis/uploads/

# Te pedirá la contraseña
# Escríbela y presiona Enter
# Verás el progreso de la transferencia
```

### Subir múltiples archivos:

```bash
scp archivo1.zip archivo2.zip archivo3.zip igis@gis.infraestruccturagis.com:/home/igis/uploads/
```

### Subir una carpeta completa:

```bash
scp -r /ruta/a/mi_carpeta igis@gis.infraestruccturagis.com:/home/igis/uploads/
```

---

## 💻 OPCIÓN 4: DESDE WINDOWS CMD/PowerShell

Windows 10/11 incluye `scp` nativo.

### Pasos:

1. Abre **PowerShell** o **CMD**
2. Navega a la carpeta de tu archivo:
   ```cmd
   cd C:\Users\TuUsuario\Desktop
   ```

3. Ejecuta:
   ```cmd
   scp mi_archivo.zip igis@gis.infraestruccturagis.com:/home/igis/uploads/
   ```

4. Ingresa la contraseña cuando te la pida
5. Espera la confirmación

---

## 📧 OPCIÓN 5: ENVIAR POR EMAIL (Para archivos pequeños)

Si tu archivo es menor a 25 MB y no tienes acceso SSH:

1. Comprime tu shapefile en un ZIP
2. Envía el archivo por email a: **sgonzalez@infraestructuragis.com**
3. En el asunto escribe: **"Subir datos a GeoServer"**
4. En el mensaje incluye:
   - **Nombre deseado** para la capa
   - **Descripción** breve
   - **Sistema de coordenadas** (si lo conoces)
   - Si debe ser **pública o privada**
5. El administrador subirá el archivo y te notificará

---

## ☁️ OPCIÓN 6: GOOGLE DRIVE / DROPBOX (Para archivos grandes)

Si tu archivo es mayor a 100 MB:

1. Sube tu archivo a **Google Drive** o **Dropbox**
2. Comparte el link (con permiso de descarga)
3. Envía el link por email a: sgonzalez@infraestructuragis.com
4. Incluye la misma información que en Opción 5
5. El administrador descargará y procesará el archivo

---

## ✅ DESPUÉS DE SUBIR: USAR EL IMPORTER

Una vez que tu archivo esté en el servidor:

### En GeoServer:

1. Login en: https://gis.infraestructuragis.com/geoserver/web
2. Menú izquierdo → **"Importer"**
3. **"Import data"**
4. **"Choose a data source"** → Selecciona **"Server files"**
5. Navega a `/home/igis/uploads/`
6. Selecciona tu archivo
7. **Next** → Configura → **Import**

---

## 📋 CHECKLIST ANTES DE SUBIR

Antes de transferir tu archivo, verifica:

- [ ] **Shapefile completo**:
  - [ ] .shp (geometrías)
  - [ ] .shx (índice)
  - [ ] .dbf (atributos)
  - [ ] .prj (proyección) ← **MUY IMPORTANTE**
  - [ ] .cpg (opcional - codificación)

- [ ] **Todo comprimido en ZIP**
  - Nombre del ZIP: sin espacios, sin acentos
  - Ejemplo: `municipios_colima_2024.zip`

- [ ] **Tamaño razonable**:
  - Menor a 100 MB: Subir directamente
  - Mayor a 100 MB: Consultar con administrador

- [ ] **Sistema de coordenadas conocido**:
  - EPSG:4326 (WGS84) → Recomendado
  - EPSG:6372 (ITRF2008 México)
  - EPSG:32614 (UTM Zona 14N - Colima)

---

## 🔐 CREDENCIALES SSH

Para acceder al servidor necesitas:

| Campo | Valor |
|-------|-------|
| **Host** | gis.infraestruccturagis.com |
| **Puerto** | 22 |
| **Usuario** | igis |
| **Contraseña** | [Solicitar al administrador] |
| **Carpeta de carga** | /home/igis/uploads/ |

**IMPORTANTE**: 
- No compartas estas credenciales
- Si olvidaste la contraseña, contacta a: sgonzalez@infraestructuragis.com

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Cuánto tiempo tarda en subir un archivo?**
R: Depende del tamaño y tu conexión a internet:
- 10 MB → ~30 segundos
- 50 MB → ~2 minutos
- 100 MB → ~5 minutos

**P: ¿Puedo eliminar archivos del servidor?**
R: Sí, desde WinSCP o FileZilla puedes eliminar archivos en `/home/igis/uploads/`. No elimines archivos de otras carpetas.

**P: ¿Puedo ver los archivos de otros usuarios?**
R: No, solo tienes acceso a la carpeta `/home/igis/uploads/`. Los archivos ya publicados están en otras carpetas protegidas.

**P: ¿Qué hago si la conexión SSH falla?**
R: Verifica:
1. Que el servidor esté encendido
2. Que tengas acceso a la red de la universidad
3. Que usuario y contraseña sean correctos
4. Contacta al administrador si el problema persiste

**P: ¿Puedo subir archivos desde mi celular?**
R: Sí, existen apps como "FTP Manager" (Android) o "Termius" (iOS) para transferir archivos por SSH desde móviles.

---

## 🆘 SOPORTE

Si tienes problemas subiendo archivos:

📧 **Email**: sgonzalez@infraestructuragis.com
📞 **Ext**: [312--------]

Incluye en tu mensaje:
- Qué método intentaste usar
- Mensaje de error (si hay)
- Captura de pantalla (si es posible)

---

**Última actualización**: Marzo 2026  
**Versión**: 1.0  
**Universidad de Colima - InfraestructuraGIS**
