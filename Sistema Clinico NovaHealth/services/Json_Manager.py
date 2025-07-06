import json
import os

def guardar_json(ruta, datos):
    """
    Guarda datos en formato JSON.
    """
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def cargar_json(ruta):
    """
    Carga datos desde un archivo JSON.
    Retorna una lista o diccionario.
    """
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)