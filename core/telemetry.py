#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime
F = Path.home() / "cortex" / "data" / "state.json"
def read_state():
    if F.exists():
        try:
            with open(F, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"simulation": {"h_index": 1.25, "ipc": 3.4, "corruption_index": 75}, "infrastructure": {"node_muscle_status": "OFFLINE", "gpu_load": 0.0, "ue_fps": 0.0, "terrarium_temp": 29.0, "terrarium_hum": 45.0}, "system": {"timestamp": ""}, "radar": []}
def write_state(s):
    try:
        F.parent.mkdir(parents=True, exist_ok=True)
        with open(F, "w", encoding="utf-8") as f: json.dump(s, f, indent=2, ensure_ascii=False)
        return True
    except: return False
