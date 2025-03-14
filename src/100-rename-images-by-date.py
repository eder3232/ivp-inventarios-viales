import os
import glob
import shutil
from PIL import Image
from config import CONFIG
from pathlib import Path
from datetime import datetime

IMAGES_DIR = Path(CONFIG["IMAGES_RAW_DIR"])
IMAGES_RENAMED_BY_DATE = Path(CONFIG["IMAGES_RENAMED_BY_DATE_DIR"])

# Crear la carpeta de salida si no existe
os.makedirs(IMAGES_RENAMED_BY_DATE, exist_ok=True)

# Obtener todas las imágenes (JPG, PNG, etc.)
imagenes = glob.glob(os.path.join(IMAGES_DIR, "*.*"))


# Función para obtener la fecha de creación
def obtener_fecha_creacion(ruta):
    try:
        imagen = Image.open(ruta)
        info = imagen._getexif()
        if info and 36867 in info:  # 36867 = DateTimeOriginal en metadatos EXIF
            return datetime.strptime(info[36867], "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"No se pudo leer EXIF de {ruta}: {e}")

    # Si no tiene metadatos, usar la fecha de modificación del sistema
    return datetime.fromtimestamp(os.path.getctime(ruta))


# Obtener lista de imágenes con fechas
imagenes_con_fechas = [(ruta, obtener_fecha_creacion(ruta)) for ruta in imagenes]

# Ordenar por fecha (del más antiguo al más reciente)
imagenes_con_fechas.sort(key=lambda x: x[1])

# Copiar y renombrar en la carpeta de salida
for i, (ruta, fecha) in enumerate(imagenes_con_fechas, start=1):
    ext = os.path.splitext(ruta)[1]  # Obtener la extensión (.jpg, .png, etc.)
    nuevo_nombre = os.path.join(
        IMAGES_RENAMED_BY_DATE, f"{i}{ext}"
    )  # Crear nuevo nombre
    shutil.copy2(ruta, nuevo_nombre)  # Copiar y renombrar archivo
    print(f"Copiado y renombrado: {ruta} → {nuevo_nombre}")

print("Proceso completado.")
