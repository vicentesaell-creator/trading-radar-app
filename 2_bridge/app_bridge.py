from flask import Flask, jsonify, render_template_string
import subprocess
import os

app = Flask(__name__)

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
        <p style="font-size: 0.75rem; color: #9ca3af; text-align: center; margin-bottom: 1.5rem; margin-top: 0;">Filtro de Diamantes en Bruto ($5 - $40)</p>
        
        <button onclick="ejecutarEscaner('brain_scanner.py.')" class="btn-scan">📊 Escanear S&P 500</button>
        <button onclick="ejecutarEscaner('nasdaq_scanner.py')" class="btn-scan">💻 Escanear NASDAQ 100</button>
        <button onclick="ejecutarEscaner('dow_scanner.py')" class="btn-scan">🏭 Escanear DOW JONES</button>

        <div class="console-box" id="consola">> Servidor listo. Esperando comando...</div>
    </div>

    <script>
        function ejecutarEscaner(nombreArchivo) {
            var consola = document.getElementById('consola');
            consola.innerHTML = "> Conectando con el puente...\\n> Iniciando escaneo...\\n> Procesando mercado ($5 - $40)...";
            
            var rutaDestino = '/scan?script=' + nombreArchivo;
            
            fetch(rutaDestino)
                .then(function(res) { return res.json(); })
                .then(function(data) {
                    if(data.status === "success") {
                        consola.innerHTML = data.output;
                    } else {
                        consola.innerHTML = "> ERROR EN EL SERVIDOR:\\n\\n" + data.error;
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
    script_name = request.args.get('script')
    
    if not script_name:
        return jsonify({"status": "error", "error": "No se especificó el nombre del archivo."})
        
    # CORRECCIÓN DE RUTA ABSOLUTA: Forzamos ir a la raíz del proyecto para evitar que busque dentro de 2_bridge
    # Subimos un nivel en las carpetas para encontrar el directorio 1_scanner real
    ruta_raiz = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    script_path = os.path.join(ruta_raiz, '1_scanner', '1_scanner', script_name)
    
    if not os.path.exists(script_path):
        return jsonify({
            "status": "error", 
            "error": "No existe el archivo en la ruta del servidor: " + script_path
        })
        
    try:
        resultado = subprocess.run(
            ['python', script_path], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return jsonify({
            "status": "success", 
            "output": resultado.stdout if resultado.stdout else "El escáner corrió pero no arrojó texto."
        })
    except subprocess.CalledProcessError as e:
        error_detectado = e.stderr if e.stderr else e.stdout
        return jsonify({
            "status": "error", 
            "error": "Error interno al ejecutar el script:\\n" + error_detectado
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
