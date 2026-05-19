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
            d["economy"].__setitem__("deuda_publica_pct", max(0.0, round(d["economy"]["deuda_publica_pct"] - 1.5, 2))),
            d["world"].__setitem__("h_index", min(10.0, round(d["world"]["h_index"] + 0.2, 2))),
            d.__setitem__("news_feed", {"titular": "AUSTERIDAD FISCAL ACTIVADA", "impacto": "H-Index sube"})
        ),
    },
    "recortar_sanidad": {
        "fn": lambda d: (
            d["world"].__setitem__("chaos", min(1.0, round(d["world"]["chaos"] + 0.15, 2))),
            d.__setitem__("news_feed", {"titular": "AJUSTE PRESUPUESTARIO", "impacto": "Caos social +0.15"})
        ),
    },
    "ejecutar_golpe": {
        "fn": lambda d: (
            d["economy"].__setitem__("regimen_actual", "COLAPSO_SISTEMICO"),
            d["world"].__setitem__("chaos", 1.0),
            d.__setitem__("news_feed", {"titular": "GOLPE DE ESTADO", "impacto": "Sistema en colapso"})
        ),
    },
}

def procesar(accion):
    if not os.path.exists(BRIDGE):
        print(f"ERROR: bridge no encontrado en {BRIDGE}", file=sys.stderr)
        return
    data = load()
    if accion in REGLAS:
        REGLAS[accion]["fn"](data)
        save(data)
        print(f"OK: {accion} aplicado")
    else:
        print(f"WARN: accion desconocida '{accion}'")

if __name__ == "__main__":
    accion = sys.argv[1] if len(sys.argv) > 1 else "rutina"
    procesar(accion)
