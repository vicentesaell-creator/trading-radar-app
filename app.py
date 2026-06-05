import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configuración de la página (Modo móvil optimizado)
st.set_page_config(page_title="Hidalgo Trading Radar", page_icon="🚀", layout="centered")

# Estilos visuales oscuros y limpios tipo Investing/TC2000
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background-color: #2ecc71; color: white; width: 100%; 
        border-radius: 8px; padding: 12px; font-weight: bold; border: none;
    }
    .card-compras { background-color: #1f242d; padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71; margin-bottom: 10px; }
    .card-tecnico { background-color: #1f242d; padding: 15px; border-radius: 10px; border-left: 5px solid #3498db; margin-bottom: 10px; }
    .card-espera { background-color: #1f242d; padding: 15px; border-radius: 10px; border-left: 5px solid #f1c40f; margin-bottom: 10px; }
    .ticker-title { font-size: 20px; font-weight: bold; color: #ffffff; }
    .badge { padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("Hidalgo Trading Radar 🚀")
st.write("Filtro móvil de valor y momentum en tiempo real.")

# Lista de activos optimizada ($5 - $20)
todo_wall_street = [
    "PLTR", "SOFI", "NIO", "LCID", "SNAP", "PINS", "PATH", "PTON", "FUBO", "CRSR", "U", "RBLX", "AFRM", "CHPT", "RUN", "PLUG", "AAL", "JBLU", "DAL", "UAL",
    "F", "GM", "CLF", "X", "FCX", "VALE", "AA", "NKLA", "OPEN", "BE", "GRWG", "BAC", "WFC", "T", "VZ", "CMCSA", "PBR", "BMY", "PFE", "SO", "HST", "KEY", "RF", "NYCB", 
    "ITUB", "BBD", "CCL", "NCLH", "RCL", "MGM", "CZR", "DKNG", "CNK", "IMAX", "PLAY", "TGT", "M", "JWN", "KSS", "AEO", "URBN", "GPS", "HOOD", "COIN", "MARA", "RIOT", 
    "CLV", "TLRY", "ACB", "CGC", "GOLD", "NEM", "AUY", "KGC", "BTG", "HL", "AG", "PAAS", "GFI", "CDE"
]
tickers_finales = list(set(todo_wall_street))

# Botón gigante para ejecutar el escáner desde el celular
if st.button("🔄 ESCANEAR WALL STREET AHORA"):
    st.write("🌐 Conectándose a los servidores de la bolsa... Analizando gráficos diarios...")
    
    resultados = []
    
    for ticker in tickers_finales:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("currentPrice", info.get("regularMarketPrice", 0))
            volume = info.get("averageVolume", 0)
            
            if not (5 <= price <= 20) or volume < 500000: continue
                
            pe_ratio = info.get("trailingPE", "N/A")
            peg_ratio = info.get("pegRatio", "N/A")
            
            hist = stock.history(period="250d")
            if len(hist) < 210: continue
                
            # Indicadores de tus pantallas de TC2000
            hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()
            hist['MA100'] = hist['Close'].rolling(window=100).mean()
            hist['MA200'] = hist['Close'].rolling(window=200).mean()
            
            c_close = hist['Close'].iloc[-1]
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

            # Radar de Momentum para celulares
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
                    detalles_tecnicos = "⚠️ CECA TECHO MA 200"
                    badge_color = "#d35400" 
            elif c_close > c_ema20:
                detalles_tecnicos = "📈 ALCISTA SOBRE EMA 20"
                badge_color = "#2c3e50"

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

    # Desplegar las tarjetas en formato lista vertical tipo app móvil
    if resultados:
        st.success(f"Se encontraron {len(resultados)} activos analizados:")
        for res in resultados:
            st.markdown(f"""
                <div class="{res['class']}">
                    <span class="ticker-title">{res['ticker']}</span> &nbsp;&nbsp; 
                    <span style="color: #bbb; font-size: 14px;">Precio: <b>{res['price']}</b> | RSI: <b>{res['rsi']}</b> | Vol: <b>{res['vol']}</b></span>
                    <div style="margin-top: 8px;">
                        <span class="badge" style="background-color: {res['badge_c']};">{res['tech']}</span>
                        <span class="badge" style="background-color: {res['scolor']}; float: right;">{res['status']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No hay activos que cumplan las condiciones estrictas hoy.")
