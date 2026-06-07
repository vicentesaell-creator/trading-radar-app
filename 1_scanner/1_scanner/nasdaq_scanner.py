import yfinance as yf
import pandas as pd
import numpy as np

def calcular_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def obtener_tickers_nasdaq100():
    try:
        url = "https://en.wikipedia.org/wiki/Nasdaq-100"
        tablas = pd.read_html(url)
        df = None
        for t in tablas:
            if 'Ticker' in t.columns:
                df = t
                column_name = 'Ticker'
                break
            elif 'Symbol' in t.columns:
                df = t
                column_name = 'Symbol'
                break
        if df is not None:
            return [str(t).replace('.', '-') for t in df[column_name].tolist()]
        return []
    except Exception:
        return []

def ejecutar_escaner_nasdaq():
    print("🚀 Iniciando Super Escáner: Alpha Radar -> ESCANEO EN VIVO NASDAQ 100...")
    tickers_lista = obtener_tickers_nasdaq100()
    if not tickers_lista:
        print("❌ No se pudo cargar la lista del Nasdaq 100.")
        return
        
    print(f"Analizando un total de {len(tickers_lista)} activos del Nasdaq.\n")
    resultados_finales = []

    for ticker in tickers_lista:
        try:
            asset = yf.Ticker(ticker)
            info = asset.info
            
            if info.get('quoteType', '').upper() != 'EQUITY':
                continue

            current_price = info.get('currentPrice')
            if current_price is None or current_price < 5.0 or current_price > 40.0:
                continue

            if info.get('trailingPE', 999) >= 20:
                continue

            sales_growth = info.get('revenueGrowth')
            if sales_growth is None or sales_growth < 0.10:
                continue

            target_price = info.get('targetMeanPrice')
            if target_price is None or current_price == 0:
                continue
            
            if ((target_price - current_price) / current_price) < 0.50:
                continue

            debt_equity = info.get('debtToEquity')
            if debt_equity is None or (debt_equity / 100.0) >= 1:
                continue

            if info.get('quickRatio', 0) <= 1 or info.get('returnOnAssets', 0) < 0.10:
                continue

            hist = asset.history(period="300d")
            if len(hist) < 200:
                continue

            hist['SMA200'] = hist['Close'].rolling(window=200).mean()
            hist['SMA50'] = hist['Close'].rolling(window=50).mean()
            hist['SMA20'] = hist['Close'].rolling(window=20).mean()
            hist['RSI14'] = calcular_rsi(hist)

            last_close = hist['Close'].iloc[-1]
            last_sma200 = hist['SMA200'].iloc[-1]
            last_sma50 = hist['SMA50'].iloc[-1]
            last_sma20 = hist['SMA20'].iloc[-1]
            last_rsi = hist['RSI14'].iloc[-1]

            if last_close <= last_sma200 or last_close <= last_sma50 or last_close <= last_sma20:
                continue

            if last_rsi is None or np.isnan(last_rsi) or last_rsi <= 50:
                continue

            avg_volume = info.get('averageVolume', 0)
            if avg_volume <= 100000:
                continue

            volume_hoy = hist['Volume'].iloc[-1]
            relative_volume = volume_hoy / avg_volume if avg_volume > 0 else 0
            if relative_volume <= 1.5:
                continue

            ricom_calculado = round((last_close / last_sma20) * (1 + (1 / relative_volume)), 2)
            if ricom_calculado > 1.90:
                continue

            rango_compra_min = round(last_sma20, 2)
            rango_compra_max = round(last_close, 2)
            proxima_resistencia = round(hist['High'].tail(20).max(), 2)

            resultados_finales.append({
                "Ticker": ticker,
                "Target Price": round(target_price, 2),
                "RICOM": ricom_calculado,
                "Rango de Compra": f"${rango_compra_min} - ${rango_compra_max}",
                "Resistencia": proxima_resistencia
            })
        except Exception:
            continue

    print("\n" + "=" * 65)
    if resultados_finales:
        print("🎯 ¡ACTIVOS ENCONTRADOS EN EL NASDAQ 100! ($5 - $40) 🎯")
        print("=" * 65)
        for activo in resultados_finales:
            print(f"🔹 ACTIVO: {activo['Ticker']}")
            print(f"  • Target Price (Consenso): ${activo['Target Price']}")
            print(f"  • Métrica RICOM: {activo['RICOM']}")
            print(f"  • Rango de Compra Ideal: {activo['Rango de Compra']}")
            print(f"  • Próxima Posible Resistencia: ${activo['Resistencia']}")
            print("-" * 65)
    else:
        print("❌ Ningún activo del Nasdaq 100 superó los filtros estrictos en el rango de $5-$40 hoy.")

if __name__ == "__main__":
    ejecutar_escaner_nasdaq()
