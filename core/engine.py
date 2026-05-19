# -*- coding: utf-8 -*-
import json
import os
import time
import sys

# Detectar puertos serie estándar de Arduino/ESP32 en Linux Pop!_OS
PUERTOS_A_PROBAR = ['/dev/ttyACM0', '/dev/ttyUSB0', '/dev/ttyACM1']
BRIDGE_FILE = "/home/weemb/cortex/var/world/params.json"

def buscar_puerto_activo():
    import serial.tools.list_ports
    ports = [p.device for p in serial.tools.list_ports.comports()]
    for p in PUERTOS_A_PROBAR:
        if p in ports or os.path.exists(p):
            return p
    return None

def actualizar_telemetria_terrario(temperatura, humedad):
    if not os.path.exists(BRIDGE_FILE):
        return
    try:
        with open(BRIDGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Mapear e inyectar las métricas de hardware dentro de la estructura canónica
        data["life_os"]["terrario_sefa"]["status"] = "ACTIVO"
        data["life_os"]["terrario_sefa"]["temperatura_sonda_c"] = temperatura
        data["life_os"]["terrario_sefa"]["humedad_sonda_pct"] = humedad
        data["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
        with open(BRIDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[HARDWARE] Telemetría inyectada con éxito: {temperatura}°C | {humedad}%")
    except Exception as error:
        print(f"[ERROR_BRIDGE] Fallo al escribir en params.json: {error}")

def main():
    print("[HARDWARE] Inicializando escaneo del bus serie para Sonda Lampropeltis...")
    puerto = buscar_puerto_activo()
    
    if not puerto:
        print("[ADVERTENCIA] No se detecta microcontrolador físico en /dev/ttyACM* o /dev/ttyUSB*.")
        print("[MODO_SIMULACIÓN] Inyectando telemetría de ruido ambiental simulada...")
        while True:
            # Caída simulatoria sutil de la temperatura nocturna en Tàrrega
            temp_sim = round(24.5 + (time.time() % 10 * 0.05), 1)
            hum_sim = round(55.0 + (time.time() % 5 * 0.2), 1)
            actualizar_telemetria_terrario(temp_sim, hum_sim)
            time.sleep(4)
            
    try:
        import serial
        ser = serial.Serial(puerto, 9600, timeout=1)
        print(f"[CONEXIÓN] Túnel serie abierto correctamente en {puerto}")
        time.sleep(2) # Esperar inicialización del hardware
        
        while True:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            if linea:
                # El firmware estándar del Arduino debe imprimir: "TEMP,HUM" (ej: "26.4,52")
                parts = linea.split(',')
                if len(parts) == 2:
                    try:
                        t = float(parts[0])
                        h = float(parts[1])
                        actualizar_telemetria_terrario(t, h)
                    except ValueError:
                        pass
            time.sleep(4)
    except Exception as e:
        print(f"[CRÍTICO] Fallo en la comunicación por puerto serie: {e}")

if __name__ == "__main__":
    main()
