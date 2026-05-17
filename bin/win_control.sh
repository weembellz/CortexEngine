#!/usr/bin/env bash
set -euo pipefail
STATE="$HOME/cortex/core/world_state.json"
LOG_FILE="$HOME/cortex/var/log/server.log"
if [ ! -f "$STATE" ]; then exit 1; fi
TEMP=$(jq -r '.infrastructure.terrarium_temperature_celsius // 28.5' "$STATE")
if (( $(echo "$TEMP > 32.0" | bc -l) )); then
    MSG="CRITICAL - Exceso termico en el biotopo de Sefa: $TEMP C."
    echo "$(date -Iseconds) - $MSG" >> "$LOG_FILE"
    curl -s -H "Title: CORTEX BIOTOPO" -H "Priority: urgent" -d "$MSG" "https://ntfy.sh/cortex_alerta_anna_armengol" > /dev/null || true
elif (( $(echo "$TEMP < 24.0" | bc -l) )); then
    MSG="CRITICAL - Deficit termico en el biotopo de Sefa: $TEMP C."
    echo "$(date -Iseconds) - $MSG" >> "$LOG_FILE"
    curl -s -H "Title: CORTEX BIOTOPO" -H "Priority: high" -d "$MSG" "https://ntfy.sh/cortex_alerta_anna_armengol" > /dev/null || true
fi
