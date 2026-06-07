import os
import pandas as pd
import yfinance as yf

def ejecutar_escaner_dow():
    print("\n" + "=" * 65)
    print("🚀 Alpha Radar -> ESCANEO EN VIVO DOW JONES (Estrategia Completa)")
    print("=" * 65)
    
    tickers = [
        "AAPL", "AMZN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "HD",
        "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT",
        "NKE", "NVDA", "PG", "STR", "TRV", "UNH", "V", "VZ", "WMT", "XOM"
    ]
    
    resultados_finales = []
    
    for ticker in tickers:
        try:
            asset = yf.Ticker(ticker)
            info = asset.info
            
            # --- FILTROS FUNDAMENTALES ---
            # 1. Filtro de Tipo de Activo (Solo Acciones)
            if info.get('quoteType') != 'EQUITY': continue
            
            # 2. Filtro de Precio ($5 - $40)
            hist = asset.history(period='1y')
            if hist.empty or len(hist) < 200: continue
            last_close = hist['Close'].iloc[-1]
            if not (5 <= last_close <= 40): continue
            
            # 3. Relación de Ganancias (P/E Under 20)
            pe = info.get('trailingPE')
            if not pe or pe >= 20: continue
            
            # 4. Crecimiento de Ventas (Sales Growth 5Y > 10%)
            # Nota: yfinance entrega crecimiento reciente; usamos revenueGrowth como indicador de tracción
            rev_growth = info.get('revenueGrowth')
            if not rev_growth or rev_growth < 0.10: continue
            
            # 5. Margen de Valor (Target Price mínimo 50% por encima del precio actual)
            target_price = info.get('targetMeanPrice')
            if not target_price or target_price < (last_close * 1.50): continue
            
            # 6. Control de Apalancamiento (Debt/Equity Under 1)
            debt_to_equity = info.get('debtToEquity')
            if debt_to_equity is not None and (debt_to_equity / 100.0) >= 1: continue
            
            # 7. Liquidez Inmediata (Quick Ratio Over 1)
            quick_ratio = info.get('quickRatio')
            if not quick_ratio or quick_ratio <= 1: continue
            
            # 8. Eficiencia de Activos (ROA Over 10%)
            roa = info.get('returnOnAssets')
            if not roa or roa < 0.10: continue
            
            # --- FILTROS TÉCNICOS ---
            # Calcular Medias Móviles
            hist['SMA200'] = hist['Close'].rolling(window=200).mean()
            hist['SMA50'] = hist['Close'].rolling(window=50).mean()
            hist['SMA20'] = hist['Close'].rolling(window=20).mean()
            
            sma200 = hist['SMA200'].iloc[-1]
            sma50 = hist['SMA50'].iloc[-1]
            sma20 = hist['SMA20'].iloc[-1]
            
            # 9. Estructura Alcista Mayor (Precio > SMA 200)
            if last_close <= sma200: continue
            # 10. Estructura Alcista Mediana (Precio > SMA 50)
            if last_close <= sma50: continue
            # 11. Estructura Alcista Corta (Precio > SMA 20)
            if last_close <= sma20: continue
            
            # 12. Fuerza de Compradores (RSI 14 > 50)
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            if pd.isna(rsi) or rsi <= 50: continue
            
            # 13. Volumen Promedio (Avg Volume > 100k)
            avg_volume = hist['Volume'].tail(20).mean()
            if avg_volume <= 100000: continue
            
            # 14. Presencia Institucional (Relative Volume > 1.5)
            volume_hoy = hist['Volume'].iloc[-1]
            relative_volume = volume_hoy / avg_volume if avg_volume > 0 else 0
            if relative_volume <= 1.5: continue
            
            # --- MÉTRICA ESPECIAL DE CONTROL DE RIESGO ---
            # Filtro Interno: RICOM menor o igual a 1.90
            ricom_calculado = round((last_close / sma20) * (1 + (1 / relative_volume)), 2)
            if ricom_calculado > 1.90: continue
            
            # Rangos sugeridos simplificados solicitados:
            rango_compra = f"${round(sma20, 2)} - ${round(last_close, 2)}"
            # Rango de venta aproximado basado en la resistencia más alta de las últimas 20 velas
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
            
    # MOSTRAR RESULTADOS RESUMIDOS Y SIMPLES EN CONSOLA
    if resultados_finales:
        for activo in resultados_finales:
            print(f"🔹 Ticker: {activo['Ticker']}")
            print(f" • Target Price: ${activo['Target Price']}")
            print(f" • RICOM: {activo['RICOM']}")
            print(f" • Rango de Compra: {activo['Rango de Compra']}")
            print(f" • Rango de Venta: {activo['Rango de Venta']}")
            print("-" * 50)
    else:
        print("❌ Ningún activo superó los filtros institucionales estrictos hoy.")

if __name__ == "__main__":
    ejecutar_escaner_dow()
