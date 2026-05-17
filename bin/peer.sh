#!/usr/bin/env bash
set -euo pipefail
MY_IP=$(ip -4 addr show | grep -oP "(?<=inet\s)\d+(\.\d+){3}" | grep -v 127.0.0.1 | head -1 || echo "127.0.0.1")
OUTPUT_FILE="/home/weemb/cortex/web/index.html"
STATE_JSON="/home/weemb/cortex/core/world_state.json"

while true; do
    python3 /home/weemb/cortex/core/engine.py ""
    DEUDA=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['simulation']['deuda_publica_pct'])")
    REGIMEN=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['simulation']['regimen_actual'])")
    GOLPE=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['simulation']['riesgo_golpe_estado_pct'])")
    OP_MUN=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['bienes_raices']['operador_local']['municipio'])")
    OP_EMP=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['bienes_raices']['operador_local']['empadronamiento'])")
    OP_COB=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['bienes_raices']['operador_local']['cobertura_solicitada'])")
    ASSETS=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['yield']['marketplace_tattoos']['assets_count'])")
    XMR_W=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['yield']['marketplace_tattoos']['wallet_xmr'])")
    XMR_P=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['yield']['marketplace_tattoos']['precio_base_xmr'])")

    cat << HTML_GEN > "$OUTPUT_FILE"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>CORTEX OS v3.0 - Reality Interface</title>
    <style>
        body { font-family: monospace; background: #fafafa; color: #000; margin: 20px; line-height: 1.4; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .card { background: #fff; border: 3px solid #000; padding: 20px; box-shadow: 6px 6px 0px #000; }
        .header { border-bottom: 3px double #000; padding-bottom: 10px; margin-bottom: 20px; }
        .btn { background: #000; color: #fff; border: none; padding: 12px; width: 100%; font-family: monospace; font-weight: bold; cursor: pointer; text-transform: uppercase; margin-bottom: 10px; }
        .btn:hover { background: #333; }
        .btn.danger { background: #d9534f; color: white; }
        .btn.danger:hover { background: #c9302c; }
        .btn.voice { background: #007bff; color: white; }
        .btn.voice:hover { background: #0056b3; }
        iframe { width: 100%; height: 260px; border: 2px solid #000; }
        .stats { font-size: 1.2rem; font-weight: bold; background: #eee; padding: 10px; border: 1px solid #000; }
    </style>
    <script>
        let voiceWS;
        let mediaRecorder;

        async function enviarVoto(accion) {
            await fetch('/api/v1/simulation/vote', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({voto_index: accion})
            });
            setTimeout(() => location.reload(), 800);
        }

        async function initVoiceChat() {
            const btn = document.getElementById("voiceBtn");
            btn.innerText = "Conectando Audio...";
            btn.disabled = true;

            const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
            voiceWS = new WebSocket(`${protocol}//${window.location.host}/ws/v1/voice`);
            voiceWS.binaryType = 'arraybuffer';

            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    audio: { echoCancellation: true, noiseSuppression: true }, 
                    video: false 
                });
                
                mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm; codecs=opus' });
                
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0 && voiceWS.readyState === WebSocket.OPEN) {
                        voiceWS.send(event.data);
                    }
                };

                voiceWS.onmessage = async (event) => {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    const audioBuffer = await audioContext.decodeAudioData(event.data);
                    const source = audioContext.createBufferSource();
                    source.buffer = audioBuffer;
                    source.connect(audioContext.destination);
                    source.start(0);
                };

                mediaRecorder.start(100);
                btn.innerText = "Voz CORTEX Activa (100ms Chunks)";
                btn.classList.remove("voice");
                btn.style.background = "#28a745";
                console.log("Sistema de streaming de voz inicializado.");
            } catch (err) {
                btn.innerText = "Error: Sin Acceso a Micrófono";
                btn.style.background = "#dc3545";
                console.error(err);
            }
        }
    </script>
</head>
<body>
    <div class="header">
        <h1>CORTEX OS v3.0 // INTERFAZ OPERATIVA DE LA REALIDAD</h1>
        <p>Nodo Local IP: <strong>$MY_IP</strong> | Municipio: $OP_MUN ($OP_EMP) | Estado de Cobertura: $OP_COB</p>
    </div>

    <div class="stats">
        ESTADO DEL RÉGIMEN: $REGIMEN | DEUDA PÚBLICA: $DEUDA% | RIESGO GOLPE: $GOLPE%
    </div>

    <div class="grid">
        <div class="card">
            <h2>MECÁNICAS DE CONTROL Y SIMULACIÓN</h2>
            <button class="btn voice" id="voiceBtn" onclick="initVoiceChat()">Activar Interfaz de Voz Permanente</button>
            <hr style="border: 1px solid #000; margin: 15px 0;">
            <button class="btn" onclick="enviarVoto('subir_iva')">Subir IVA (+Corrupción, -Deuda)</button>
            <button class="btn" onclick="enviarVoto('recortar_sanidad')">Recortar Sanidad (+Riesgo Golpe)</button>
            <button class="btn danger" onclick="enviarVoto('ejecutar_golpe')">FORZAR ACCIÓN: EJECUTAR GOLPE DE ESTADO</button>
        </div>

        <div class="card">
            <h2>STREAMING EN TIEMPO REAL & YIELD</h2>
            <iframe src="https://youtube.com" allowfullscreen></iframe>
            <div style="margin-top: 15px; font-size: 0.85rem;">
                <strong>Marketplace Tattoos:</strong> $ASSETS diseños listos | <strong>Precio Base:</strong> $XMR_P XMR <br>
                <strong>Donaciones / Ventas (Monero):</strong> <code style="word-break: break-all;">$XMR_W</code>
            </div>
        </div>
    </div>
</body>
</html>
HTML_GEN
    sleep 5
done
