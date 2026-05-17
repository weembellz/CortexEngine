#!/usr/bin/env bash
set -euo pipefail

STATE_JSON="/home/weemb/cortex/world_state.json"

if [ -f "$STATE_JSON" ]; then
    # Extraer la temperatura usando python nativo en una línea
    TEMP=$(python3 -c "import json; print(json.load(open('$STATE_JSON'))['infrastructure']['terrarium_temperature_celsius'])")
    
    # Validar si la temperatura sale del rango seguro (ejemplo: mayor a 30°C o menor a 22°C)
    if (( $(echo "$TEMP > 30.0" | bc -l) )) || (( $(echo "$TEMP < 22.0" | bc -l) )); then
        echo "[ALERTA] Temperatura crítica en terrario de Sefa: ${TEMP}°C"
        # Envío inmediato a tu canal de ntfy (CortexSefaAlerts es un canal de ejemplo)
        curl -H "Title: Alerta Terrario Sefa" \
             -H "Priority: urgent" \
             -d "La temperatura está en ${TEMP}°C. Revisa el nodo local de inmediato." \
             ntfy.sh/CortexSefaAlerts 2>/dev/null || true
    fi
fi
