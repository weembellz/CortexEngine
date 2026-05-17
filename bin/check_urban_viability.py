#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE = Path.home() / "cortex"
STATE_PATH = BASE / "data/state.json"

def verificar_agua_cercana(lat, lon, radio_metros=500):
    """Consulta Overpass API para detectar masas de agua cercanas a las coordenadas."""
    print(f"[*] Analizando entorno hidrográfico en radio de {radio_metros}m para las coordenadas: {lat}, {lon}")
    
    # Query Overpass estructurada para buscar rios, canales o costas cercanos
    overpass_query = f"""
    [out:json][timeout:15];
    (
      node["waterway"](around:{radio_metros},{lat},{lon});
      way["waterway"](around:{radio_metros},{lat},{lon});
      relation["waterway"](around:{radio_metros},{lat},{lon});
      node["natural"="water"](around:{radio_metros},{lat},{lon});
      way["natural"="water"](around:{radio_metros},{lat},{lon});
    );
    out body geom;
    """
    
    url = "https://overpass-api.de"
    data = urllib.parse.urlencode({'data': overpass_query}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'CortexEngine/2.0'})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            resultado = json.loads(response.read().decode('utf-8'))
            elementos = resultado.get('elements', [])
            return len(elementos) > 0, elementos
    except Exception as e:
        print(f"[!] Error de conexión con Overpass API: {e}")
        return False, []

def ejecutar_auditoria():
    if not STATE_PATH.exists():
        print("[!] Archivo state.json no encontrado.")
        return

    with open(STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)

    objetivos = state.get("bienes_raices", {}).get("objetivos", [])
    cambios = False

    for obj in objetivos:
        if "coords" in obj:
            lat, lon = map(float, obj["coords"].split(","))
            tiene_agua, elementos = verificar_agua_cercana(lat, lon)
            
            # Clasificación de viabilidad técnica basada en la presencia de agua
            obj["recurso_hidrico_detectado"] = tiene_agua
            if tiene_agua:
                obj["viabilidad"] = min(100.0, obj.get("viabilidad", 70.0) + 15.0)
                print(f"[+] Éxito: Masa de agua detectada cerca de {obj['id']} ({obj['tipo']}). Viabilidad aumentada.")
            else:
                print(f"[-] Alerta: No se detectó agua superficial inmediata para {obj['id']}.")
            cambios = True

    if cambios:
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        print("[+] Base de datos state.json actualizada con los criterios hidrográficos reales.")

if __name__ == "__main__":
    ejecutar_auditoria()
