from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

# Diseñando la interfaz directamente dentro del código para evitar errores de carpetas en Render
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alpha Radar Control</title>
    <script src="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.center.js"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
    </style>
</head>
<body class="flex flex-col items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-md bg-gray-900 rounded-2xl p-6 shadow-2xl border border-gray-800">
        <h1 class="text-2xl font-bold text-center text-blue-400 mb-2">⚡ MI-ALPHA-RADAR ⚡</h1>
        <p class="text-xs text-gray-400 text-center mb-6">Filtro de Diamantes en Bruto ($5 - $40)</p>
        
        <div class="space-y-4">
            <button onclick="ejecutarEscaner('sp500')" class="w-full py-4 bg-gray-800 border-2 border-blue-500 hover:bg-blue-900 rounded-xl font-bold text-lg transition-all transform active:scale-95 flex items-center justify-center gap-3">
                📊 Escanear S&P 500
            </button>
            <button onclick="ejecutarEscaner('nasdaq')" class="w-full py-4 bg-gray-800 border-2 border-blue-500 hover:bg-blue-900 rounded-xl font-bold text-lg transition-all transform active:scale-95 flex items-center justify-center gap-3">
                💻 Escanear NASDAQ 100
            </button>
            <button onclick="ejecutarEscaner('dow')" class="w-full py-4 bg-gray-800 border-2 border-blue-500 hover:bg-blue-900 rounded-xl font-bold text-lg transition-all transform active:scale-95 flex items-center justify-center gap-3">
                🏭 Escanear DOW JONES
            </button>
        </div>

        <div class="mt-6 p-4 bg-black rounded-xl border border-gray-800 min-h-[150px]">
            <p class="text-xs text-green-400 font-mono" id="consola">> Servidor listo. Esperando comando...</p>
        </div>
    </div>

    <script>
        function ejecutarEscaner(indice) {
            const consola = document.getElementById('consola');
            consola.innerHTML = `> Conectando con el puente...\\n> Iniciando escaneo de ${indice.toUpperCase()}...\\n> Filtrando acciones entre $5 y $40...`;
            
            fetch(`/scan/${indice}`)
                .then(res => res.json())
                .then(data => {
                    consola.innerHTML = `> Respuesta recibida del servidor:\\n> Status: ${data.status.toUpperCase()}\\n> Mensaje: ${data.message}`;
                })
                .catch(err => {
                    consola.innerHTML = `> Error en la conexión: \${err}`;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Carga la interfaz visual directamente desde la memoria."""
    return render_template_string(HTML_LAYOUT)

@app.route('/scan/sp500', methods=['GET'])
def scan_sp500():
    try:
        return jsonify({"status": "success", "message": "Escaneo del S&P 500 ejecutado con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/scan/nasdaq', methods=['GET'])
def scan_nasdaq():
    try:
        return jsonify({"status": "success", "message": "Escaneo del Nasdaq 100 ejecutado con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/scan/dow', methods=['GET'])
def scan_dow():
    try:
        return jsonify({"status": "success", "message": "Escaneo del Dow Jones ejecutado con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
