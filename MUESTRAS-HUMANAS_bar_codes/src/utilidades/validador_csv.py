"""Validador y procesador de archivos CSV."""

import pandas as pd
import streamlit as st


def procesar_archivo_csv(archivo_cargado):
    """
    Procesa CSV y extrae Record IDs válidos.
    
    Args:
        archivo_cargado: Archivo desde st.file_uploader
        
    Returns:
        list: Lista de Record IDs válidos o None
    """
    try:
        df = pd.read_csv(archivo_cargado)
        
        if "record_id" not in df.columns:
            st.error("El CSV no contiene la columna 'record_id'")
            return None
        
        st.markdown("#### Vista Previa de Datos")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        st.info(f"Total de filas: {len(df)}")
        
        df["record_id_numeric"] = pd.to_numeric(df["record_id"], errors="coerce")
        
        valores_invalidos = df.loc[df["record_id_numeric"].isnull(), "record_id"]
        
        if not valores_invalidos.empty:
            st.warning("Valores no numéricos encontrados (serán omitidos):")
            st.write(valores_invalidos.tolist())
        
        df_valido = df.dropna(subset=["record_id_numeric"]).copy()
        
        if len(df_valido) == 0:
            st.error("No hay Record IDs numéricos válidos")
            return None
        
        df_valido["record_id_int"] = df_valido["record_id_numeric"].astype(int)
        record_ids = df_valido["record_id_int"].tolist()
        
        st.success(f"Record IDs válidos encontrados: {len(record_ids)}")
        
        with st.expander(f"Ver lista completa ({len(record_ids)} IDs)"):
            st.write(record_ids)
        
        return record_ids
        
    except Exception as e:
        st.error(f"Error al procesar CSV: {e}")
        return None


def validar_record_ids_manual(texto_entrada):
    """
    Valida Record IDs ingresados manualmente.
    
    Args:
        texto_entrada (str): IDs separados por comas
        
    Returns:
        list: Lista de IDs válidos
    """
    record_ids = []
    
    if not texto_entrada.strip():
        return record_ids
    
    try:
        for rid in texto_entrada.split(","):
            rid = rid.strip()
            if rid:
                try:
                    record_ids.append(int(rid))
                except ValueError:
                    st.warning(f"'{rid}' no es válido (omitido)")
    except Exception as e:
        st.error(f"Error al parsear IDs: {e}")
    
    return record_ids


def generar_csv_ejemplo():
    """
    Genera DataFrame de ejemplo.
    
    Returns:
        pd.DataFrame: DataFrame con estructura ejemplo
    """
    return pd.DataFrame({
        "record_id": ["1", "2", "3", "4"]
    })