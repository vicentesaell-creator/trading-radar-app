from flask import Flask, jsonify, render_template_string
import sys
import os

app = Flask(__name__)

# Asegurar que Python pueda encontrar la carpeta de los escáneres para importar las funciones limpias
ruta_raiz = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
carpeta_scanner = os.path.join(ruta_raiz, '1_scanner', '1_scanner')
if carpeta_scanner not in sys.path:
    sys.path.append(carpeta_scanner)

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
        
        <button onclick="ejecutarEscaner('sp500')" class="btn-scan">📊 Escanear S&P 500</button>
        <button onclick="ejecutarEscaner('nasdaq')" class="btn-scan">💻 Escanear NASDAQ 100</button>
        <button onclick="ejecutarEscaner('dow')" class="btn-scan">🏭 Escanear DOW JONES</button>

        <div class="console-box" id="consola">> Servidor listo. Esperando comando...</div>
    </div>

    <script>
        function ejecutarEscaner(tipoMercado) {
            var consola = document.getElementById('consola');
            consola.innerHTML = "> Conectando con el puente...\\n> Iniciando escaneo institucional...\\n> Filtrando activos en vivo ($5 - $40)...";
            
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
    import io
    from contextlib import redirect_stdout
    
    mercado = request.args.get('mercado')
    
    try:
        # Capturar de manera directa e interna lo que imprimen tus escáneres sin usar subprocess externos
        f = io.StringIO()
        with redirect_stdout(f):
            if mercado == 'dow':
                from dow_scanner import ejecutar_escaner_dow
                ejecutar_escaner_dow()
            elif mercado == 'nasdaq':
                from nasdaq_scanner import ejecutar_escaner_nasdaq
                ejecutar_escaner_nasdaq()
            elif mercado == 'sp500':
                from brain_scanner import ejecutar_escaner_sp500
                ejecutar_escaner_sp500()
            else:
                return jsonify({"status": "error", "error": "Mercado no identificado."})
                
        output_data = f.getvalue()
        return jsonify({
            "status": "success", 
            "output": output_data if output_data else "El escáner terminó pero no generó texto."
        })
    except Exception as e:
        return jsonify({"status": "error", "error": f"Error al leer las listas locales: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
