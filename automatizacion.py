import pandas as pd
import re
import unicodedata

df = pd.read_excel("datos_prueba_Tecnica.xlsx")

# =========================
# LIMPIEZA BÁSICA
# =========================
df.columns = df.columns.str.strip()

df["Tipo"] = df["Tipo"].astype(str).str.upper().str.strip()
df["Estado"] = df["Estado"].astype(str).str.upper().str.strip()

# =========================
# HOMOLOGAR TIPO DOCUMENTO
# =========================
tipo_map = {
    "ORDEN DE COMPRA": "OC",
    "FACTURA DE VENTA": "FV",
    "RECIBO DE CAJA": "RC"
}

df["Tipo"] = df["Tipo"].replace(tipo_map)

# eliminar cualquier valor que no sea válido
df = df[df["Tipo"].isin(["OC", "FV", "RC"])]

# =========================
# EMPRESA 
# =========================
def limpiar_empresa(texto):
    texto = str(texto).upper().strip()

    # quitar acentos
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('utf-8')

    # quitar puntos
    texto = texto.replace(".", "")

    # quitar formas societarias
    texto = re.sub(r"\bSAS\b", "", texto)
    texto = re.sub(r"\bSA\b", "", texto)
    texto = re.sub(r"\bLTDA\b", "", texto)

    # limpiar espacios múltiples
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()

df["Empresa"] = df["Empresa"].apply(limpiar_empresa)

# =========================
# Homologacion
# =========================

empresas_validas = {
    "CUM": "CUMANDES",
    "EQUITEL": "EQUITEL",
    "INGE":  "INGENERGIA",
    "LAP": "LAP"
}
def homologar_empresa(nombre):
    for clave, oficial in empresas_validas.items():
        if clave in nombre:
            return oficial
        
    return nombre
df["Empresa"] = df["Empresa"].apply(homologar_empresa)

df = df[df["Empresa"].notna()]


# =========================
# NIT LIMPIO
# =========================
df["NIT"] = (
    df["NIT"]
    .astype(str)
    .str.replace(r"\D", "", regex=True)
    .str.strip()
)

# eliminar vacíos o inválidos
df = df[df["NIT"].notna()]
df = df[df["NIT"].str.len().between(8, 9)]

# =========================
# FECHAS
# =========================
df["Fecha Emisión"] = pd.to_datetime(df["Fecha Emisión"], errors="coerce").dt.date
df["Fecha Vencimiento"] = pd.to_datetime(df["Fecha Vencimiento"], errors="coerce").dt.date

# =========================
# VALORES
# =========================
df["Valor"] = (
    df["Valor"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

# =========================
# REGLA DE NEGOCIO
# =========================
df = df[df["Fecha Vencimiento"] >= df["Fecha Emisión"]]

# =========================
# DUPLICADOS
# =========================
df = df.drop_duplicates(subset=["No. Documento"], keep="first")

# =========================
# NULOS CRÍTICOS
# =========================
df = df.dropna(subset=["Tipo", "Fecha Emisión", "Fecha Vencimiento", "Valor"])

# =========================
# EXPORTAR
# =========================
df.to_excel("datos_modificados.xlsx", index=False)

print("Datos limpios y consistentes ✔")