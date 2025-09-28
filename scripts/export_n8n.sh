#!/usr/bin/env bash
set -euo pipefail
N8N_URL="${N8N_URL:-http://localhost:5678}"
AUTH="${AUTH:-basic}"
USER="${N8N_USER:-kyrios}"
PASS="${N8N_PASS:-changeme}"
OUT="n8n_export_$(date +%Y%m%d_%H%M%S).json"

if [ "$AUTH" = "token" ]; then
  curl -sf -H "X-N8N-API-KEY: ${N8N_TOKEN:?set N8N_TOKEN}" "$N8N_URL/rest/workflows" > "$OUT"
else
  curl -sf -u "$USER:$PASS" "$N8N_URL/rest/workflows" > "$OUT"
fi
echo "✅ exported → $OUT"
