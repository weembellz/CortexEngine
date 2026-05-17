#!/usr/bin/env python3
import sys, json, os
from datetime import datetime, timezone

BRIDGE = "/home/weemb/cortex/var/world/params.json"

def load():
    with open(BRIDGE, "r") as f:
        return json.load(f)

def save(data):
    data["timestamp"] = datetime.now(timezone.utc).isoformat()
    with open(BRIDGE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

REGLAS = {
    "subir_iva": {
        "fn": lambda d: (
            d["economy"].__setitem__("deuda_publica_pct",
                max(0.0, round(d["economy"]["deuda_publica_pct"] - 1.5, 2))),
            d["world"].__setitem__("h_index",
                min(10.0, round(d["world"]["h_index"] + 0.2, 2))),
            d.__setitem__("news_feed", {
                "titular": "AUSTERIDAD FISCAL ACTIVADA",
                "impacto": "H-Index sube. Extracción optimizada."
            })
        )
    },
    "recortar_sanidad": {
        "fn": lambda d: (
            d["world"].__setitem__("chaos",
                min(1.0, round(d["world"]["chaos"] + 0.15, 2))),
            d["world"].__setitem__("fog_density",
                min(1.0, round(d["world"]["fog_density"] + 0.1, 2))),
            d.__setitem__("news_feed", {
                "titular": "AJUSTE PRESUPUESTARIO CRÍTICO",
                "impacto": "Caos sube. Niebla densificada en UE5."
            })
        )
    },
    "ejecutar_golpe": {
        "fn": lambda d: (
            d["economy"].__setitem__("regimen_actual", "COLAPSO_SISTEMICO"),
            d["economy"].__setitem__("active_crises",
                d["economy"]["active_crises"] + 1),
            d["world"].__setitem__("chaos", 1.0),
            d.__setitem__("news_feed", {
                "titular": "GOLPE DE ESTADO EJECUTADO",
                "impacto": "Protocolo de control de daños total activo."
            })
        )
    }
}

def procesar(accion):
    if not os.path.exists(BRIDGE):
        print(f"ERROR: bridge no encontrado en {BRIDGE}", file=sys.stderr)
        return
    data = load()
    regla = REGLAS.get(accion)
    if regla:
        regla["fn"](data)
        save(data)
        print(f"OK: {accion}")
    else:
        print(f"WARN: accion desconocida '{accion}'")

if __name__ == "__main__":
    accion = sys.argv[1] if len(sys.argv) > 1 else "rutina"
    procesar(accion)
