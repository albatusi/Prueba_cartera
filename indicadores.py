import pandas as pd
import streamlit as st

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(
    page_title="Indicadores Financieros",
    layout="wide"
)

st.title("📊 Indicadores Financieros de Cartera")

# =========================
# CARGAR DATOS
# =========================
df = pd.read_excel("datos_modificados.xlsx")

# =========================
# NORMALIZAR FECHAS
# =========================
df["Fecha Emisión"] = pd.to_datetime(
    df["Fecha Emisión"],
    errors="coerce"
)

df["Fecha Vencimiento"] = pd.to_datetime(
    df["Fecha Vencimiento"],
    errors="coerce"
)

# =========================
# TOTAL CARTERA
# =========================
total_cartera = df["Valor"].sum()

# =========================
# CARTERA VENCIDA
# =========================
df_vencida = df[
    df["Fecha Vencimiento"] < pd.to_datetime("today")
]

total_vencida = df_vencida["Valor"].sum()

porcentaje_vencido = (
    (total_vencida / total_cartera) * 100
    if total_cartera > 0 else 0
)

# =========================
# EMPRESAS CON MÁS RIESGO
# =========================
top_empresas = (
    df.groupby("Empresa")["Valor"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# =========================
# BALANCE FACTURADO VS COBRADO
# =========================
facturado = df["Valor"].sum()

cobrado = df[
    df["Estado"] == "PAGADO"
]["Valor"].sum()

pendiente = facturado - cobrado

# =========================
# TRAMOS DE MORA
# =========================
df["Dias Mora"] = (
    pd.to_datetime("today") - df["Fecha Vencimiento"]
).dt.days

mora_0_30 = df[
    (df["Dias Mora"] <= 30) &
    (df["Dias Mora"] > 0)
]["Valor"].sum()

mora_31_60 = df[
    (df["Dias Mora"] <= 60) &
    (df["Dias Mora"] > 30)
]["Valor"].sum()

mora_60_mas = df[
    df["Dias Mora"] > 60
]["Valor"].sum()

# =========================
# KPIs PRINCIPALES
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Total Cartera",
        f"$ {total_cartera:,.0f}".replace(",", ".")
    )

with col2:
    st.metric(
        "⚠️ Cartera Vencida",
        f"$ {total_vencida:,.0f}".replace(",", ".")
    )

with col3:
    st.metric(
        "📉 % Vencido",
        f"{porcentaje_vencido:.2f}%"
    )

# =========================
# EMPRESAS CON MAYOR RIESGO
# =========================
st.subheader("🏢 Empresas con Mayor Riesgo")

top_empresas["Valor"] = top_empresas["Valor"].apply(
    lambda x: f"$ {x:,.0f}".replace(",", ".")
)

st.dataframe(
    top_empresas,
    use_container_width=True
)

# =========================
# ANTIGÜEDAD DE CARTERA
# =========================
st.subheader("⏳ Antigüedad de Cartera")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "0 - 30 días",
        f"$ {mora_0_30:,.0f}".replace(",", ".")
    )

with col5:
    st.metric(
        "31 - 60 días",
        f"$ {mora_31_60:,.0f}".replace(",", ".")
    )

with col6:
    st.metric(
        "60+ días",
        f"$ {mora_60_mas:,.0f}".replace(",", ".")
    )

# =========================
# BALANCE FINANCIERO
# =========================
st.subheader("📈 Balance Facturado vs Cobrado")

col7, col8, col9 = st.columns(3)

with col7:
    st.metric(
        "Facturado",
        f"$ {facturado:,.0f}".replace(",", ".")
    )

with col8:
    st.metric(
        "Cobrado",
        f"$ {cobrado:,.0f}".replace(",", ".")
    )

with col9:
    st.metric(
        "Pendiente",
        f"$ {pendiente:,.0f}".replace(",", ".")
    )

