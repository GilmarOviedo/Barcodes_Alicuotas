"""Servicio de captura de códigos de barras."""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import streamlit as st

from src.config import obtener_opciones_chrome, ConfiguracionURL
from src.utilidades import (
    recortar_imagen_alicuota_3,
    recortar_imagen_alicuota,
    crear_directorio_temporal
)


def capturar_alicuota_con_dropdown(driver, wait, numero_alicuota, carpeta, record_id):
    try:
        nombre_dropdown = f"alic{numero_alicuota}_dest_2"
        st.info(f"🔍 Buscando dropdown: {nombre_dropdown}")

        elemento_dropdown = wait.until(
            EC.presence_of_element_located((By.NAME, nombre_dropdown))
        )
        st.success(f"✅ Dropdown encontrado: {nombre_dropdown}")

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            elemento_dropdown
        )
        time.sleep(0.5)

        select = Select(elemento_dropdown)
        select.select_by_value("4")
        st.info(f"✅ MODERNA seleccionada en alícuota {numero_alicuota}")
        time.sleep(1.5)

        if numero_alicuota == 3:
            id_barcode_tr = "moderna_id_t-tr"
        else:
            id_barcode_tr = f"alic{numero_alicuota}_barcode-tr"

        selector_barcode = f"tr#{id_barcode_tr}"
        st.info(f"🔍 Buscando código de barras: {selector_barcode}")

        elemento_barcode = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector_barcode))
        )
        st.success(f"✅ Código de barras encontrado: {selector_barcode}")

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            elemento_barcode
        )
        time.sleep(1.0)

        nombre_archivo = f"{record_id}_alicuota_{numero_alicuota}.png"
        ruta_imagen = os.path.join(carpeta, nombre_archivo)
        elemento_barcode.screenshot(ruta_imagen)
        st.success(f"📸 Screenshot guardado: {nombre_archivo}")

        if numero_alicuota == 3:
            recortar_imagen_alicuota_3(ruta_imagen)
        else:
            recortar_imagen_alicuota(ruta_imagen)

        return ruta_imagen

    except TimeoutException:
        st.error(f"❌ TIMEOUT — Alícuota {numero_alicuota} Record {record_id}: elemento no encontrado en 30s")
        st.code(f"URL actual: {driver.current_url}")
        return None
    except NoSuchElementException:
        st.error(f"❌ NO EXISTE — Alícuota {numero_alicuota} Record {record_id}: elemento no existe en la página")
        st.code(f"URL actual: {driver.current_url}")
        return None
    except Exception as e:
        st.error(f"❌ ERROR INESPERADO — Alícuota {numero_alicuota} Record {record_id}: {str(e)}")
        st.code(f"URL actual: {driver.current_url}")
        return None


def descargar_codigos_barras_alicuotas(record_ids, usuario, password):
    from src.servicios.redcap_login import realizar_login_redcap

    driver = None

    try:
        st.info("🔧 Iniciando Chrome...")
        opciones_chrome = obtener_opciones_chrome()
        carpeta = crear_directorio_temporal("codigos_barras_alicuotas")

        try:
            # Buscar chromedriver en rutas conocidas de Streamlit Cloud
            posibles_paths = [
                "/usr/bin/chromedriver",
                "/usr/lib/chromium-browser/chromedriver",
                "/usr/lib/chromium/chromedriver",
                "/snap/bin/chromium.chromedriver"
            ]

            chromedriver_path = None
            for path in posibles_paths:
                if os.path.exists(path):
                    chromedriver_path = path
                    st.info(f"🔍 Chromedriver encontrado en: {path}")
                    break

            if not chromedriver_path:
                st.error("❌ Chromedriver NO encontrado en ninguna ruta conocida")
                return []

            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=opciones_chrome)
            st.success("✅ Chrome iniciado correctamente")

        except Exception as e:
            st.error(f"❌ Chrome NO pudo iniciar: {str(e)}")
            return []

        wait = WebDriverWait(driver, 30)

        url_login = ConfiguracionURL.url_login()
        st.info(f"🔐 Login en: {url_login}")

        if not realizar_login_redcap(driver, wait, usuario, password, url_login):
            st.error("❌ Login fallido — verifica usuario/password en Secrets")
            return []

        archivos_descargados = []

        for id_val in record_ids:
            try:
                url_laboratorio = ConfiguracionURL.url_laboratorio(id_val)
                st.info(f"🌐 Navegando a: {url_laboratorio}")
                driver.get(url_laboratorio)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
                    )
                    st.success(f"✅ Página cargada — Record ID: {id_val}")
                except TimeoutException:
                    st.error(f"❌ Página NO cargó para Record ID {id_val}")
                    st.code(f"URL actual: {driver.current_url}")
                    continue

                time.sleep(1.5)

                for num_alicuota in [3, 4, 5, 6]:
                    archivo_capturado = capturar_alicuota_con_dropdown(
                        driver, wait, num_alicuota, carpeta, id_val
                    )
                    if archivo_capturado:
                        archivos_descargados.append(archivo_capturado)
                    time.sleep(0.3)

            except Exception as e:
                st.error(f"❌ Error en Record ID {id_val}: {str(e)}")
                continue

        st.info(f"📦 Total capturas obtenidas: {len(archivos_descargados)}")
        return archivos_descargados

    except Exception as e:
        st.error(f"❌ Error general: {str(e)}")
        return []

    finally:
        if driver:
            try:
                driver.quit()
                st.info("🔒 Chrome cerrado correctamente")
            except:
                pass
