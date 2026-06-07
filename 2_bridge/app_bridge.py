from flask import Flask, jsonify, render_template
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    """Ruta principal que cargará la interfaz visual con los botones."""
    return render_template('index_bridge.html')

@app.route('/scan/sp500', methods=['GET'])
def scan_sp500():
    """Ruta que activará el botón del S&P 500."""
    try:
        print("🔌 Puente activando: Escáner S&P 500...")
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
    app.run(debug=True, host='0.0.0.0', port=5000)
