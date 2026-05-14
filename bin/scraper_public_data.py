#!/usr/bin/env python3
import os
import json
import logging
import requests
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "data" / "state.json"
LOG_FILE = BASE_DIR / "var" / "log" / "cortex.log"

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])

def update_simulation_metrics():
    logging.info("Iniciando ciclo de ingesta analitica de datos publicos...")
    
    # Valores base por defecto si fallan las conexiones HTTP externas
    boe_alerts = 0
    inflation_rate = 3.4
    demand_ree = 24000.0
    
    try:
        # Ingesta automatizada BOE
        boe_res = requests.get("https://boe.es" + datetime.now().strftime("%Y%m%d"), timeout=5)
        if boe_res.status_code == 200:
            boe_alerts = boe_res.text.count("<item>")
            logging.info(f"BOE consultado con exito. Entradas detectadas: {boe_alerts}")
    except Exception as e:
        logging.warning(f"Aviso: Inalcanzable endpoint del BOE: {e}")

    try:
        # Ingesta automatizada REE (Demanda energetica de la red espanola)
        headers = {"Accept": "application/json; application/vnd.esios-api-v1+json", "x-api-token": "null"}
        ree_res = requests.get("https://ree.es", headers=headers, timeout=5)
        if ree_res.status_code == 200:
            demand_ree = ree_res.json().get("indicator", {}).get("values", [{}])[0].get("value", 24000.0)
            logging.info(f"REE consultada con exito. Demanda actual: {demand_ree} MW")
    except Exception as e:
        logging.warning(f"Aviso: Inalcanzable api de Red Electrica de Espana: {e}")

    # Calculo matematico determinista del H-INDEX basado en los datos publicos recolectados
    calculated_h_index = max(1.0, min(10.0, (boe_alerts * 0.15) + (demand_ree / 6000.0)))
    
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
        
        state["simulation"]["h_index"] = round(calculated_h_index, 2)
        state["simulation"]["inflation_rate"] = inflation_rate
        state["simulation"]["active_alerts"] = boe_alerts
        state["system"]["timestamp"] = datetime.now().isoformat()
        
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
            
        logging.info(f"Persistencia actualizada con exito. Nuevo H-INDEX: {state['simulation']['h_index']}")
        
        # Sincronizacion directa hacia el WebSocket local enviando el payload modificado
        try:
            requests.post("http://127.0.0", json={
                "h_index": state["simulation"]["h_index"],
                "inflation_rate": state["simulation"]["inflation_rate"]
            }, timeout=3)
        except Exception as e:
            logging.warning(f"Aviso: No se pudo retransmitir la alerta al socket local: {e}")

if __name__ == "__main__":
    update_simulation_metrics()
