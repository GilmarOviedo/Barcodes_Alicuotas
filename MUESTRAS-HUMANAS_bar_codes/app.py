
"""
Sistema de Extracción de Códigos de Barras - Alícuotas RedCap
"""

# 🔥 FIX IMPORTANTE PARA STREAMLIT CLOUD
import sys
import os

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

# -------------------------------------

import warnings
import streamlit as st

warnings.filterwarnings('ignore')

from src.config import ConfiguracionCredenciales
from src.utilidades import (
    procesar_archivo_csv,
    validar_record_ids_manual,
    generar_csv_ejemplo,
    limpiar_directorio
)
from src.servicios.captura_barras import descargar_codigos_barras_alicuotas
from src.servicios.email_service import enviar_email_con_zip
from src.estilos import obtener_estilos_css


def configurar_pagina():
    st.set_page_config(
        page_title="Extracción Códigos de Barras - Lab Muestras Humanas",
        page_icon="🧬",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown(obtener_estilos_css(), unsafe_allow_html=True)


def mostrar_encabezado():
    st.markdown(
        "<div class='header-container'>"
        "<h1>🧬 Extracción de Códigos de Barras</h1>"
        "<p class='subtitle'>Lab Muestras Humanas - Proyecto PRESIENTE</p>"
        "</div>",
        unsafe_allow_html=True
    )


def seccion_entrada_manual():
    texto_entrada = st.text_input(
        "Record IDs",
        placeholder="1, 2, 3, 4",
        label_visibility="collapsed"
    )
    return validar_record_ids_manual(texto_entrada)


def seccion_carga_csv():
    with st.expander("📄 Formato CSV"):
        df_ejemplo = generar_csv_ejemplo()
        st.dataframe(df_ejemplo, use_container_width=True, hide_index=True)
        
        csv_ejemplo = df_ejemplo.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar plantilla",
            data=csv_ejemplo,
            file_name="plantilla.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    archivo = st.file_uploader(
        "Cargar CSV",
        type=["csv"],
        label_visibility="collapsed"
    )
    
    if archivo:
        return procesar_archivo_csv(archivo)
    
    return None


def mostrar_resultados(archivos, record_ids):
    """Resultados de extracción"""
    esperadas = len(record_ids) * 4
    obtenidas = len(archivos)
    porcentaje = (obtenidas / esperadas * 100) if esperadas > 0 else 0
    
    st.markdown(
        f"""
        <div class='result-card'>
            <div class='result-header'>
                <h3>✓ Extracción Completada</h3>
            </div>
            <div class='result-stats'>
                <div class='stat-item'>
                    <span class='stat-value'>{obtenidas}</span>
                    <span class='stat-label'>Capturas obtenidas</span>
                </div>
                <div class='stat-item'>
                    <span class='stat-value'>{esperadas}</span>
                    <span class='stat-label'>Capturas esperadas</span>
                </div>
                <div class='stat-item'>
                    <span class='stat-value'>{porcentaje:.1f}%</span>
                    <span class='stat-label'>Tasa de éxito</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if archivos:
        with st.expander("🔍 Ver capturas obtenidas", expanded=False):
            cols = st.columns(4)
            for i, archivo in enumerate(archivos[:12]):
                with cols[i % 4]:
                    if os.path.exists(archivo):
                        nombre = os.path.basename(archivo)
                        st.image(archivo, caption=nombre, use_container_width=True)


def procesar_extraccion(record_ids, email_dest, config):
    try:
        with st.spinner(f"🔄 Procesando {len(record_ids)} Record IDs • {len(record_ids) * 4} capturas esperadas..."):
            usuario, password = config.obtener_credenciales_redcap()
            
            archivos = descargar_codigos_barras_alicuotas(
                record_ids,
                usuario,
                password
            )
        
        if archivos:
            mostrar_resultados(archivos, record_ids)
            
            with st.spinner("📧 Enviando email..."):
                remitente, password_email = config.obtener_credenciales_email()
                
                if enviar_email_con_zip(
                    record_ids,
                    archivos,
                    email_dest,
                    remitente,
                    password_email
                ):
                    st.success("✓ Email enviado correctamente")
                    limpiar_directorio("codigos_barras_alicuotas")
                else:
                    st.error("✗ Error al enviar email")
        else:
            st.error("✗ No se obtuvieron capturas. Verifica los Record IDs.")
            
    except Exception as e:
        st.error(f"✗ Error en el proceso: {str(e)}")


def main():
    configurar_pagina()
    mostrar_encabezado()
    
    try:
        config = ConfiguracionCredenciales()
    except Exception:
        st.error("✗ Error: Verifica las credenciales en Secrets")
        st.stop()
    
    st.markdown("<div class='section-header'>Paso 1: Método de Entrada</div>", unsafe_allow_html=True)
    
    metodo = st.radio(
        "Método",
        ["Entrada Manual", "Carga CSV"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    record_ids = []
    
    if metodo == "Entrada Manual":
        record_ids = seccion_entrada_manual()
    else:
        record_ids = seccion_carga_csv() or []
    
    if record_ids:
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div class='info-pill'>
                <span class='pill-icon'>📊</span>
                <span class='pill-text'>{len(record_ids)} Record IDs • {len(record_ids) * 4} capturas</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<div class='section-header'>Paso 2: Email de Destino</div>", unsafe_allow_html=True)
        
        email = st.text_input(
            "Email",
            placeholder="ejemplo@dominio.com",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Iniciar Extracción", type="primary", use_container_width=True):
            if not email.strip() or "@" not in email:
                st.error("✗ Ingresa un email válido")
            else:
                procesar_extraccion(record_ids, email, config)


if __name__ == "__main__":
    main()

