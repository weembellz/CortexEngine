#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import os
import base64
from datetime import datetime

MEDIA_DIR = os.path.expanduser("~/cortex/media/tattoos")
STATE_PATH = os.path.expanduser("~/cortex/data/state.json")
SD_URL = "http://127.0.0"

def forge_art():
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)

    # Prompt técnico optimizado para estética Cyberpunk/Blackwork libre de artefactos
    payload = {
        "prompt": "cyberpunk tattoo design, gothic geometry, linework, neo-traditional, blackwork, sharp details, pure white background",
        "negative_prompt": "shading, realistic, human, skin, background noise, blurry, color, gradient",
        "steps": 20,
        "cfg_scale": 7,
        "width": 512,
        "height": 512
    }

    try:
        req = urllib.request.Request(
            SD_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            res = json.loads(response.read().decode("utf-8"))
            
        image_base64 = res["images"][0]
        filename = f"tattoo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(MEDIA_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(base64.b64decode(image_base64))

        # Actualizar el contador de activos disponibles en la fuente de verdad
        if os.path.exists(STATE_PATH):
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)
            
            state["yield"]["marketplace_tattoos"]["assets"] = state["yield"]["marketplace_tattoos"].get("assets", 0) + 1
            
            with open(STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
                
        print(f"Forge Engine: Activo generado y exportado a media/tattoos/{filename}")

    except urllib.error.URLError:
        print("Forge Engine Offline: Asegúrate de que Stable Diffusion esté corriendo en el puerto 7860 con el flag --api.")
    except Exception as e:
        print(f"Error en la factoría de activos: {e}")

if __name__ == "__main__":
    forge_art()
