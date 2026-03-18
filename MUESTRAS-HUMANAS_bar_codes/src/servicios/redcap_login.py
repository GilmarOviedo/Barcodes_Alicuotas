"""Servicio de autenticación en RedCap."""

import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def realizar_login_redcap(driver, wait, usuario, password, url_login):
    """
    Realiza login en RedCap.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        usuario (str): Usuario RedCap
        password (str): Contraseña RedCap
        url_login (str): URL de login
        
    Returns:
        bool: True si exitoso
    """
    try:
        st.info("Iniciando sesión en RedCap...")
        
        driver.get(url_login)
        
        campo_usuario = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)
        
        campo_password = wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        campo_password.clear()
        campo_password.send_keys(password)
        campo_password.send_keys(Keys.ENTER)
        
        wait.until(EC.url_contains("record_status_dashboard.php"))
        
        st.success("Sesión iniciada correctamente")
        return True
        
    except Exception as e:
        st.error(f"Error en login: {e}")
        return False