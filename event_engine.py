#!/usr/bin/env python3
import json, sys
from pathlib import Path

STATE_FILE = Path("/home/weemb/cortex/world_state.json")

def procesar_ciclo(voto_accion=None):
    if not STATE_FILE.exists():
        # Crear un estado por defecto si no existiera físicamente en la raíz
        default_state = {
            "simulation": {
                "deuda_publica_pct": 113.2, "unemployment_rate_pct": 11.7, "approval_rating_pct": 42.0,
                "ipc_interanual_pct": 3.4, "corruption_index_pct": 75.0, "riesgo_golpe_estado_pct": 0.0,
                "regimen_actual": "Democracia Parlamentaria en Obras",
                "chat_log": [{"sender": "Sistema", "message": "Centro Nervioso Operacional Activo."}]
            },
            "infrastructure": { "node_muscle_status": "OFFLINE", "gpu_load_pct": 0.0, "ue_fps": 0.0, "terrarium_temperature_celsius": 28.5 },
            "bienes_raices": { "operador_local": { "identidad": "Anna Armengol Hallado", "municipio": "Tàrrega", "empadronamiento": "Ciutadilla", "cobertura_solicitada": "RGC (801.85 EUR)" } },
            "yield": { "marketplace_tattoos": { "assets_count": 14, "wallet_xmr": "44AFFq5kSiGb...", "precio_base_xmr": 0.04 } }
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f: json.dump(default_state, f, indent=2)
        return

    with open(STATE_FILE, "r", encoding="utf-8") as f: st = json.load(f)

    # Procesamiento determinista de las mecánicas macro
    if voto_accion == "subir_iva":
        st["simulation"]["deuda_publica_pct"] = max(0.0, st["simulation"]["deuda_publica_pct"] - 10.0)
    elif voto_accion == "recortar_sanidad":
        st["simulation"]["riesgo_golpe_estado_pct"] = min(100.0, st["simulation"]["riesgo_golpe_estado_pct"] + 20.0)
    elif voto_accion == "ejecutar_golpe":
        st["simulation"]["riesgo_golpe_estado_pct"] = min(100.0, st["simulation"]["riesgo_golpe_estado_pct"] + 35.0)

    if st["simulation"]["riesgo_golpe_estado_pct"] >= 100.0:
        st["simulation"]["regimen_actual"] = "Junta Militar de Emergencia 'Pais en Obras'"
        st["simulation"]["riesgo_golpe_estado_pct"] = 0.0
    else:
        st["simulation"]["deuda_publica_pct"] = round(st["simulation"]["deuda_publica_pct"] + 0.01, 2)

    with open(STATE_FILE, "w", encoding="utf-8") as f: json.dump(st, f, indent=2)

if __name__ == "__main__":
    accion = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "" else None
    procesar_ciclo(accion)
