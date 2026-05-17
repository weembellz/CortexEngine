#!/usr/bin/env bash
set -euo pipefail

STATE="$HOME/cortex/data/state.json"
TODAY=$(date +%Y%m%d)
URL="https://boe.es{TODAY}"

# Captura analítica delegando la resolución DNS al kernel mediante curl
LIC=$(curl -s -L -A "Mozilla/5.0 (X11; Linux x86_64)" "$URL" | grep -oP '<titulo>.*?</titulo>' | head -n 20 | grep -iE '(subvencion|ayuda|licitacion)' | sed -e 's/<[^>]*>//g' | head -n 1 || true)

if [ -z "$LIC" ]; then
    LIC="Sin licitaciones de riesgo detectadas hoy."
fi

# Inyección atómica mediante jq sin abrir descriptores de archivo propensos a corrupción
jq --arg lic "$LIC" '.yield.subvenciones.ultima_licitacion = $lic | .yield.subvenciones.estado = "APLICABLE"' "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"

# Regenerar la interfaz cartográfica estática para reflejar los cambios de inmediato
python3 "$HOME/cortex/bin/generator_asset_forge.py"
