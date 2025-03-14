# src/config.py
import json
from pathlib import Path

# Ruta del JSON de configuración
CONFIG_PATH = Path(__file__).resolve().parent / "paths.json"

# Cargar la configuración desde el JSON
with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config_data = json.load(file)

# Exportar el diccionario tal cual, sin modificar rutas
CONFIG = config_data
