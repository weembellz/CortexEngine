#!/usr/bin/env bash
set -euo pipefail

STATE_JSON="/home/weemb/cortex/world_state.json"
LOG_FILE="/home/weemb/cortex/logs/scraper.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando escaneo del BOE..." >> "$LOG_FILE"

# Simulación de extracción atómica mediante API o curl crudo filtrado con jq
# En producción, aquí meterás tu token o endpoint específico de filtrado
ULTIMA_LICITACION="Ayuda estatal digitalización infraestructuras BOE - $(date +%d/%m/%m)"
PARTIDA_EUROS=12500.0

if [ -f "$STATE_JSON" ]; then
    # Actualizar world_state.json de forma segura usando un archivo temporal
    jq --arg lic "$ULTIMA_LICITACION" --argjsoneur "$PARTIDA_EUROS" \
    '.yield.subvenciones.ultima_licitacion = $lic | .yield.subvenciones.partida_euros = $eur | .yield.subvenciones.estado = "APLICABLE"' \
    "$STATE_JSON" > "${STATE_JSON}.tmp" && mv "${STATE_JSON}.tmp" "$STATE_JSON"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Scraper completado. world_state.json actualizado." >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: No se encontró world_state.json" >> "$LOG_FILE"
fi
