"""Servicio de captura de códigos de barras."""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
)
from selenium.webdriver.common.alert import Alert
import streamlit as st

from src.config import obtener_opciones_chrome, ConfiguracionURL
from src.utilidades import (
    recortar_imagen_alicuota_3,
    # recortar_imagen_alicuota,  # Desactivado — solo se usa alícuota 3
    crear_directorio_temporal
)


def cancelar_todas_las_alertas(driver, max_intentos=6):
    """
    Cancela TODAS las alertas pendientes en bucle.
    REDCap puede lanzar múltiples alertas seguidas.
    """
    alertas_canceladas = 0
    for _ in range(max_intentos):
        try:
            WebDriverWait(driver, 1.5).until(EC.alert_is_present())
            alert = Alert(driver)
            alert.dismiss()  # CANCELAR siempre — no borra valores
            alertas_canceladas += 1
            time.sleep(0.5)
        except Exception:
            break
    if alertas_canceladas > 0:
        st.warning(f"⚠️ {alertas_canceladas} alerta(s) REDCap canceladas")
    return alertas_canceladas


def capturar_alicuota_con_dropdown(driver, wait, numero_alicuota, carpeta, record_id):
    """
    Captura código de barras de la alícuota indicada.
    ACTUALMENTE SOLO SE USA ALÍCUOTA 3.

    Alícuotas desactivadas temporalmente:
    - Alícuota 4 → selector: tr#alic4_barcode-tr td.labelrc
    - Alícuota 5 → selector: tr#alic5_barcode-tr td.labelrc
    - Alícuota 6 → selector: tr#alic6_barcode-tr td.labelrc
    """
    try:
        # Cancelar alertas pendientes antes de empezar
        cancelar_todas_las_alertas(driver)

        nombre_dropdown = f"alic{numero_alicuota}_dest_2"
        st.info(f"🔍 Buscando dropdown: {nombre_dropdown}")

        elemento_dropdown = wait.until(
            EC.presence_of_element_located((By.NAME, nombre_dropdown))
        )

        # Forzar visibilidad del dropdown con JavaScript
        driver.execute_script(
            "arguments[0].style.display='block'; arguments[0].style.visibility='visible';",
            elemento_dropdown
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            elemento_dropdown
        )
        time.sleep(0.5)

        # Cancelar alertas después del scroll
        cancelar_todas_las_alertas(driver)

        # Seleccionar MODERNA con JavaScript
        driver.execute_script(
            "arguments[0].value = '4'; arguments[0].dispatchEvent(new Event('change'));",
            elemento_dropdown
        )
        st.info(f"✅ MODERNA seleccionada en alícuota {numero_alicuota}")
        time.sleep(1.0)

        # Cancelar TODAS las alertas en bucle
        cancelar_todas_las_alertas(driver)
        time.sleep(0.8)
        cancelar_todas_las_alertas(driver)
        time.sleep(0.5)

        # Selector del td completo — incluye barcode + número debajo
        if numero_alicuota == 3:
            selector_barcode = "tr#moderna_id_t-tr td.labelrc"
        # else:
        #     selector_barcode = f"tr#alic{numero_alicuota}_barcode-tr td.labelrc"  # Alícuotas 4, 5, 6 desactivadas

        st.info(f"🔍 Buscando código de barras: {selector_barcode}")

        # Cancelar alertas antes de buscar el barcode
        cancelar_todas_las_alertas(driver)

        # Esperar visibilidad natural del td completo
        elemento_barcode = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector_barcode))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            elemento_barcode
        )
        time.sleep(1.0)

        # Cancelar alertas antes de capturar screenshot
        cancelar_todas_las_alertas(driver)

        # Nomenclatura: {record_id}_alicuota_3.png
        nombre_archivo = f"{record_id}_alicuota_{numero_alicuota}.png"
        ruta_imagen = os.path.join(carpeta, nombre_archivo)
        elemento_barcode.screenshot(ruta_imagen)
        st.success(f"📸 Screenshot guardado: {nombre_archivo}")

        # Recorte alícuota 3 — lógica original sin modificar
        if numero_alicuota == 3:
            recortar_imagen_alicuota_3(ruta_imagen)
        # else:
        #     recortar_imagen_alicuota(ruta_imagen)  # Desactivado — alícuotas 4, 5, 6

        return ruta_imagen

    except UnexpectedAlertPresentException:
        cancelar_todas_las_alertas(driver)
        st.warning(f"⚠️ Alerta inesperada en alícuota {numero_alicuota} Record {record_id} — reintentando")
        try:
            time.sleep(1.0)
            cancelar_todas_las_alertas(driver)
            if numero_alicuota == 3:
                selector_barcode = "tr#moderna_id_t-tr td.labelrc"
            elemento_barcode = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector_barcode))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                elemento_barcode
            )
            time.sleep(1.0)
            nombre_archivo = f"{record_id}_alicuota_{numero_alicuota}.png"
            ruta_imagen = os.path.join(carpeta, nombre_archivo)
            elemento_barcode.screenshot(ruta_imagen)
            st.success(f"📸 Screenshot guardado en reintento: {nombre_archivo}")
            if numero_alicuota == 3:
                recortar_imagen_alicuota_3(ruta_imagen)
            return ruta_imagen
        except Exception as e2:
            st.error(f"❌ Reintento fallido — alícuota {numero_alicuota} Record {record_id}: {str(e2)[:100]}")
            return None

    except TimeoutException:
        st.warning(f"⚠️ TIMEOUT — Alícuota {numero_alicuota} Record {record_id}: no visible — puede que no exista para este registro")
        return None
    except NoSuchElementException:
        st.warning(f"⚠️ NO EXISTE — Alícuota {numero_alicuota} Record {record_id}: elemento no existe")
        return None
    except Exception as e:
        st.error(f"❌ ERROR — Alícuota {numero_alicuota} Record {record_id}: {str(e)[:150]}")
        cancelar_todas_las_alertas(driver)
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
                st.error("❌ Chromedriver NO encontrado")
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
            st.error("❌ Login fallido")
            return []

        archivos_descargados = []

        for id_val in record_ids:
            try:
                # Cancelar alertas pendientes ANTES de navegar
                cancelar_todas_las_alertas(driver)

                url_laboratorio = ConfiguracionURL.url_laboratorio(id_val)
                st.info(f"🌐 Navegando a: {url_laboratorio}")

                try:
                    driver.get(url_laboratorio)
                except UnexpectedAlertPresentException:
                    cancelar_todas_las_alertas(driver)
                    driver.get(url_laboratorio)

                # Cancelar alertas al cargar la nueva página
                cancelar_todas_las_alertas(driver)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
                    )
                    st.success(f"✅ Página cargada — Record ID: {id_val}")
                except TimeoutException:
                    st.error(f"❌ Página NO cargó para Record ID {id_val}")
                    continue

                time.sleep(1.5)
                cancelar_todas_las_alertas(driver)

                # SOLO ALÍCUOTA 3 ACTIVA
                # Alícuotas desactivadas: 4, 5, 6
                for num_alicuota in [3]:
                    archivo_capturado = capturar_alicuota_con_dropdown(
                        driver, wait, num_alicuota, carpeta, id_val
                    )
                    if archivo_capturado:
                        archivos_descargados.append(archivo_capturado)
                    time.sleep(0.3)
                    cancelar_todas_las_alertas(driver)

            except Exception as e:
                cancelar_todas_las_alertas(driver)
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
