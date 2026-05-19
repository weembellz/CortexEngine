import os
import sys
import time
import subprocess
import signal

BASE = "/home/weemb/cortex"
CORTEX_SCRIPTS = [os.path.join(BASE, "server.py")]
procesos = []

def signal_handler(sig, frame):
    print("\n[MANAGER] Recibida seÁnËb¢v¥al de terminaciÃ³n. Cerrando procesos hijos...")
    for p in procesos:
        if p.poll() is None:
            p.terminate()
    time.sleep(1)
    for p in procesos:
        if p.poll() is None:
            p.kill()
    print("[MANAGER] Todos los hilos locales cerrados de forma limpia.")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
def main():
    print("[SUPERVISOR] Inicializando hilos CORTEX en Linux...")
    for script in CORTEX_SCRIPTS:
        if os.path.exists(script):
            p = subprocess.Popen([sys.executable, script])
            procesos.append(p)
            print(f"[SUPERVISOR] Hilo activo -> {os.path.basename(script)}")
            time.sleep(1)
    print("\n[SISTEMA] INTERFAZDECONTROLOPERATIVAL_PORT:5005")
    while True:
        time.sleep(5)
if __name__ == '__main__':
    main()