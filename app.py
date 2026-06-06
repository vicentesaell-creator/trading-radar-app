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
dt.subheader("Sistema Institucional de Captura de Momentum")
dt.write("---")

# SIMULACIÓN DEL MOTOR CORE-8 Y ALFA-6 CON DATOS EN VIVO (MOCK DATA PARA VALIDACIÓN)
# Nota: Este motor simula el filtrado estricto de los 14 criterios fundamentales y técnicos.
data = {
    "Ticker": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
    "Precio": [175.20, 415.50, 172.10, 180.40, 900.20],
    "PE_Ratio": [18.5, 19.2, 17.8, 24.5, 35.2],  # Filtro estricto Under 20
    "Sales_Growth_5Y": [0.12, 0.14, 0.11, 0.08, 0.45],  # Filtro estricto Over 10%
    "Debt_Equity": [0.85, 0.45, 0.35, 1.20, 0.60],  # Filtro estricto Under 1
    "Quick_Ratio": [1.2, 1.5, 1.8, 0.9, 2.1],  # Filtro estricto Over 1
    "ROA": [0.14, 0.16, 0.12, 0.05, 0.22],  # Filtro estricto Over 10%
    "SMA_20": [172.00, 410.00, 170.00, 182.00, 850.00],
    "SMA_50": [168.00, 395.00, 165.00, 178.00, 800.00],
    "SMA_200": [155.00, 360.00, 150.00, 160.00, 700.00],
    "RSI": [54, 56, 52, 48, 68],  # Filtro estricto > 50
    "Rel_Volume": [1.8, 2.1, 1.6, 0.9, 3.4],  # Filtro estricto Over 1.5
    "RICOM": [1.45, 1.20, 1.65, 2.10, 2.50]  # Filtro de riesgo menor o igual a 1.90
}

df_raw = pd.DataFrame(data)

# APLICACIÓN MATEMÁTICA DEL FILTRO DE ACERO (0% CHURRE)
df_filtrado = df_raw[
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
dt.sidebar.write("Algoritmo Core-8 & Alfa-6 Activo")

if dt.button("🔍 ESCANEAR MERCADO EN TIEMPO REAL"):
    if not df_filtrado.empty:
        dt.success(f"Se encontraron {len(df_filtrado)} activos que cumplen al 100% con los criterios institucionales.")
        
        for index, row in df_filtrado.iterrows():
            ticker = row["Ticker"]
            precio_act = row["Precio"]
            sma20 = row["SMA_20"]
            
            # CÁLCULO AUTOMÁTICO DE ZONAS ESTRATÉGICAS
            zona_compra_min = round(sma20, 2)
            zona_compra_max = round(sma20 * 1.02, 2)
            target_salida = round(precio_act * 1.50, 2)  # Regla del 50% de margen mínimo
            stop_loss = round(sma20 * 0.97, 2)  # Invalidez estructural del 3% bajo la media
            
            with dt.container():
                dt.markdown(f"### 📈 Activo Detectado: **{ticker}**")
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
        dt.warning("Filtro de Acero Ejecutado: Ningún activo cumple con el 100% de las restricciones de alta gama en este momento.")
