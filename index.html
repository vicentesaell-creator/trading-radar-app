<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Alpha Radar Pro</title>
    <link rel="icon" type="image/png" href="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=32&h=32&fit=crop">
    <link rel="apple-touch-icon" href="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=180&h=180&fit=crop">
    
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }
        body {
            background-color: #0d0f12;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding-bottom: 85px;
        }
        header {
            background-color: #14171c;
            padding: 18px;
            text-align: center;
            border-bottom: 1px solid #1f242d;
            position: sticky;
            top: 0;
            z-index: 900;
        }
        header h1 {
            font-size: 1.4rem;
            letter-spacing: 1px;
            color: #00e676;
        }
        header p {
            font-size: 0.8rem;
            color: #90a4ae;
            margin-top: 3px;
        }
        .container {
            padding: 15px;
            max-width: 600px;
            margin: 0 auto;
        }
        .page-content {
            display: none;
        }
        .page-content.active {
            display: block;
        }
        .card {
            background: linear-gradient(135deg, #14171c 0%, #1a1f26 100%);
            border: 1px solid #1f242d;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 15px;
        }
        .card h2 {
            font-size: 1.2rem;
            margin-bottom: 8px;
            color: #00e676;
        }
        .card p {
            color: #90a4ae;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        .btn-scan {
            background-color: #00e676;
            color: #0d0f12;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1rem;
            width: 100%;
            cursor: pointer;
            margin-top: 10px;
        }
        .ticker-card {
            border-left: 4px solid #00e676; 
            padding: 15px; 
            margin-top: 15px; 
            background: #14171c;
            cursor: pointer;
            transition: background 0.2s;
        }
        .ticker-card:active {
            background: #1f242d;
        }
        .widget-container {
            margin-top: 15px;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #1f242d;
            background: #14171c;
        }
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 65px;
            background-color: #14171c;
            border-top: 1px solid #1f242d;
            display: flex;
            justify-content: space-around;
            align-items: center;
            z-index: 1000;
            padding-bottom: env(safe-area-inset-bottom);
        }
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #90a4ae;
            text-decoration: none;
            font-size: 0.75rem;
            font-weight: 500;
            background: none;
            border: none;
            cursor: pointer;
            width: 25%;
            height: 100%;
            justify-content: center;
        }
        .nav-item.active {
            color: #00e676;
        }
        .nav-icon {
            font-size: 1.3rem;
            margin-bottom: 3px;
        }
        .selected-ticker-badge {
            background: #00e676;
            color: #0d0f12;
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
            display: inline-block;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

    <header>
        <h1>📡 ALPHA RADAR</h1>
        <p>Sistema de Captura de Momentum • V2.0</p>
    </header>

    <div class="container">
        
        <div id="page-radar" class="page-content active">
            <div class="card">
                <h2>Buscador de Diamantes en Bruto</h2>
                <p>Presiona el botón para consultar los activos reales filtrados. **Toca cualquier tarjeta** para cargar sus gráficas y noticias al instante.</p>
                <button class="btn-scan" onclick="cargarDatosRadar()">Consultar Radar Real ⚡</button>
            </div>
            <div id="radar-results"></div>
        </div>

        <div id="page-estrategias" class="page-content">
            <div class="card">
                <h2>Filtros de Acero Ajustados</h2>
                <p style="margin-bottom: 8px;">• Rango estricto de Precio: **$5.00 a $30.00**</p>
                <p style="margin-bottom: 8px;">• Volumen Institucional Relativo: **Mayor a 1.5**</p>
                <p>• Filtro de seguridad activado contra acciones de baja capitalización.</p>
            </div>
        </div>

        <div id="page-noticias" class="page-content">
            <div id="ticker-analisis-header" class="selected-ticker-badge">Ningún activo seleccionado</div>
            
            <div class="card">
                <h2>📊 Gráfica en Vivo</h2>
                <div class="widget-container" style="height: 350px;" id="tv-chart-wrapper">
                    <p style="padding: 20px; color: #90a4ae;">Selecciona una acción en el Radar para cargar la gráfica operativa.</p>
                </div>
            </div>

            <div class="card">
                <h2>📈 Salud y Perfil Técnico</h2>
                <div class="widget-container" style="height: 180px;" id="tv-technical-wrapper">
                    <p style="padding: 20px; color: #90a4ae;">Esperando activo...</p>
                </div>
            </div>

            <div class="card">
                <h2>📰 Noticias de Impacto Institucional & Earnings</h2>
                <div class="widget-container" style="height: 300px; overflow-y: auto;" id="tv-news-wrapper">
                    <p style="padding: 20px; color: #90a4ae;">Esperando activo...</p>
                </div>
            </div>
        </div>

        <div id="page-bitacora" class="page-content">
            <div class="card">
                <h2>Bitácora de Operaciones</h2>
                <p>Registro automatizado de tus planes de trading del día para mantener una disciplina estricta antes de cada sesión.</p>
            </div>
        </div>

    </div>

    <nav class="bottom-nav">
        <button class="nav-item active" onclick="switchPage('radar', this)">
            <span class="nav-icon">📡</span>
            <span>Radar</span>
        </button>
        <button class="nav-item" onclick="switchPage('estrategias', this)">
            <span class="nav-icon">⚡</span>
            <span>Estrategias</span>
        </button>
        <button class="nav-item" onclick="switchPage('noticias', this)">
            <span class="nav-icon">📊 Análisis</span>
        </button>
        <button class="nav-item" onclick="switchPage('bitacora', this)">
            <span class="nav-icon">📝</span>
            <span>Bitácora</span>
        </button>
    </nav>

    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script>
        let tickerSeleccionado = "";

        function switchPage(pageId, element) {
            const pages = document.querySelectorAll('.page-content');
            pages.forEach(page => page.classList.remove('active'));
            
            const buttons = document.querySelectorAll('.nav-item');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            document.getElementById('page-' + pageId).classList.add('active');
            element.classList.add('active');

            if (pageId === 'noticias' && tickerSeleccionado) {
                cargarAnalisisGrafico(tickerSeleccionado);
            }
        }

        // 📡 LECTURA REPARADA: Lee exactamente lo que genera tu Python
        function cargarDatosRadar() {
            const resultsContainer = document.getElementById('radar-results');
            resultsContainer.innerHTML = `
                <div class="card" style="text-align: center; border-color: #00e676; margin-top: 15px;">
                    <p style="color: #00e676; font-weight: bold; font-size: 1.1rem;">📡 Leyendo datos del mercado real...</p>
                </div>
            `;

            fetch('datos_radar.json?v=' + new Date().getTime())
                .then(response => response.json())
                .then(data => {
                    if (data.length === 0) {
                        resultsContainer.innerHTML = `
                            <div class="card" style="text-align: center; margin-top: 15px;">
                                <p style="color: #ff5252; font-weight: bold;">No se encontraron activos en el rango de $5 a $30 en este momento.</p>
                            </div>
                        `;
                        return;
                    }

                    resultsContainer.innerHTML = '';

                    // Pintamos las tarjetas respetando tus variables acordadas
                    data.forEach(accion => {
                        resultsContainer.innerHTML += `
                            <div class="card ticker-card" onclick="seleccionarActivo('${accion.ticker}')">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <h3 style="color: #ffffff; font-size: 1.3rem; font-weight: bold;">${accion.ticker} ⚡</h3>
                                    <span style="background-color: rgba(0, 230, 118, 0.1); color: #00e676; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;">Recom: ${accion.recomendacion || 'N/A'} 🏢</span>
                                </div>
                                <p style="font-size: 1.1rem; font-weight: bold; color: #00e676; margin-bottom: 12px;">Precio Actual: $${accion.precio_actual || accion.precio}</p>
                                <p style="font-size: 0.9rem; color: #90a4ae; margin-bottom: 10px;">Target Price: <strong style="color: #00e676;">$${accion.target_price || 'N/A'}</strong></p>
                                
                                <div style="background-color: #0d0f12; padding: 12px; border-radius: 8px; display: flex; justify-content: space-between; font-size: 0.85rem; border: 1px solid #1f242d;">
                                    <div><span style="color: #90a4ae;">Rango Entrada:</span> <strong style="color: #fff;">${accion.rango_entrada || 'N/A'}</strong></div>
                                    <div><span style="color: #90a4ae;">Rango Salida:</span> <strong style="color: #ff5252;">${accion.rango_salida || 'N/A'}</strong></div>
                                </div>
                                <p style="font-size:0.75rem; color:#00e676; text-align:right; margin-top:8px;">Toca para analizar 📊</p>
                            </div>
                        `;
                    });
                })
                .catch(error => {
                    resultsContainer.innerHTML = `
                        <div class="card" style="text-align: center; margin-top: 15px;">
                            <p style="color: #ff5252; font-weight: bold;">Error al conectar con la base de datos.</p>
                        </div>
                    `;
                });
        }

        function seleccionarActivo(ticker) {
            tickerSeleccionado = ticker;
            const navAnalisis = document.querySelectorAll('.nav-item')[2];
            switchPage('noticias', navAnalisis);
        }

        function cargarAnalisisGrafico(ticker) {
            document.getElementById('ticker-analisis-header').innerText = `Activo Seleccionado: ${ticker}`;

            // Inyectar gráfica limpia interactiva
            document.getElementById('tv-chart-wrapper').innerHTML = `<div id="tv-chart-container" style="height:100%;"></div>`;
            new TradingView.widget({
                "autosize": true,
                "symbol": ticker, // Quitamos el candado "NASDAQ:" para que busque en NYSE o donde pertenezca solo con el ticker
                "interval": "D",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "es",
                "toolbar_bg": "#14171c",
                "enable_publishing": false,
                "hide_side_toolbar": true,
                "allow_symbol_change": false,
                "container_id": "tv-chart-container"
            });

            // Inyectar Perfil Técnico Técnico Estilo Google Finance
            document.getElementById('tv-technical-wrapper').innerHTML = `
                <div class="tradingview-widget-container">
                    <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?locale=es&symbol=${ticker}&interval=1D&width=100%25&height=180&theme=dark" style="width: 100%; height: 180px; border: none; overflow: hidden;"></iframe>
                </div>
            `;

            // Inyectar flujo de Noticias y Earnings
            document.getElementById('tv-news-wrapper').innerHTML = `
                <div class="tradingview-widget-container">
                    <iframe src="https://s.tradingview.com/embed-widget/timeline/?locale=es&symbol=${ticker}&width=100%25&height=300&theme=dark" style="width: 100%; height: 300px; border: none; overflow: hidden;"></iframe>
                </div>
            `;
        }
    </script>

</body>
</html>
