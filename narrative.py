#!/usr/bin/env python3
import json
import http.client
from pathlib import Path

STATE_JSON = Path("/home/weemb/cortex/world_state.json")

def consultar_ollama(prompt):
    try:
        conn = http.client.HTTPConnection("localhost", 11434)
        payload = json.dumps({
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "system": "Eres el locutor de noticias de la matriz geopolítica Cortex OS. Redacta titulares fríos, concisos y de alta densidad periodística al estilo ciberpunk."
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/api/generate", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))["response"].strip()
    except Exception:
        return "ALERTA SINTÉTICA: Variación paramétrica detectada en el algoritmo nacional."

if STATE_JSON.exists():
    with open(STATE_JSON, "r", encoding="utf-8") as f:
        st = json.load(f)
    
    # Extraer variables contextuales para alimentar el prompt de la IA
    regimen = st["simulation"]["regimen_actual"]
    deuda = st["simulation"]["deuda_publica_pct"]
    licitacion = st["yield"]["subvenciones"]["ultima_licitacion"]
    
    prompt_noticia = f"Genera una única noticia urgente basada en este estado real: Régimen: {regimen}. Deuda: {deuda}%. Última licitación detectada en el BOE: {licitacion}. Máximo 20 palabras."
    
    nueva_noticia = consultar_ollama(prompt_noticia)
    
    # Inyectar la noticia generada en el feed histórico de simulación
    st["simulation"]["chat_log"].append({"sender": "Cortex-News", "message": nueva_noticia})
    
    # Mantener solo los últimos 10 eventos en memoria para evitar saturación del JSON
    st["simulation"]["chat_log"] = st["simulation"]["chat_log"][-10:]
    
    with open(STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)
    print(f"[NARRATIVE] Nueva crónica inyectada: {nueva_noticia}")
