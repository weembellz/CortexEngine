#!/usr/bin/env bash
set -euo pipefail
STATE_FILE="$HOME/cortex/world_state.json"
OUTPUT_DIR="$HOME/cortex/data/docs"
TXT_RGC="$OUTPUT_DIR/declaracion_rgc.txt"
TXT_IMV="$OUTPUT_DIR/declaracion_imv.txt"
if [ ! -f "$STATE_FILE" ]; then exit 1; fi
NOMBRE=$(jq -r '.user_profile.nombre_completo' "$STATE_FILE")
DNI=$(jq -r '.user_profile.documento_identidad' "$STATE_FILE")
DOMICILIO=$(jq -r '.user_profile.direccion' "$STATE_FILE")
MUNICIPIO=$(jq -r '.user_profile.municipio' "$STATE_FILE")
FECHA=$(jq -r '.user_profile.fecha_declaracion' "$STATE_FILE")
cat << EOF > "$TXT_RGC"
DECLARACIÓ JURADA DE INGRESSOS I PATRIMONI (RGC)
Nom i cognoms: $NOMBRE
DNI: $DNI
Domicili habitual: $DOMICILIO
Municipi de gestió: $MUNICIPIO
DECLAR SOTA JURAMENT: Que en la data actual el meu nivell d'ingressos mensuals és zero (0,00 eur), mancant de recursos econòmics mínims per a la cobertura de les meves necessitats bàsiques de subsistència.
Signat: $NOMBRE
EOF
cat << EOF > "$TXT_IMV"
DECLARACION JURADA DE SITUACION ECONOMICA (IMV)
Nombre y Apellidos: $NOMBRE
DNI: $DNI
Domicilio: $DOMICILIO
Municipio: $MUNICIPIO
DECLARO BAJO JURAMENTO: Que en el año en curso carezco de rentas salariales o profesionales, situándose mis ingresos actuales en cero euros (0,00 eur) mensuales.
Firmado: $NOMBRE
EOF
libreoffice --headless --convert-to pdf --outdir "$OUTPUT_DIR" "$TXT_RGC" > /dev/null 2>&1
libreoffice --headless --convert-to pdf --outdir "$OUTPUT_DIR" "$TXT_IMV" > /dev/null 2>&1
echo "=== COMPILACION LEGAL COMPLETADA ==="