import os
import piexif
from PIL import Image
from pathlib import Path
from config import CONFIG

ORIGEN_PATH = Path(CONFIG["IMAGES_RAW_DIR"])
DESTINO_PATH = Path(CONFIG["IMAGES_REDUCED_SIZE_DIR"])


def optimizar_imagen(ruta_entrada, ruta_salida, max_size=(300, 300), calidad=70):
    """
    Abre una imagen, la reduce a un tamaño máximo manteniendo la relación de aspecto,
    elimina los metadatos EXIF y la guarda con la calidad especificada.
    """
    with Image.open(ruta_entrada) as img:
        # Redimensionar manteniendo la relación de aspecto
        img.thumbnail(max_size)

        # Cargar y limpiar metadatos EXIF (si existen)
        exif_data = None
        if "exif" in img.info:
            exif_data = piexif.load(img.info["exif"])
            exif_data.pop("thumbnail", None)

        exif_bytes = piexif.dump(exif_data) if exif_data else None

        # Guardar imagen optimizada
        img.save(ruta_salida, quality=calidad, exif=exif_bytes)


def procesar_imagenes(origen_path, destino_path, max_size=(1280, 1280), calidad=70):
    if not os.path.exists(destino_path):
        os.makedirs(destino_path)

    # Recorremos todos los archivos del directorio de origen
    for nombre_archivo in os.listdir(origen_path):
        # Construir la ruta completa
        ruta_entrada = os.path.join(origen_path, nombre_archivo)

        # Validar que sea un archivo de imagen (opcional, depende de tu flujo)
        if not nombre_archivo.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # Crear ruta de salida (usando la misma extensión o forzando .jpg)
        nombre_salida, extension = os.path.splitext(nombre_archivo)
        ruta_salida = os.path.join(destino_path, f"{nombre_salida}-optimizado.jpg")

        # Llamamos a la función de optimización
        optimizar_imagen(ruta_entrada, ruta_salida, max_size=max_size, calidad=calidad)
        print(f"Imagen optimizada guardada en: {ruta_salida}")


# Uso
if __name__ == "__main__":
    procesar_imagenes(
        ORIGEN_PATH,
        DESTINO_PATH,
        max_size=(300, 300),  # Ajustar según tus necesidades
        calidad=70,  # Ajustar según tus necesidades
    )
