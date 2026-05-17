#!/usr/bin/env python3
import http.client
import json

OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
MODEL_NAME = "llama3.2:latest"

def generar_noticia_sistemica(tipo_evento, contexto):
    prompt = f"""
    Eres el motor narrativo de la interfaz operativa 'Pais en Obras'.
    Genera un flash de prensa distopico basado en esta alteracion macro. No uses emojis.
    
    Evento: {tipo_evento}
    Metricas: {json.dumps(contexto)}
    
    Devuelve UNICAMENTE un objeto JSON plano sin textos extras:
    {{
      "titular": "TITULAR EN MAYUSCULAS",
      "impacto": "Consecuencia en la calle (maximo 15 palabras)"
    }}
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        conn = http.client.HTTPConnection(OLLAMA_HOST, OLLAMA_PORT, timeout=30)
        conn.request("POST", "/api/generate", json.dumps(payload), {"Content-Type": "application/json"})
        resp = conn.getresponse()
        if resp.status == 200:
            raw = json.loads(resp.read().decode())
            narrativa = json.loads(raw.get("response", "{}"))
            conn.close()
            return narrativa
        conn.close()
    except Exception:
        pass
    
    return {
        "titular": f"ALERTA PERIMETRAL: SISTEMA MODIFICADO POR {tipo_evento.upper()}",
        "impacto": "Los flujos procedurales del nucleo registraron variaciones de control."
    }
