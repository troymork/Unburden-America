# Solvency Automation

Hands-free campaign automation … n8n orchestrates planner … producer … design … social … analytics … cert agents.

## What’s inside
- **notion** … CSVs plus schemas for one-click import
- **prompts** … agent prompts for planner … producer … design … social … analytics … cert
- **n8n_flows** … 16 JSON workflows
- **next_content_schema** … explainer … one-pager … infographics hub … social kit
- **ffmpeg_templates** … command templates for automated video
- **certificate** … seal SVG … template SVG … generator script
- **github_wiring** … solvency-agents FastAPI … compose stack … GHCR workflow
- **cloud_run** … YAMLs and scripts for GCP Cloud Run (optional)

## Local quick start
```bash
cd github_wiring/compose
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build
open http://localhost:5678
