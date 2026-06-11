# ============================================================
#  CONFIGURACIÓN BUILDOZER - SmartStore PyMES (Kivy/KivyMD)
# ============================================================

[app]

# (str) Nombre de tu aplicación móvil
title = SmartStore PyMES

# (str) Nombre del paquete
package.name = smartstore_pymes

# (str) Dominio del paquete
package.domain = org.smartech

# (str) Dónde vive el código fuente
source.dir = .

# (list) Extensiones de archivos a incluir
source.include_exts = py,png,jpg,kv,atlas,txt

# (str) Versión de la aplicación
version = 1.0

# (list) REQUISITOS Y LIBRERÍAS (La receta de DeepSeek)
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pyrebase4,sqlite3,datetime,os

# (list) Orientación de la pantalla
orientation = portrait

# ============================================================
#  Configuración Específica de Android
# ============================================================

# (bool) Indicar si la app es pantalla completa
fullscreen = 0

# (list) PERMISOS DE ANDROID (Activados para Firebase e Internet)
android.permissions = android.permission.INTERNET, android.permission.ACCESS_NETWORK_STATE

# (int) Versiones de Android API (Configuración estable)
android.api = 30
android.minapi = 21
android.ndk = 26.3.11579264

# (bool) Aceptar automáticamente la licencia de Android SDK
android.accept_sdk_license = True

# (list) Arquitecturas para las que se compilará
android.archs = arm64-v8a, armeabi-v7a

# (bool) Permitir copia de seguridad automática de Android
android.allow_backup = True

# ============================================================
#  Configuración del Sistema Buildozer
# ============================================================

[buildozer]

# (int) Nivel de Log (2 muestra todo el proceso en vivo en pantalla)
log_level = 2

# (int) Mostrar advertencia si se corre como administrador
warn_on_root = 1