from flask import Flask, jsonify, render_template_string
import pandas as pd
import yfinance as yf
import io
from contextlib import redirect_stdout

app = Flask(__name__)

# ==============================================================================
# LÓGICA DE ESCANEO DE ACTIVOS - ENBUDO CALIBRADO (MÁS FLEXIBLE)
# ==============================================================================
def procesar_lista_activos(tickers, nombre_mercado):
    print("\n" + "=" * 65)
    print(f"🚀 Alpha Radar -> ESCANEO EN VIVO {nombre_mercado} (Filtros Calibrados)")
    print("=" * 65)
    
    resultados_finales = []
    
    for ticker in tickers:
        try:
            asset = yf.Ticker(ticker)
            info = asset.info
            
            # --- FILTROS FUNDAMENTALES ---
            if info.get('quoteType') != 'EQUITY': continue
            
            hist = asset.history(period='1y')
            if hist.empty or len(hist) < 200: continue
            last_close = hist['Close'].iloc[-1]
            
            # 1. Filtro base de precio (Tu regla de diamantes en bruto)
            if not (5 <= last_close <= 40): continue
            
            # 2. Relación de Ganancias razonable
            pe = info.get('trailingPE')
            if pe and pe >= 25: continue # Flexibilizado a 25 máximo si existe
            
            # 3. Margen de Valor Calibrado (Mínimo un 15% de espacio al Target Price)
            target_price = info.get('targetMeanPrice')
            if not target_price or target_price < (last_close * 1.15): continue
            
            # 4. Salud Financiera Básica
            debt_to_equity = info.get('debtToEquity')
            if debt_to_equity is not None and (debt_to_equity / 100.0) > 1.5: continue
            
            quick_ratio = info.get('quickRatio')
            if quick_ratio and quick_ratio < 0.8: continue
            
            # --- FILTROS TÉCNICOS (Estructura de Tendencia Fuerte) ---
            hist['SMA200'] = hist['Close'].rolling(window=200).mean()
            hist['SMA50'] = hist['Close'].rolling(window=50).mean()
            hist['SMA20'] = hist['Close'].rolling(window=20).mean()
            
            sma200 = hist['SMA200'].iloc[-1]
            sma50 = hist['SMA50'].iloc[-1]
            sma20 = hist['SMA20'].iloc[-1]
            
            # Mantener la estructura alcista institucional activa
            if last_close <= sma200 or last_close <= sma50: continue
            
            # Fuerza de impulso (RSI > 45 para dar más margen de entrada)
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            if pd.isna(rsi) or rsi <= 45: continue
            
            # Volumen promedio mínimo para poder entrar y salir rápido
            avg_volume = hist['Volume'].tail(20).mean()
            if avg_volume <= 100000: continue
            
            # --- CALCULO SIMPLIFICADO DE ENTRADA Y RIESGO ---
            ricom_calculado = round((last_close / sma20), 2)
            
            rango_compra = f"${round(sma20, 2)} - ${round(last_close, 2)}"
            rango_venta = f"${round(hist['High'].tail(20).max(), 2)}"
            
            resultados_finales.append({
                "Ticker": ticker,
                "Target Price": round(target_price, 2),
                "RICOM": ricom_calculado,
                "Rango de Compra": rango_compra,
                "Rango de Venta": rango_venta
            })
        except Exception:
            continue
            
    if resultados_finales:
        for activo in resultados_finales:
            print(f"🔹 Ticker: {activo['Ticker']}")
            print(f" • Target Price: ${activo['Target Price']}")
            print(f" • Rango de Compra: {activo['Rango de Compra']}")
            print(f" • Rango de Venta: {activo['Rango de Venta']}")
            print("-" * 50)
    else:
        print("ℹ️ Ningún activo cumple con los criterios en este momento. Ajustando radares...")

# ==============================================================================
# DISEÑO DE INTERFAZ WEB
# ==============================================================================
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alpha Radar Control</title>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 1rem; box-sizing: border-box; }
        .card { width: 100%; max-width: 500px; background-color: #111827; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); border: 1px solid #1f2937; }
        .btn-scan { width: 100%; padding: 1rem; background-color: #1e293b; border: 2px solid #3b82f6; border-radius: 0.75rem; font-weight: bold; color: white; cursor: pointer; text-align: left; margin-bottom: 1rem; transition: all 0.2s; }
        .btn-scan:hover { background-color: #1e3a8a; }
        .btn-scan:active { transform: scale(0.98); }
        .console-box { background-color: #000000; border: 1px solid #1e293b; font-family: monospace; white-space: pre-wrap; padding: 1rem; border-radius: 0.75rem; min-height: 200px; max-height: 400px; overflow-y: auto; font-size: 0.8rem; color: #34d399; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="card">
        <h1 style="font-size: 1.5rem; font-weight: bold; text-align: center; color: #60a5fa; margin-top: 0; margin-bottom: 0.5rem;">⚡ MI-ALPHA-RADAR ⚡</h1>
        <p style="font-size: 0.75rem; color: #9ca3af; text-align: center; margin-bottom: 1.5rem; margin-top: 0;">Filtro Optimizado de Diamantes ($5 - $40)</p>
        
        <button onclick="ejecutarEscaner('sp500')" class="btn-scan">📊 Escanear S&P 500</button>
        <button onclick="ejecutarEscaner('nasdaq')" class="btn-scan">💻 Escanear NASDAQ 100</button>
        <button onclick="ejecutarEscaner('dow')" class="btn-scan">🏭 Escanear DOW JONES</button>

        <div class="console-box" id="consola">> Radar calibrado listo. Esperando comando...</div>
    </div>

    <script>
        function ejecutarEscaner(tipoMercado) {
            var consola = document.getElementById('consola');
            consola.innerHTML = "> Conectando con el radar optimizado...\\n> Filtrando candidatos viables en vivo ($5 - $40)...";
            
            fetch('/scan?mercado=' + tipoMercado)
                .then(function(res) { return res.json(); })
                .then(function(data) {
                    if(data.status === "success") {
                        consola.innerHTML = data.output;
                    } else {
                        consola.innerHTML = "> ERROR EN EL RADAR:\\n\\n" + data.error;
                    }
                })
                .catch(function(err) {
                    consola.innerHTML = "> Error de red: " + err;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

@app.route('/scan', methods=['GET'])
def scan():
    from flask import request
    mercado = request.args.get('mercado')
    
    if mercado == 'dow':
        tickers = ["AAPL", "AMZN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "NVDA", "PG", "TRV", "UNH", "V", "VZ", "WMT", "XOM"]
        nombre = "DOW JONES"
    elif mercado == 'nasdaq':
        tickers = ["MDLZ", "MNST", "MSFT", "MU", "NFLX", "NVDA", "NXPI", "ORLY", "PANW", "PAYX", "PCAR", "PEP", "PYPL", "QCOM", "REGN", "ROST", "SBUX", "SIRI", "SNPS", "TEAM", "TMUS", "TSLA", "TXN", "VRSK", "VRTX", "WBA", "WBD", "WDAY", "XEL", "ZBRA", "AAPL", "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "ALGN", "AMAT", "AMD", "AMGN", "AMZN", "ANSS", "ASML", "AVGO", "AZN", "BIIB", "BKNG", "BKR", "CDNS", "CEG", "CHTR", "CPRT", "CSGP", "CSX", "CTAS", "CTSH", "DDOG", "DLTR", "DXCM", "EA", "EXC", "FAST", "FTNT", "GEHC", "GILD", "GOOG", "GOOGL", "HON", "IDXX", "ILMN", "INTC", "INTU", "ISRG", "KDP", "KLAC", "LRCX", "MAR", "MCHP", "MELI", "META", "MRVL", "MSI", "ODFL", "ON", "PDD", "TTD", "MDB", "ROP", "DASH", "CDW", "GE", "FANG", "CCEP", "LIN", "MSTR", "ARM"]
        nombre = "NASDAQ 100"
    elif mercado == 'sp500':
        tickers = ["F", "GM", "BAC", "T", "VZ", "PFE", "BMY", "WFC", "C", "AAL", "DAL", "UAL", "LUV", "XOM", "CVX", "COP", "HAL", "SLB", "AIG", "MET", "PRU", "HPQ", "HPE", "NTAP", "WBD", "PARA", "DIS", "CMCSA", "KMI", "WMB", "XPO", "KVUE", "BEN", "IVZ", "KHC", "MDLZ", "GIS", "CL", "K", "D", "SO", "DUK", "AEP", "PCG", "NEM", "FCX"]
        nombre = "S&P 500"
    else:
        return jsonify({"status": "error", "error": "Mercado no identificado."})
        
    try:
        f = io.StringIO()
        with redirect_stdout(f):
            procesar_lista_activos(tickers, nombre)
        output_data = f.getvalue()
        return jsonify({"status": "success", "output": output_data})
    except Exception as e:
        return jsonify({"status": "error", "error": f"Error interno: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
