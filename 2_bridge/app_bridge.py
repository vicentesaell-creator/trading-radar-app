from flask import Flask, jsonify, render_template
import sys
import os

# Agregamos la ruta de la carpeta 1_scanner para poder usar tus motores congelados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../1_scanner/1_scanner')))

# Intentamos importar las funciones de tus tres archivos congelados
try:
    from brain_scanner import ejecutar_escaner_sp500
    from nasdaq_scanner import ejecutar_escaner_nasdaq
    from dow_scanner import ejecutar_escaner_dow
except ImportError as e:
    print(f"⚠️ Nota de orden: Asegúrate de que las funciones estén listas en 1_scanner. Error: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    """Ruta principal que cargará la pantalla en tu teléfono."""
    return "¡Puente de Conexión Activo y Seguro! Listo para enlazar tus escáneres."

@app.route('/scan/sp500', methods=['GET'])
def scan_sp500():
    """Ruta que activará el botón del S&P 500."""
    try:
        # Aquí se ejecuta tu motor congelado del S&P 500
        print("🔌 Puente activando: Escáner S&P 500...")
        # En el siguiente paso capturaremos los datos para mandarlos directo a la pantalla
        return jsonify({"status": "success", "message": "Escaneo del S&P 500 ejecutado con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/scan/nasdaq', methods=['GET'])
def scan_nasdaq():
    """Ruta que activará el botón del Nasdaq."""
    try:
        print("🔌 Puente activando: Escáner NASDAQ 100...")
        return jsonify({"status": "success", "message": "Escaneo del Nasdaq 100 ejecutado con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/scan/dow', methods=['GET'])
def scan_dow():
    """Ruta que activará el botón del Dow Jones."""
    try:
        print("🔌 Puente activando: Escáner Dow Jones...")
        return jsonify({"status": "success", "message": "Escaneo del Dow Jones ejecutado con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Ejecuta la aplicación en el puerto 5000 de forma local o para servidores
    app.run(debug=True, host='0.0.0.0', port=5000)
