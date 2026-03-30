"""Servicio de envío de emails - OuraByte."""

import os
import ssl
import smtplib
import zipfile
from email.message import EmailMessage
from datetime import datetime


def crear_archivo_zip(archivos_adjuntos, record_ids):
    """Crea archivo ZIP con imágenes."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_zip = f"codigos_barras_alicuotas_{timestamp}.zip"
        ruta_zip = os.path.join("codigos_barras_alicuotas", nombre_zip)

        with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for ruta_archivo in archivos_adjuntos:
                if os.path.exists(ruta_archivo):
                    nombre_archivo = os.path.basename(ruta_archivo)
                    zipf.write(ruta_archivo, nombre_archivo)

        return ruta_zip if os.path.exists(ruta_zip) else None

    except Exception:
        return None


def enviar_email_con_zip(record_ids, archivos_adjuntos, email_destinatario,
                         email_remitente, email_password):
    """Envía email minimalista optimizado para Gmail."""
    try:
        ruta_zip = crear_archivo_zip(archivos_adjuntos, record_ids)

        if not ruta_zip or not os.path.exists(ruta_zip):
            return False

        em = EmailMessage()
        em['From'] = email_remitente
        em['To'] = email_destinatario
        em['Subject'] = "Códigos de Barras | Lab Muestras Humanas - PRESIENTE"

        # Métricas
        total_capturas = len(archivos_adjuntos)
        total_records = len(record_ids)
        zip_size = os.path.getsize(ruta_zip) / (1024 * 1024)
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")

        cuerpo_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap" rel="stylesheet">
        </head>
        <body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: 'Roboto', Arial, sans-serif;">

            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f5f5f5; padding: 30px 10px;">
                <tr>
                    <td align="center">

                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; width: 100%; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border: 1px solid #e0e0e0;">

                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #728C31 0%, #556620 100%); padding: 32px 24px; text-align: center;">
                                    <h1 style="margin: 0; color: #C8E100; font-size: 24px; font-weight: 700; letter-spacing: -0.5px;">🧬 Códigos de Barras Generados</h1>
                                    <p style="margin: 6px 0 0 0; color: rgba(255, 255, 255, 0.95); font-size: 13px; font-weight: 400;">Lab Muestras Humanas • Proyecto PRESIENTE</p>
                                </td>
                            </tr>

                            <!-- Content -->
                            <tr>
                                <td style="padding: 32px 24px;">

                                    <!-- Stats -->
                                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom: 28px;">
                                        <tr>
                                            <td width="50%" style="padding-right: 8px;">
                                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background: #f8f9fa; border: 2px solid #C8E100; border-radius: 10px; padding: 20px;">
                                                    <tr>
                                                        <td align="center">
                                                            <div style="font-size: 36px; font-weight: 700; color: #728C31; margin-bottom: 4px;">{total_capturas}</div>
                                                            <div style="font-size: 11px; color: #666666; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600;">Capturas Totales</div>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                            <td width="50%" style="padding-left: 8px;">
                                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background: #f8f9fa; border: 2px solid #C8E100; border-radius: 10px; padding: 20px;">
                                                    <tr>
                                                        <td align="center">
                                                            <div style="font-size: 36px; font-weight: 700; color: #728C31; margin-bottom: 4px;">{total_records}</div>
                                                            <div style="font-size: 11px; color: #666666; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600;">Record IDs</div>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- Info Card -->
                                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background: #fafafa; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 20px;">
                                        <tr>
                                            <td style="padding: 20px;">
                                                <h2 style="margin: 0 0 14px 0; color: #728C31; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">📦 Detalles del Archivo</h2>
                                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                                    <tr style="border-bottom: 1px solid #e8e8e8;">
                                                        <td style="color: #666666; font-size: 13px; padding: 10px 0; font-weight: 500;">Archivo</td>
                                                        <td align="right" style="color: #333333; font-size: 13px; padding: 10px 0; font-weight: 600;">{os.path.basename(ruta_zip)}</td>
                                                    </tr>
                                                    <tr style="border-bottom: 1px solid #e8e8e8;">
                                                        <td style="color: #666666; font-size: 13px; padding: 10px 0; font-weight: 500;">Tamaño</td>
                                                        <td align="right" style="color: #728C31; font-size: 13px; padding: 10px 0; font-weight: 700;">{zip_size:.2f} MB</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color: #666666; font-size: 13px; padding: 10px 0; font-weight: 500;">Fecha</td>
                                                        <td align="right" style="color: #333333; font-size: 13px; padding: 10px 0; font-weight: 600;">{fecha_generacion}</td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- Nomenclatura — solo alícuota 3 activa -->
                                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background: #fafafa; border-left: 3px solid #C8E100; border-radius: 6px; margin-bottom: 20px;">
                                        <tr>
                                            <td style="padding: 16px 18px;">
                                                <h3 style="margin: 0 0 10px 0; color: #728C31; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">📋 Nomenclatura de Archivos</h3>
                                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                                    <!-- Alícuota 3 — ACTIVA -->
                                                    <tr>
                                                        <td style="color: #555555; font-size: 12px; padding: 5px 0;">
                                                            <code style="background: #f0f0f0; color: #728C31; padding: 3px 8px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 11px; font-weight: 600;">{{ID}}_alicuota_3.png</code>
                                                            <span style="margin-left: 8px; color: #666666;">→ Alícuota 3</span>
                                                        </td>
                                                    </tr>
                                                    <!-- Alícuotas 4, 5, 6 — DESACTIVADAS temporalmente -->
                                                    <!-- <tr><td>{{ID}}_alicuota_4.png → Alícuota 4</td></tr> -->
                                                    <!-- <tr><td>{{ID}}_alicuota_5.png → Alícuota 5</td></tr> -->
                                                    <!-- <tr><td>{{ID}}_alicuota_6.png → Alícuota 6</td></tr> -->
                                                </table>
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- Alert -->
                                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background: #fffaeb; border: 1px solid #ffd966; border-left: 3px solid #ffb300; border-radius: 6px;">
                                        <tr>
                                            <td style="padding: 14px 16px;">
                                                <p style="margin: 0; color: #333333; font-size: 12px; line-height: 1.6;">
                                                    <strong style="color: #ff8f00; font-weight: 600;">💡 Instrucciones:</strong> Descarga y descomprime el archivo ZIP adjunto para acceder a las imágenes de los códigos de barras.
                                                </p>
                                            </td>
                                        </tr>
                                    </table>

                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="background: #fafafa; padding: 20px 24px; text-align: center; border-top: 1px solid #e0e0e0;">
                                    <div style="display: inline-block; background: #C8E100; color: #1a3a2a; padding: 6px 16px; border-radius: 16px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;">AUTOMATIZADO</div>
                                    <p style="margin: 6px 0 2px 0; color: #999999; font-size: 11px; font-weight: 400;">Sistema de Extracción de Códigos de Barras</p>
                                    <p style="margin: 2px 0; color: #728C31; font-size: 12px; font-weight: 600;">OuraByte • Proyecto PRESIENTE</p>
                                    <p style="margin: 2px 0 0 0; color: #cccccc; font-size: 10px;">{datetime.now().year}</p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        em.add_alternative(cuerpo_html, subtype="html")

        with open(ruta_zip, "rb") as f:
            em.add_attachment(
                f.read(),
                maintype="application",
                subtype="zip",
                filename=os.path.basename(ruta_zip)
            )

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto, timeout=30) as smtp:
            smtp.login(email_remitente, email_password)
            smtp.sendmail(email_remitente, email_destinatario, em.as_string())

        return True

    except Exception:
        return False
