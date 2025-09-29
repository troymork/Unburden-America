#!/usr/bin/env bash
set -euo pipefail
echo "Lint: JSON/YAML"; python3 - <<PY
import json,glob,sys,yaml
for p in glob.glob("**/*.json", recursive=True):
  try: json.load(open(p))
  except Exception as e: print("JSON error:",p,e); sys.exit(1)
for p in glob.glob("**/*.y*ml", recursive=True):
  try: yaml.safe_load(open(p))
  except Exception as e: print("YAML error:",p,e); sys.exit(1)
print("OK")
PY
echo "Dry-run orchestrator route_intent"; curl -s -X POST http://127.0.0.1:7801/rpc -d '{"method":"route_intent","params":{"intent":"plan"},"id":"1"}' -H 'content-type: application/json' | jq .
