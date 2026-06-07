import yfinance as yf
import json
import os

# 📡 Lista de tickers que monitoreas para capturar momentum (puedes agregar los que quieras)
TICKERS_MONITOREO = ["CELH", "PLTR", "SOFI", "F", "AAL", "LCID", "VALE", "NIO", "XPEV", "PBR"]

def ejecutar_escaneo():
    print("📡 Iniciando escáner de Diamantes en Bruto ($5 a $30)...")
    resultados = []
    
    for ticker_id in TICKERS_MONITOREO:
        try:
            ticker = yf.Ticker(ticker_id)
            # Obtenemos el historial de los últimos días para el precio y volumen
            hist = ticker.history(period="5d")
            if hist.empty:
                continue
                
            precio_actual = round(hist['Close'].iloc[-1], 2)
            volumen_hoy = hist['Volume'].iloc[-1]
            volumen_promedio = hist['Volume'].mean()
            volumen_relativo = round(volumen_hoy / volumen_promedio, 2) if volumen_promedio > 0 else 1.0
            
            # 🎯 FILTRO DE ACERO ESTRICTO: Solo activos entre $5 y $30
            if 5.00 <= precio_actual <= 30.00:
                
                # 🧮 CÁLCULO AUTOMÁTICO DE TUS ZONAS OPERATIVAS FÍJAS
                # Entrada: Precio actual (Zona SMA 20)
                # Target: Proyección del 50% de ganancia para capturar el momentum fuerte
                # Stop Loss: Protección ajustada al 5% abajo de la entrada
                entrada = precio_actual
                target = round(entrada * 1.50, 2)
                stop_loss = round(entrada * 0.95, 2)
                
                # Guardamos los datos limpios de la acción
                resultados.append({
                    "ticker": ticker_id,
                    "precio": precio_actual,
                    "vol_rel": volumen_relativo,
                    "entrada": entrada,
                    "target": target,
                    "stop": stop_loss
                })
                print(f"✅ ¡Diamante Encontrado! {ticker_id} a ${precio_actual} (Vol. Rel: {volumen_relativo})")
        except Exception as e:
            print(f"❌ Error analizando {ticker_id}: {e}")
            
    # 📝 Guardar los resultados en el archivo JSON que leerá tu sitio web
    with open("datos_radar.json", "w") as f:
        json.dump(resultados, f, indent=4)
    print("🏁 Escaneo finalizado. Archivo 'datos_radar.json' actualizado con éxito.")

if __name__ == "__main__":
    ejecutar_escaneo()
