#!/usr/bin/env python3
import json, sys
from pathlib import Path
STATE = Path.home() / "cortex/core/world_state.json"

def procesar(accion):
    if not STATE.exists(): return
    with open(STATE) as f: st = json.load(f)
    sim = st["simulation"]
    if accion == "subir_iva":
        sim["deuda_publica_pct"] = max(0, sim.get("deuda_publica_pct", 113.2) - 10)
        sim["corruption_index_pct"] = min(100, sim.get("corruption_index_pct", 75) + 2.5)
    elif accion == "recortar_sanidad":
        sim["deuda_publica_pct"] = max(0, sim.get("deuda_publica_pct", 113.2) - 8.5)
        sim["riesgo_golpe_estado_pct"] = min(100, sim.get("riesgo_golpe_estado_pct", 0) + 20)
    elif accion == "ejecutar_golpe":
        sim["riesgo_golpe_estado_pct"] = min(100, sim.get("riesgo_golpe_estado_pct", 0) + 35)
    
    if sim.get("riesgo_golpe_estado_pct", 0) >= 100:
        sim["regimen_actual"] = "Junta Militar de Emergencia"
        sim["deuda_publica_pct"] = round(sim.get("deuda_publica_pct", 113.2) * 0.5, 2)
        sim["corruption_index_pct"] = 99.9
        sim["riesgo_golpe_estado_pct"] = 0
    else:
        sim["deuda_publica_pct"] = round(sim.get("deuda_publica_pct", 113.2) + 0.1, 2)
    with open(STATE, "w") as f: json.dump(st, f, indent=2)

if __name__ == "__main__":
    accion = sys.argv[1] if len(sys.argv) > 1 else ""
    procesar(accion)
