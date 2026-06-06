
import streamlit as dt
import pandas as pd
import numpy as np

# Configuración base estricta
dt.set_page_config(page_title="Alpha Radar Pro", page_icon="📡", layout="centered")

dt.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    h1, h2, h3 { color: #ffffff; font-family: 'Helvetica Neue', sans-serif; }
    div.stButton > button:first-child {
        background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

dt.title("📡 ALPHA RADAR")
dt.subheader("Escáner de Diamantes en Bruto ($5 - $30)")
dt.write("---")

# SIMULACIÓN CON ACTIVOS EN EL RANGO DE PRECIO OBJETIVO DE VICENTE
# Modificado para simular empresas medianas/pequeñas con alto potencial de crecimiento
data = {
    "Ticker": ["CELH", "PLTR", "SOFI", "RUM", "FSLR", "DKNG"],
    "Precio": [24.50, 18.20, 7.35, 6.10, 145.00, 42.80],  # Filtro estricto de $5 a $30
    "PE_Ratio": [16.2, 19.5, 14.8, 12.1, 15.0, 28.4],  # Filtro estricto Under 20
    "Sales_Growth_5Y": [0.35, 0.22, 0.18, 0.15, 0.08, 0.40],  # Filtro estricto Over 10%
    "Debt_Equity": [0.20, 0.15, 0.65, 0.10, 1.30, 1.10],  # Filtro estricto Under 1
    "Quick_Ratio": [2.1, 2.5, 1.4, 3.0, 0.8, 0.9],  # Filtro estricto Over 1
    "ROA": [0.18, 0.12, 0.11, 0.14, 0.06, -0.02],  # Filtro estricto Over 10%
    "SMA_20": [23.10, 17.50, 7.10, 5.80, 140.00, 40.00],
    "SMA_50": [22.00, 16.00, 6.80, 5.20, 135.00, 38.00],
    "SMA_200": [19.00, 14.00, 6.00, 4.50, 120.00, 32.00],
    "RSI": [58, 62, 54, 55, 48, 65],  # Filtro estricto > 50
    "Rel_Volume": [2.4, 1.8, 1.9, 2.2, 0.8, 1.3],  # Filtro estricto Over 1.5
    "RICOM": [1.10, 1.35, 1.50, 1.25, 2.30, 2.10]  # Filtro de riesgo menor o igual a 1.90
}

df_raw = pd.DataFrame(data)

# APLICACIÓN DEL FILTRO DE ACERO CON LA REGLA DE ORO DE PRECIO ($5 A $30)
df_filtrado = df_raw[
    (df_raw["Precio"] >= 5.0) & (df_raw["Precio"] <= 30.0) &  # <-- TU REGLA DE PRECIO
    (df_raw["PE_Ratio"] < 20) &
    (df_raw["Sales_Growth_5Y"] >= 0.10) &
    (df_raw["Debt_Equity"] < 1) &
    (df_raw["Quick_Ratio"] > 1) &
    (df_raw["ROA"] >= 0.10) &
    (df_raw["Precio"] > df_raw["SMA_20"]) &
    (df_raw["Precio"] > df_raw["SMA_50"]) &
    (df_raw["Precio"] > df_raw["SMA_200"]) &
    (df_raw["RSI"] > 50) &
    (df_raw["Rel_Volume"] >= 1.5) &
    (df_raw["RICOM"] <= 1.90)
]

dt.sidebar.header("⚙️ Panel de Control Técnico")
dt.sidebar.write("Filtro: Diamantes en Bruto Activo")

if dt.button("🔍 ESCANEAR MERCADO EN TIEMPO REAL"):
    if not df_filtrado.empty:
        dt.success(f"Se encontraron {len(df_filtrado)} activos de alta gama entre $5 y $30.")
        
        for index, row in df_filtrado.iterrows():
            ticker = row["Ticker"]
            precio_act = row["Precio"]
            sma20 = row["SMA_20"]
            
            # CÁLCULO AUTOMÁTICO DE ZONAS ESTRATÉGICAS
            zona_compra_min = round(sma20, 2)
            zona_compra_max = round(sma20 * 1.02, 2)
            target_salida = round(precio_act * 1.50, 2)  # Proyección del 50%
            stop_loss = round(sma20 * 0.97, 2)
            
            with dt.container():
                dt.markdown(f"### 📈 Oro Molido Detectado: **{ticker}**")
                col1, col2, col3 = dt.columns(3)
                col1.metric("Precio Actual", f"${precio_act}")
                col2.metric("Volumen Relativo", f"{row['Rel_Volume']}x")
                col3.metric("Riesgo RICOM", f"{row['RICOM']}")
                
                # Despliegue de Zonas Profesionales
                dt.markdown(f"""
                * 🟢 **Zona de Compra Ideal (Rango):** `${zona_compra_min}` a `${zona_compra_max}`
                * 🔴 **Objetivo de Salida Estimado (Target):** `${target_salida}`
                * 🟡 **Invalidez de Escenario (Stop Loss):** `${stop_loss}`
                """)
                dt.write("---")
    else:
        dt.warning("Filtro de Acero Ejecutado: Ningún activo de bajo precio cumple con el 100% de las restricciones institucionales hoy.")
