"""Utilidades para procesamiento de imágenes."""
import os
from PIL import Image


def recortar_imagen_alicuota_3(ruta_imagen):
    """
    Recorta imagen para Alícuota 3.
    El código está a la IZQUIERDA, mantiene 2/3 desde el inicio.
    Args:
        ruta_imagen (str): Ruta de la imagen
    Returns:
        bool: True si exitoso
    """
    try:
        img = Image.open(ruta_imagen)
        ancho, alto = img.size
        nuevo_ancho = int(ancho *1/3)
        img_recortada = img.crop((0, 0, nuevo_ancho, alto))
        img_recortada.save(ruta_imagen)
        return True
    except Exception:
        return False


def recortar_imagen_alicuota(ruta_imagen):
    """
    Recorta imagen para alícuotas 4, 5, 6.
    El código está a la DERECHA, elimina 1/3 del inicio.
    Args:
        ruta_imagen (str): Ruta de la imagen
    Returns:
        bool: True si exitoso
    """
    try:
        img = Image.open(ruta_imagen)
        ancho, alto = img.size
        inicio_recorte = int(ancho * 1 / 3)
        img_recortada = img.crop((inicio_recorte, 0, ancho, alto))
        img_recortada.save(ruta_imagen)
        return True
    except Exception:
        return False


def crear_directorio_temporal(nombre_carpeta):
    """Crea directorio temporal."""
    os.makedirs(nombre_carpeta, exist_ok=True)
    return nombre_carpeta


def limpiar_directorio(ruta_directorio):
    """Elimina directorio y contenido."""
    import shutil
    try:
        if os.path.exists(ruta_directorio):
            shutil.rmtree(ruta_directorio)
    except Exception:
        pass
