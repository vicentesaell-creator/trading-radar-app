128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
    print("\n" + "=" * 65)
        <div class="console-box" id="consola">> Radar listo en memoria interna. Esperando comando...</div>
    </div>

    <script>
        function ejecutarEscaner(tipoMercado) {
            var consola = document.getElementById('consola');
            consola.innerHTML = "> Conectando con el radar...\\n> Ejecutando tus 14 filtros fijos sobre la lista local...\\n> Analizando fundamentales y métricas en vivo...";
            
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
    
    # Listas fijas locales e institucionales para evitar problemas de carpetas externos
    if mercado == 'dow':
        tickers = [
            "AAPL", "AMZN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "HD",
            "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT",
            "NKE", "NVDA", "PG", "STR", "TRV", "UNH", "V", "VZ", "WMT", "XOM"
        ]
        nombre = "DOW JONES"
    elif mercado == 'nasdaq':
        tickers = [
            "MDLZ", "MNST", "MSFT", "MU", "NFLX", "NVDA", "NXPI", "ORLY", "PANW", "PAYX",
            "PCAR", "PEP", "PYPL", "QCOM", "REGN", "ROST", "SBUX", "SIRI", "SNPS", "TEAM",
            "TMUS", "TSLA", "TXN", "VRSK", "VRTX", "WBA", "WBD", "WDAY", "XEL", "ZBRA",
            "AAPL", "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "ALGN", "AMAT", "AMD",
            "AMGN", "AMZN", "ANSS", "ASML", "AVGO", "AZN", "BIIB", "BKNG", "BKR", "CDNS",
            "CEG", "CHTR", "CPRT", "CSGP", "CSX", "CTAS", "CTSH", "DDOG", "DLTR", "DXCM",
            "EA", "EXC", "FAST", "FTNT", "GEHC", "GILD", "GOOG", "GOOGL", "HON", "IDXX",
            "ILMN", "INTC", "INTU", "ISRG", "KDP", "KLAC", "LRCX", "MAR", "MCHP",
            "MELI", "META", "MRVL", "MSI", "ODFL", "ON", "PDD", "TTD", "MDB", "ROP",
            "DASH", "CDW", "GE", "FANG", "CCEP", "LIN", "MSTR", "ARM"
        ]
        nombre = "NASDAQ 100"
    elif mercado == 'sp500':
        tickers = [
            "F", "GM", "BAC", "T", "VZ", "PFE", "BMY", "WFC", "C", "AAL", "DAL", "UAL",
            "LUV", "XOM", "CVX", "COP", "HAL", "SLB", "AIG", "MET", "PRU", "HPQ", "HPE", "NTAP",
            "WBD", "PARA", "DIS", "CMCSA", "KMI", "WMB", "XPO", "KVUE", "BEN", "IVZ", "KHC",
            "MDLZ", "GIS", "CL", "K", "D", "SO", "DUK", "AEP", "PCG", "NEM", "FCX"
        ]
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
        return jsonify({"status": "error", "error": f"Error interno al escanear: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
