"""Paquete de configuración."""

from .chrome_options import obtener_opciones_chrome
from .secrets import ConfiguracionCredenciales, ConfiguracionURL

__all__ = [
    'obtener_opciones_chrome',
    'ConfiguracionCredenciales',
    'ConfiguracionURL'
]

