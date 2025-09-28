#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID="${1:-}"
REGION="${2:-us-central1}"

if [ -z "$PROJECT_ID" ]; then
  echo "Usage: $0 PROJECT_ID [REGION]"
  exit 1
fi

gcloud config set project "$PROJECT_ID" >/dev/null
gcloud config set run/region "$REGION" >/dev/null

for f in solvency-*.yaml; do
  echo "Applying $f …"
  gcloud run services replace "$f"
done

echo "Enable unauthenticated access (optional)…"
for role in planner producer design social analytics cert; do
  gcloud run services add-iam-policy-binding "solvency-$role" \
    --member="allUsers" --role="roles/run.invoker" || true
done

for role in planner producer design social analytics cert; do
  url=$(gcloud run services describe "solvency-$role" --format='value(status.url)')
  echo "solvency-$role → $url"
done
