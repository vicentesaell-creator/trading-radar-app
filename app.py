
import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configuración de la página (Fuerza el Modo Oscuro Premium y Vista Móvil)
st.set_page_config(page_title="Alpha Radar 🚀", page_icon="🚀", layout="centered")

# Enlace oculto para que el iPhone reconozca la portada como el icono de la app
st.markdown('<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/vicentesael-creator/trading-radar-app/main/cover.png">', unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Fondo general oscuro estilo terminal de trading */
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Botón Principal Inteligente */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white; width: 100%; border-radius: 10px; 
        padding: 14px; font-weight: bold; border: none; font-size: 16px;
        box-shadow: 0px 4px 15px rgba(46, 204, 113, 0.3);
    }
    
    /* Tarjetas de los Activos Estilo Premium */
    .card-compras { background-color: #161a23; padding: 16px; border-radius: 12px; border-left: 6px solid #2ecc71; margin-bottom: 12px; }
    .card-tecnico { background-color: #161a23; padding: 16px; border-radius: 12px; border-left: 6px solid #3498db; margin-bottom: 12px; }
    .card-espera { background-color: #161a23; padding: 16px; border-radius: 12px; border-left: 6px solid #f1c40f; margin-bottom: 12px; }
    
    .ticker-title { font-size: 22px; font-weight: bold; color: #ffffff; letter-spacing: 0.5px; }
    .badge { padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold; color: white; display: inline-block; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)
# Carga la portada super pro (asegúrate de que el archivo se llame cover.png en GitHub)
import os
image_path = os.path.join(os.getcwd(), 'cover.png')
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)


st.title("Alpha Radar 🚀")
st.write("Filtro móvil de valor, momentum y análisis de fundamentos.")

# Lista de activos optimizada ($5 - $20)
todo_wall_street = [
    "PLTR", "SOFI", "NIO", "LCID", "SNAP", "PINS", "PATH", "PTON", "FUBO", "CRSR", "U", "RBLX", "AFRM", "CHPT", "RUN", "PLUG", "AAL", "JBLU", "DAL", "UAL",
    "F", "GM", "CLF", "X", "FCX", "VALE", "AA", "NKLA", "OPEN", "BE", "GRWG", "BAC", "WFC", "T", "VZ", "CMCSA", "PBR", "BMY", "PFE", "SO", "HST", "KEY", "RF", "NYCB", 
    "ITUB", "BBD", "CCL", "NCLH", "RCL", "MGM", "CZR", "DKNG", "CNK", "IMAX", "PLAY", "TGT", "M", "JWN", "KSS", "AEO", "URBN", "GPS", "HOOD", "COIN", "MARA", "RIOT", 
    "CLV", "TLRY", "ACB", "CGC", "GOLD", "NEM", "AUY", "KGC", "BTG", "HL", "AG", "PAAS", "GFI", "CDE"
]
tickers_finales = list(set(todo_wall_street))

if st.button("🔄 ESCANEAR WALL STREET AHORA"):
    st.write("🌐 Conectándose a Wall Street... Extrayendo métricas de Sardiña e Indicadores...")
    
    resultados = []
    
    for ticker in tickers_finales:
        try:
            stock = yf.Ticker(ticker)
            
            # Solución definitiva al error $nan leyendo el historial ultra-rápido reciente
            hist_reciente = stock.history(period="5d")
            if hist_reciente.empty: continue
            c_close = hist_reciente['Close'].iloc[-1]
            
            info = stock.info
            volume = info.get("averageVolume", 0)
            
            # Filtro básico de precio y volumen mínimo
            if not (5 <= c_close <= 20) or volume < 500000: continue
                
            pe_ratio = info.get("trailingPE", "N/A")
            peg_ratio = info.get("pegRatio", "N/A")
            
            hist = stock.history(period="250d")
            if len(hist) < 210: continue
                
            # Indicadores de TC2000
            hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()
            hist['MA100'] = hist['Close'].rolling(window=100).mean()
            hist['MA200'] = hist['Close'].rolling(window=200).mean()
            
            c_ema20 = hist['EMA20'].iloc[-1]
            c_ma100 = hist['MA100'].iloc[-1]
            c_ma200 = hist['MA200'].iloc[-1]
            
            p_close = hist['Close'].iloc[-2]
            p_ma100 = hist['MA100'].iloc[-2]
            p_ma200 = hist['MA200'].iloc[-2]
            
            # RSI (14)
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]

            is_undervalued = False
            if isinstance(pe_ratio, (int, float)) and 0 < pe_ratio <= 25:
                if isinstance(peg_ratio, (int, float)) and peg_ratio < 1.5:
                    is_undervalued = True

            # Filtros de Momentum
            detalles_tecnicos = "Tendencia Estable"
            badge_color = "#7f8c8d" 
            
            if (p_close <= p_ma100 and c_close > c_ma100) or (hist['Close'].iloc[-3] <= hist['MA100'].iloc[-3] and p_close > p_ma100):
                detalles_tecnicos = "🚀 ROMPIENDO MA 100"
                badge_color = "#9b59b6" 
            elif abs(c_close - c_ma200) / c_ma200 < 0.02:
                if c_close > c_ma200:
                    detalles_tecnicos = "🔥 ROMPIENDO MA 200"
                    badge_color = "#e67e22" 
                else:
                    detalles_tecnicos = "⚠️ CERCA TECHO MA 200"
                    badge_color = "#d35400" 
            elif c_close > c_ema20:
                detalles_tecnicos = "📈 ALCISTA SOBRE EMA 20"
                badge_color = "#34495e"

            # Semáforo de estados
            if is_undervalued and c_close > c_ema20:
                if current_rsi > 72:
                    status, card_class, s_color = "⏳ ESPERAR RETROCESO", "card-espera", "#e67e22"
                else:
                    status, card_class, s_color = "🔥 LISTA PARA COMPRAR", "card-compras", "#2ecc71"
            elif is_undervalued:
                status, card_class, s_color = "⏳ EN RECAMARA", "card-espera", "#f1c40f"
            elif c_close > c_ema20:
                status, card_class, s_color = "📈 SOLO TÉCNICO", "card-tecnico", "#3498db"
            else:
                continue

            resultados.append({
                "ticker": ticker, "price": f"${c_close:.2f}", "rsi": f"{current_rsi:.1f}" if not pd.isna(current_rsi) else "N/A",
                "vol": f"{volume/1000000:.1f}M", "tech": detalles_tecnicos, "badge_c": badge_color,
                "status": status, "class": card_class, "scolor": s_color
            })
        except:
            continue

    # Desplegar las tarjetas interactivas optimizadas para el celular
    if resultados:
        st.success(f"Se encontraron {len(resultados)} activos analizados:")
        for res in resultados:
            # Estructura visual HTML de la tarjeta
            st.markdown(f"""
                <div class="{res['class']}">
                    <span class="ticker-title">{res['ticker']}</span> &nbsp;&nbsp; 
                    <span style="color: #a0aab5; font-size: 15px;">Precio: <b>{res['price']}</b> | RSI: <b>{res['rsi']}</b> | Vol: <b>{res['vol']}</b></span>
                    <div style="margin-top: 6px;">
                        <span class="badge" style="background-color: {res['badge_c']};">{res['tech']}</span>
                        <span class="badge" style="background-color: {res['scolor']}; float: right;">{res['status']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Filtro interactivo del libro de Yoel Sardiña desplegable debajo de cada tarjeta
            with st.expander(f"📋 Filtro de Cuentas Millonarias ({res['ticker']})"):
                st.write("**Pasa el activo por el filtro del libro:**")
                st.checkbox("📊 1. Historial Financiero (¿Ingresos constantes y deudas bajo control?)", key=f"c1_{res['ticker']}")
                st.checkbox("🧠 2. Modelo de Negocio (¿Tiene ventaja competitiva clara a futuro?)", key=f"c2_{res['ticker']}")
                st.checkbox("👥 3. Liderazgo (¿Los jefes toman decisiones acertadas?)", key=f"c3_{res['ticker']}")
                st.checkbox("🎯 4. Valoración (¿Está por debajo de su valor intrínseco real?)", key=f"c4_{res['ticker']}")
    else:
        st.warning("No hay activos que cumplan las condiciones hoy.")
