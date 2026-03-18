"""Servicio de captura de códigos de barras."""

import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
)
from selenium.webdriver.common.alert import Alert
import streamlit as st

from src.config import obtener_opciones_chrome, ConfiguracionURL
from src.utilidades import (
    recortar_imagen_alicuota_3,
    recortar_imagen_alicuota,
    crear_directorio_temporal
)


def manejar_alerta_si_existe(driver):
    """Acepta cualquier alerta/popup de REDCap si está presente."""
    try:
        alert = Alert(driver)
        texto = alert.text
        st.warning(f"⚠️ Alerta REDCap detectada — aceptando: {texto[:80]}...")
        alert.dismiss()  # CANCELAR — no borra valores existentes
        time.sleep(0.5)
        return True
    except Exception:
        return False


def capturar_alicuota_con_dropdown(driver, wait, numero_alicuota, carpeta, record_id):
    try:
        # Manejar alerta antes de empezar
        manejar_alerta_si_existe(driver)

        nombre_dropdown = f"alic{numero_alicuota}_dest_2"
        st.info(f"🔍 Buscando dropdown: {nombre_dropdown}")

        elemento_dropdown = wait.until(
            EC.presence_of_element_located((By.NAME, nombre_dropdown))
        )

        # Forzar visibilidad con JavaScript si está oculto
        driver.execute_script(
            "arguments[0].style.display='block'; arguments[0].style.visibility='visible';",
            elemento_dropdown
        )

        # Scroll al dropdown
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            elemento_dropdown
        )
        time.sleep(0.5)

        # Manejar alerta después del scroll
        manejar_alerta_si_existe(driver)

        # Seleccionar MODERNA usando JavaScript para evitar problemas de visibilidad
        driver.execute_script(
            "arguments[0].value = '4'; arguments[0].dispatchEvent(new Event('change'));",
            elemento_dropdown
        )
        st.info(f"✅ MODERNA seleccionada en alícuota {numero_alicuota}")
        time.sleep(1.5)

        # Manejar alerta después de seleccionar
        manejar_alerta_si_existe(driver)

        if numero_alicuota == 3:
            id_barcode_tr = "moderna_id_t-tr"
        else:
            id_barcode_tr = f"alic{numero_alicuota}_barcode-tr"

        selector_barcode = f"tr#{id_barcode_tr}"
        st.info(f"🔍 Buscando código de barras: {selector_barcode}")

        elemento_barcode = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector_barcode))
        )

        # Forzar visibilidad del barcode
        driver.execute_script(
            "arguments[0].style.display='table-row'; arguments[0].style.visibility='visible';",
            elemento_barcode
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            elemento_barcode
        )
        time.sleep(1.0)

        manejar_alerta_si_existe(driver)

        nombre_archivo = f"{record_id}_alicuota_{numero_alicuota}.png"
        ruta_imagen = os.path.join(carpeta, nombre_archivo)
        elemento_barcode.screenshot(ruta_imagen)
        st.success(f"📸 Screenshot guardado: {nombre_archivo}")

        if numero_alicuota == 3:
            recortar_imagen_alicuota_3(ruta_imagen)
        else:
            recortar_imagen_alicuota(ruta_imagen)

        return ruta_imagen

    except UnexpectedAlertPresentException as e:
        manejar_alerta_si_existe(driver)
        st.warning(f"⚠️ Alerta inesperada en alícuota {numero_alicuota} Record {record_id} — continuando")
        return None
    except TimeoutException:
        st.warning(f"⚠️ TIMEOUT — Alícuota {numero_alicuota} Record {record_id}: no encontrado — puede que no exista para este registro")
        return None
    except NoSuchElementException:
        st.warning(f"⚠️ NO EXISTE — Alícuota {numero_alicuota} Record {record_id}: elemento no existe — puede que no aplique")
        return None
    except Exception as e:
        st.error(f"❌ ERROR — Alícuota {numero_alicuota} Record {record_id}: {str(e)[:150]}")
        manejar_alerta_si_existe(driver)
        return None


def descargar_codigos_barras_alicuotas(record_ids, usuario, password):
    from src.servicios.redcap_login import realizar_login_redcap

    driver = None

    try:
        st.info("🔧 Iniciando Chrome...")
        opciones_chrome = obtener_opciones_chrome()
        carpeta = crear_directorio_temporal("codigos_barras_alicuotas")

        try:
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

                # Manejar alerta al cargar la página
                manejar_alerta_si_existe(driver)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
                    )
                    st.success(f"✅ Página cargada — Record ID: {id_val}")
                except TimeoutException:
                    st.error(f"❌ Página NO cargó para Record ID {id_val}")
                    continue

                time.sleep(1.5)
                manejar_alerta_si_existe(driver)

                for num_alicuota in [3, 4, 5, 6]:
                    archivo_capturado = capturar_alicuota_con_dropdown(
                        driver, wait, num_alicuota, carpeta, id_val
                    )
                    if archivo_capturado:
                        archivos_descargados.append(archivo_capturado)
                    time.sleep(0.3)

            except Exception as e:
                manejar_alerta_si_existe(driver)
                st.error(f"❌ Error en Record ID {id_val}: {str(e)[:150]}")
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
