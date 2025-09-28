#!/usr/bin/env bash
# Deploy six role-based agents to Cloud Run from GHCR image
set -euo pipefail

PROJECT_ID="${1:-}"
REGION="${2:-us-central1}"
IMAGE="${IMAGE:-ghcr.io/troymork/solvency-agent:latest}"

if [ -z "$PROJECT_ID" ]; then
  echo "Usage: $0 PROJECT_ID [REGION]"
  exit 1
fi

gcloud config set project "$PROJECT_ID" >/dev/null
gcloud config set run/region "$REGION" >/dev/null

roles=(planner producer design social analytics cert)

for role in "${roles[@]}"; do
  svc="solvency-$role"
  echo "Deploying $svc …"
  gcloud run deploy "$svc" \
    --image "$IMAGE" \
    --platform managed \
    --allow-unauthenticated \
    --memory 256Mi \
    --cpu 1 \
    --max-instances 2 \
    --min-instances 0 \
    --set-env-vars ROLE="$role" \
    --port 8080 \
    --ingress all \
    --quiet

  url=$(gcloud run services describe "$svc" --format='value(status.url)')
  echo "$svc → $url"
done

echo "✅ Done. Paste these URLs into your n8n workflows."


# Deploy compliance
gcloud run deploy solvency-compliance   --image ghcr.io/troymork/solvency-agent:latest   --platform managed   --allow-unauthenticated   --memory 256Mi   --cpu 1   --max-instances 2   --min-instances 0   --set-env-vars ROLE="compliance"   --port 8080   --ingress all   --quiet
echo "solvency-compliance → $(gcloud run services describe solvency-compliance --format='value(status.url)')"

# Optional n8n for hands free orchestration
gcloud run deploy solvency-n8n   --image n8nio/n8n:1.79.3   --platform managed   --allow-unauthenticated   --memory 512Mi   --cpu 1   --max-instances 1   --min-instances 0   --port 5678   --set-env-vars N8N_PORT=5678,N8N_PROTOCOL=https,N8N_ENCRYPTION_KEY=change-me-please,N8N_BASIC_AUTH_ACTIVE=true,N8N_BASIC_AUTH_USER=kyrios,N8N_BASIC_AUTH_PASSWORD=change-me-please,GENERIC_TIMEZONE=America/Los_Angeles   --ingress all   --quiet
echo "solvency-n8n → $(gcloud run services describe solvency-n8n --format='value(status.url)')"
