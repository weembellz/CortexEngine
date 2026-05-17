#!/bin/bash
STATE="$HOME/cortex/data/state.json"
FPS=$(jq -r '.infrastructure.ue_fps // 0' "$STATE")
TEMP=$(jq -r '.infrastructure.terrarium_temperature_celsius // 0' "$STATE")
if (( $(echo "$FPS < 30" | bc -l) )); then
    echo "$(date) - ALERTA: FPS bajos ($FPS)" >> ~/cortex/var/log/server.log
fi
if (( $(echo "$TEMP > 32" | bc -l) )) || (( $(echo "$TEMP < 24" | bc -l) )); then
    echo "$(date) - ALERTA: Temperatura del terrario fuera de rango ($TEMP C)" >> ~/cortex/var/log/server.log
fi
