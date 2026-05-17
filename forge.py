#!/usr/bin/env python3
import json, time, os, socket
from pathlib import Path

STATE_JSON = Path("/home/weemb/cortex/world_state.json")
OUTPUT_FILE = Path("/home/weemb/cortex/web/index.html")

def obtener_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
print("[FORGE] Motor de renderizado de la interfaz operativa iniciado.")

while True:
    if Path("/home/weemb/cortex/event_engine.py").exists():
        os.system("python3 /home/weemb/cortex/event_engine.py")
    
    if STATE_JSON.exists():
        try:
            with open(STATE_JSON, "r", encoding="utf-8") as f: 
                st = json.load(f)
            
            deuda = st["simulation"]["deuda_publica_pct"]
            regimen = st["simulation"]["regimen_actual"]
            golpe = st["simulation"]["riesgo_golpe_estado_pct"]
            op_mun = st["bienes_raices"]["operador_local"]["municipio"]
            op_emp = st["bienes_raices"]["operador_local"]["empadronamiento"]
            op_cob = st["bienes_raices"]["operador_local"]["cobertura_solicitada"]
            assets = st["yield"]["marketplace_tattoos"]["assets_count"]
            xmr_w = st["yield"]["marketplace_tattoos"]["wallet_xmr"]
            xmr_p = st["yield"]["marketplace_tattoos"]["precio_base_xmr"]
            ip_local = obtener_ip()

            html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>CORTEX OS v3.0 - Centro Nervioso</title>
    <style>
        body {{ font-family: monospace; background: #fafafa; color: #000; margin: 20px; font-size: 13px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }}
        .card {{ background: #fff; border: 2px solid #000; padding: 15px; box-shadow: 4px 4px 0px #000; }}
        .stats {{ font-size: 14px; font-weight: bold; background: #e2e2e2; padding: 10px; border: 2px solid #000; }}
        .btn {{ background: #000; color: #fff; border: none; padding: 10px; width: 100%; font-family: monospace; font-weight: bold; cursor: pointer; text-transform: uppercase; margin-bottom: 8px; }}
        .btn:hover {{ background: #333; }}
        .btn.danger {{ background: #ff4d4d; color: black; }}
        .btn.voice {{ background: #4da6ff; color: black; }}
        iframe {{ width: 100%; height: 240px; border: 2px solid #000; }}
    </style>
    <script>
        async function enviarVoto(accion) {{
            await fetch('/api/v1/simulation/vote', {{
                method: 'POST',
                headers: {{Content-Type: application/json}},
                body: JSON.stringify({{voto_index: accion}})
            }});
            setTimeout(() => location.reload(), 500);
        }}
    </script>
</head>
<body>
    <div class="card" style="margin-bottom:15px;">
        <h2>PAÍS EN OBRAS · INTERFAZ OPERATIVA DE LA REALIDAD v3.0</h2>
        <p>Operador: Anna Armengol | IP: {ip_local} | Padrón: {op_emp} ({op_mun}) | Solicitud: {op_cob}</p>
    </div>
    <div class="stats">
        RÉGIMEN ACTIVO: {regimen} | DEUDA PÚBLICA: {deuda}% | RIESGO DE GOLPE: {golpe}%
    </div>
    <div class="grid">
        <div class="card">
            <h3>REALITY SIMULATION & LIFE OS</h3>
            <button class="btn voice">Voz Descentralizada Canal Activo</button>
            <button class="btn" onclick="enviarVoto('subir_iva')">Subir IVA (+Corrupción, -Deuda)</button>
            <button class="btn" onclick="enviarVoto('recortar_sanidad')">Recortar Sanidad (+Riesgo Golpe)</button>
            <button class="btn danger" onclick="enviarVoto('ejecutar_golpe')">FORZAR ACCIÓN: EJECUTAR GOLPE DE ESTADO</button>
        </div>
        <div class="card">
            <h3>WORLD FEED & NOTICIAS SINTÉTICAS</h3>
            <iframe src="https://youtube.com" allowfullscreen></iframe>
            <p style="margin-top:10px; font-size:11px; word-break:break-all;"><strong>XMR:</strong> {xmr_w} | <strong>Base:</strong> {xmr_p} XMR | <strong>Tattoos IA:</strong> {assets}</p>
        </div>
    </div>
</body>
</html>"""
            with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
                out.write(html_content)
        except Exception as e:
            print(f"[FORGE ERROR] {e}")
            
    time.sleep(5)
