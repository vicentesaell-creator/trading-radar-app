from flask import Flask, jsonify, render_template_string
import subprocess
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
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
        .btn-scan { background-color: #1e293b; border: 2px solid #3b82f6; transition: all 0.2s; }
        .btn-scan:hover { background-color: #1e3a8a; }
        .btn-scan:active { transform: scale(0.98); }
        .console-box { background-color: #000000; border: 1px solid #1e293b; font-family: monospace; white-space: pre-wrap; }
    </style>
</head>
<body style="display: flex; flex-direction: col; items-center; justify-content: center; min-height: 100vh; padding: 1rem; box-sizing: border-box;">
    <div style="width: 100%; max-width: 500px; background-color: #111827; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); border: 1px solid #1f2937;">
        <h1 style="font-size: 1.5rem; font-weight: bold; text-align: center; color: #60a5fa; margin-bottom: 0.5rem;">⚡ MI-ALPHA-RADAR ⚡</h1>
        <p style="font-size: 0.75rem; color: #9ca3af; text-align: center; margin-bottom: 1.5rem;">Filtro de Diamantes en Bruto ($5 - $40)</p>
        
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <button onclick="ejecutarEscaner('brain_scanner.py')" class="btn-scan" style="width: 100%; padding: 1rem; border-radius: 0.75rem; font-weight: bold; text-align: left; cursor: pointer; color: white;">
                📊 Escanear S&P 500
            </button>
            <button onclick="ejecutarEscaner('nasdaq_scanner.py')" class="btn-scan" style="width: 100%; padding: 1rem; border-radius: 0.75rem; font-weight: bold; text-align: left; cursor: pointer; color: white;">
                💻 Escanear NASDAQ 100
            </button>
            <button onclick="ejecutarEscaner('dow_scanner.py')" class="btn-scan" style="width: 100%; padding: 1rem; border-radius: 0.75rem; font-weight: bold; text-align: left; cursor: pointer; color: white;">
                🏭 Escanear DOW JONES
            </button>
        </div>

        <div class="console-box" id="consola" style="margin-top: 1.5rem; padding: 1rem; border-radius: 0.75rem; min-height: 200px; max-height: 400px; overflow-y: auto; font-size: 0.8rem; color: #34d399;">> Servidor listo. Esperando comando...</div>
    </div>

    <script>
        function ejecutarEscaner(archivoScript) {
            const consola = document.getElementById('consola');
            consola.innerHTML = `> Conectando con el puente...\\n> Iniciando escaneo mediante ${archivoScript}...\\n> Esto puede tardar unos segundos mientras yfinance procesa el mercado...`;
            
            fetch(`/scan?script=${archivoScript}`)
                .then(res => res.json())
                .then(data => {
                    if(data.status === "success") {
                        consola.innerHTML = data.output;
                    } else {
                        consola.innerHTML = `> ERROR EN EL ESCÁNER:\\n\\n\${data.error}`;
                    }
                })
                .catch(err => {
                    consola.innerHTML = `> Error de conexión con Render: \${err}`;
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

@app.route('/scan', methods=['GET'])
def scan():
    from flask import request
    script_name = request.args.get('script')
    
    # Definir la ruta exacta donde se encuentran tus escáneres en Render
    script_path = os.path.join(os.getcwd(), '1_scanner', '1_scanner', script_name)
    
    if not os.path.exists(script_path):
        return jsonify({
            "status": "error", 
            "error": f"No se encontró el archivo del escáner en la ruta: {script_path}"
        })
        
    try:
        # Ejecuta el script de python y captura lo que imprima en la consola
        resultado = subprocess.run(
            ['python', script_path], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return jsonify({
            "status": "success", 
            "output": resultado.stdout
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error", 
            "error": f"Error al ejecutar el script del escáner:\\nSTDOUT:\\n{e.stdout}\\nSTDERR:\\n{e.stderr}"
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
