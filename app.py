import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# CARGAR DATOS
# =========================
df = pd.read_excel("datos_modificados.xlsx")

# =========================
# NORMALIZACIÓN DE FECHAS 
# =========================
df["Fecha Emisión"] = pd.to_datetime(df["Fecha Emisión"], errors="coerce").dt.date
df["Fecha Vencimiento"] = pd.to_datetime(df["Fecha Vencimiento"], errors="coerce").dt.date

# =========================
# TÍTULO
# =========================
st.title("📊 Sistema de Gestión de Cartera")

# =========================
# FILTROS
# =========================
col1, col2 = st.columns(2)

with col1:
    empresa = st.selectbox(
        "Filtrar por Empresa",
        ["Todas"] + sorted(df["Empresa"].dropna().unique())
    )

with col2:
    estado = st.selectbox(
        "Filtrar por Estado",
        ["Todos", "PAGADO", "PENDIENTE", "VENCIDO", "ANULADO","GESTIONADO"]
    )

df_filtrado = df.copy()

if empresa != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Empresa"] == empresa]

if estado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Estado"] == estado]

# =========================
# TABLA PRINCIPAL
# =========================

df_mostrar = df_filtrado.copy()

df_mostrar["Valor"] = df_mostrar["Valor"].apply(
    lambda x: f"$ {x:,.0f}".replace(",", ".")
)
st.subheader(" Registros")
st.dataframe(df_mostrar, use_container_width=True)

# =========================
# GESTIÓN DE REGISTROS
# =========================
st.subheader("✔ Marcar como gestionado")

usuario = st.text_input("Nombre del gestor")

# crear lista visual amigable
opciones = (
    df_filtrado["No. Documento"].astype(str)
    + " | "
    + df_filtrado["Empresa"].astype(str)
    + " | "
    + df_filtrado["Tercero"].astype(str)
)

registro = st.selectbox(
    "Seleccione el registro",
    opciones
)

if st.button("Marcar como gestionado"):

    if usuario.strip() == "":
        st.warning("Ingresa el nombre del gestor")
    else:

        documento = registro.split(" | ")[0]

        ahora = datetime.now()

        df.loc[df["No. Documento"].astype(str) == documento, "Estado"] = "GESTIONADO"

        df.loc[df["No. Documento"].astype(str) == documento, "Responsable"] = usuario

        df.loc[df["No. Documento"].astype(str) == documento, "Fecha Gestión"] = ahora

        df.to_excel("datos_modificados.xlsx", index=False)

        st.success("Registro actualizado correctamente ✔")

        st.rerun()

# =========================
# SOPORTE (BÁSICO REQUERIDO)
# =========================
st.subheader("📎 Adjuntar soporte")

archivo = st.file_uploader("Subir archivo")

if archivo is not None:
    st.success("Archivo cargado (puedes ampliarlo guardándolo en carpeta)")

# =========================
# RESUMEN
# =========================
st.subheader("📌 Resumen")

st.write("Total registros:", len(df))
st.write("Total cartera:", df["Valor"].sum())
st.write("Empresas únicas:", df["Empresa"].nunique())
st.write("Registros vencidos:", len(df[df["Estado"] == "VENCIDO"]))