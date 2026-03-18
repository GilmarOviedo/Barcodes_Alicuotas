"""Gestión de credenciales y URLs."""
import streamlit as st


class ConfiguracionCredenciales:
    """Gestión de credenciales desde Streamlit secrets."""
    
    def __init__(self):
        try:
            self.redcap_usuario = st.secrets["redcap_username"]
            self.redcap_password = st.secrets["redcap_password"]
            self.email_remitente = st.secrets["email_sender"]
            self.email_password = st.secrets["email_password"]
        except Exception as e:
            st.error("Error al cargar credenciales desde secrets")
            st.stop()
    
    def obtener_credenciales_redcap(self):
        """Retorna credenciales de RedCap."""
        return self.redcap_usuario, self.redcap_password
    
    def obtener_credenciales_email(self):
        """Retorna credenciales de email."""
        return self.email_remitente, self.email_password


class ConfiguracionURL:
    """URLs y endpoints de RedCap."""
    
    BASE_URL = "https://redcap.prisma.org.pe/redcap_v14.5.11"
    
    @staticmethod
    def url_login():
        """URL de login."""
        return f"{ConfiguracionURL.BASE_URL}/index.php?action=login"
    
    @staticmethod
    def url_laboratorio(record_id):
        """URL del formulario de Extraccion con códigos de barras."""
        return (
            f"{ConfiguracionURL.BASE_URL}/DataEntry/index.php?"
            f"pid=19&id={record_id}&event_id=59&page=extraccion"
        )
