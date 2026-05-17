#!/usr/bin/env python3
import json, os, time, socket
BASE = "/home/weemb/cortex"
STATE_JSON = os.path.join(BASE, "world_state.json")
OUTPUT_FILE = os.path.join(BASE, "web/index.html")
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception: return "127.0.0.1"
while True:
    if os.path.exists(STATE_JSON):
        try:
            with open(STATE_JSON, "r", encoding="utf-8") as f: st = json.load(f)
            sim = st.get("simulation", {})
            infra = st.get("infrastructure", {})
            yd = st.get("yield", {})
            bienes = st.get("bienes_raices", {})
            op = bienes.get("operador_local", {})
            chat_log = sim.get("chat_log", [])
            debt = sim.get("deuda_publica_pct", 119.9)
            regimen = sim.get("regimen_actual", "Democracia Parlamentaria en Obras")
            golpe = sim.get("riesgo_golpe_estado_pct", 0.0)
            assets = yd.get("marketplace_tattoos", {}).get("assets_count", 14)
            xmr_p = yd.get("marketplace_tattoos", {}).get("precio_base_xmr", 0.04)
            xmr_w = "4FDD206CB403CA076447E0AC2E73DB53C1DA4D973534DEBF2A687B94EF7C24B504BA4ACB07BEEF3E0CE10D2F8A0CCCA"
            btc_w = "bc1qeaf1b3cc0826d05dc9250db65d25f0ad49f25f0ad4"
            feed_html = "".join([f"<li><b>[{n.get('sender')}]</b>: {n.get('message')}</li>" for n in chat_log[::-1]])
            bienes_rows = "".join([f"<tr><td>{b['id']}</td><td>{b['tipo']}</td><td>{b['provincia']}</td><td>{b['viabilidad_pct']}%</td></tr>" for b in bienes.get("objetivos", [])])
            html = f"""<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Reality OS v3.0</title><style>body {{ font-family: monospace; background: #fafafa; margin: 20px; }} .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }} .card {{ background: #fff; border: 2px solid #000; padding: 15px; box-shadow: 4px 4px 0px #000; }} .stats {{ font-size: 13px; font-weight: bold; background: #e2e2e2; padding: 10px; border: 2px solid #000; display: flex; justify-content: space-between; }} .btn {{ background: #000; color: #fff; border: none; padding: 10px; width: 100%; font-family: monospace; font-weight: bold; cursor: pointer; text-transform: uppercase; margin-bottom: 8px; }} .btn.danger {{ background: #ff4d4d; color: #000; }} iframe {{ width: 100%; height: 200px; border: 2px solid #000; }} ul {{ list-style: none; padding: 5px; background: #eee; border: 1px solid #000; max-height: 120px; overflow-y: auto; }} table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }} th, td {{ border: 1px solid #000; padding: 4px; font-size:11px; }} th {{ background: #ddd; }}</style><script>async function vote(i){{await fetch('/api/v1/simulation/vote',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{vote_index:i==0?'subir_iva':i==1?'recortar_sanidad':'ejecutar_golpe'}})}});setTimeout(()=>location.reload(),400);}}</script></head><body><div class='card'><h2>PAÍS EN OBRAS · CENTRO NERVIOSO TOTAL v3.0</h2><p>Operador: Anna Armengol Hallado | IP: {get_ip()} | Padrón: {op.get('empadronamiento')} | Escudo Vital: PENDIENTE_ENTREGA</p></div><div class='stats'><span>RÉGIMEN: {regimen}</span><span>DEUDA PÚBLICA: {debt}%</span><span>RIESGO GOLPE: {golpe}%</span></div><div class='grid'><div class='card'><h3>LIFE OS & REALITY SIMULATION</h3><button class='btn' onclick='vote(0)'>Subir IVA (+Corrupción, -Deuda)</button><button class='btn' onclick='vote(1)'>Recortar Sanidad (+Riesgo Golpe)</button><button class='btn danger' onclick='vote(2)'>FORZAR ACCIÓN: EJECUTAR GOLPE DE ESTADO</button><h4>WORLD FEED / LOG NARRATIVO</h4><ul>{feed_html}</ul></div><div class='card'><h3>TRANSMISIÓN EN TIEMPO REAL & ASSETS</h3><iframe src='https://youtube.com' allowfullscreen></iframe><p style='margin-top:8px;font-size:10px;word-break:break-all;'><b>XMR Wallet:</b> {xmr_w}<br><b>BTC Wallet:</b> {btc_w}<br>Tattoos: {assets} items | Base: {xmr_p} XMR</p><table><thead><tr><th>ID</th><th>Inmueble</th><th>Provincia</th><th>Viabilidad</th></tr></thead><tbody>{bienes_rows}</tbody></table></div></div></body></html>"""
            with open(OUTPUT_FILE, "w", encoding="utf-8") as out: out.write(html)
        except Exception: pass
    time.sleep(5)