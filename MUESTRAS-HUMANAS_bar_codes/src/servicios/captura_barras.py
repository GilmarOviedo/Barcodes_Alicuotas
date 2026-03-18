"""Servicio de captura de códigos de barras."""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.config import obtener_opciones_chrome, ConfiguracionURL
from src.utilidades import (
    recortar_imagen_alicuota_3,
    recortar_imagen_alicuota,
    crear_directorio_temporal
)
#from src.servicios.redcap_login import realizar_login_redcap


def capturar_alicuota_con_dropdown(driver, wait, numero_alicuota, carpeta, record_id):
    """
    Selecciona MODERNA en dropdown y captura código de barras.
    Funciona para TODAS las alícuotas (3, 4, 5, 6).
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        numero_alicuota (int): Número de alícuota (3, 4, 5, 6)
        carpeta (str): Directorio destino
        record_id: ID del registro
        
    Returns:
        str or None: Ruta del archivo o None
    """
    try:
        # Nombre del dropdown
        nombre_dropdown = f"alic{numero_alicuota}_dest_2"
        
        # Esperar y localizar dropdown
        elemento_dropdown = wait.until(
            EC.presence_of_element_located((By.NAME, nombre_dropdown))
        )
        
        # Scroll al dropdown
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", 
            elemento_dropdown
        )
        time.sleep(0.5)  # Reducido de 0.8
        
        # Seleccionar MODERNA (value="4")
        select = Select(elemento_dropdown)
        select.select_by_value("4")
        
        # Esperar a que aparezca el código de barras
        time.sleep(1.5)  # Reducido de 2.0
        
        # ID del elemento de código de barras
        if numero_alicuota == 3:
            id_barcode_tr = "moderna_id_t-tr"
        else:
            id_barcode_tr = f"alic{numero_alicuota}_barcode-tr"
        
        selector_barcode = f"tr#{id_barcode_tr}"
        
        # Esperar y localizar código de barras
        elemento_barcode = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector_barcode))
        )
        
        # Scroll al código de barras
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", 
            elemento_barcode
        )
        time.sleep(1.0)  # Reducido de 1.4
        
        # Nombre del archivo - NOMENCLATURA UNIFICADA
        nombre_archivo = f"{record_id}_alicuota_{numero_alicuota}.png"
        ruta_imagen = os.path.join(carpeta, nombre_archivo)
        
        # Capturar screenshot
        elemento_barcode.screenshot(ruta_imagen)
        
        # RECORTAR SEGÚN LA ALÍCUOTA
        if numero_alicuota == 3:
            # Alícuota 3: Código a la IZQUIERDA
            recortar_imagen_alicuota_3(ruta_imagen)
        else:
            # Alícuotas 4, 5, 6: Código a la DERECHA
            recortar_imagen_alicuota(ruta_imagen)
        
        return ruta_imagen
        
    except (TimeoutException, NoSuchElementException, Exception):
        return None


def descargar_codigos_barras_alicuotas(record_ids, usuario, password):
    from src.servicios.redcap_login import realizar_login_redcap
    """
    Descarga 4 códigos de barras por Record ID.
    Todas las alícuotas están en la misma página de laboratorio.
    Args:
        record_ids (list): Lista de Record IDs
        usuario (str): Usuario RedCap
        password (str): Contraseña RedCap
    Returns:
        list: Lista de rutas de archivos descargados
    """
    driver = None
    
    try:
        opciones_chrome = obtener_opciones_chrome()
        carpeta = crear_directorio_temporal("codigos_barras_alicuotas")
        
        try:
            driver = webdriver.Chrome(options=opciones_chrome)
        except Exception:
            return []
        
        wait = WebDriverWait(driver, 30)
        
        # Login en RedCap
        url_login = ConfiguracionURL.url_login()
        if not realizar_login_redcap(driver, wait, usuario, password, url_login):
            return []
        
        archivos_descargados = []
        
        # Procesar cada Record ID
        for id_val in record_ids:
            try:
                # Navegar a la página de laboratorio
                url_laboratorio = ConfiguracionURL.url_laboratorio(id_val)
                driver.get(url_laboratorio)
                
                # Esperar carga inicial
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
                )
                time.sleep(1.5)  # Reducido de 2.0
                
                # Capturar las 4 alícuotas (3, 4, 5, 6)
                for num_alicuota in [3, 4, 5, 6]:
                    archivo_capturado = capturar_alicuota_con_dropdown(
                        driver, wait, num_alicuota, carpeta, id_val
                    )
                    
                    if archivo_capturado:
                        archivos_descargados.append(archivo_capturado)
                    
                    time.sleep(0.3)  # Reducido de 0.5
                
            except (TimeoutException, Exception):
                continue
        
        return archivos_descargados
        
    except Exception:
        return []
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
