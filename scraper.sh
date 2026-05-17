#!/usr/bin/env bash
set -euo pipefail

echo "[*] Escaneando publicaciones oficiales del BOE..."

FECHA_HOY=$(date +%Y%m%d)
FEED_URL="https://boe.es{FECHA_HOY}"
RAW_XML=$(curl -s -L --connect-timeout 5 "${FEED_URL}" || echo "")

WORKER_URL="https://workers.dev"

if [ -z "${RAW_XML}" ] || echo "${RAW_XML}" | grep -q "Error"; then
    echo "[!] El BOE no ha publicado hoy o el servicio no esta disponible."
    echo "[*] Inyectando pulso preventivo de rutina en D1 remota..."
    
    curl -s -L -X POST "${WORKER_URL}" \
      -H "Content-Type: application/json" \
      -d '{"type":"world_state","key":"news_feed","value":"{\"titular\":\"SISTEMA EN ESPERA: FIN DE SEMANA\",\"impacto\":\"El nucleo perimetral mantiene el control preventivo sin alertas oficiales de ley.\"}"}'
else
    # Filtrar leyes del día
    TITULO=$(echo "${RAW_XML}" | grep -oP '(?<=<titulo>).*?(?=</titulo>)' | grep -E -i "vivienda|decreto|medidas|urgentes|fiscal|presupuesto" | head -n 1 || echo "")
    if [ -z "${TITULO}" ]; then
        echo "[*] No se detectan reformas criticas hoy. Pulsando rutina..."
        curl -s -L -X POST "${WORKER_URL}" \
          -H "Content-Type: application/json" \
          -d '{"type":"world_state","key":"news_feed","value":"{\"titular\":\"MONITOREO DE RUTINA: SIN ALERTAS\",\"impacto\":\"No se han detectado publicaciones de riesgo presupuestario en el BOE.\"}"}'
    else
        echo "[+] Publicacion detectada: ${TITULO}"
        python3 /home/weemb/cortex/core/event_engine.py "recortar_sanidad"
    fi
fi
