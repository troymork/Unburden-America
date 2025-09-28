# Cloud Run — Zero Cost Agent Deploy

This folder lets you deploy all six role-based agents to **Google Cloud Run** using the free tier. 
They scale to zero when idle… so you pay $0 until traffic arrives.

## Prereqs
1. Install the Google Cloud CLI and login:
   ```bash
   brew install --cask google-cloud-sdk   # macOS
   gcloud auth login
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   gcloud config set run/region us-central1
   ```
2. Enable APIs
   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com
   ```
3. Make sure your image exists at **ghcr.io/troymork/solvency-agent:latest** (our GitHub Action builds this automatically on push to `solvency-agents`).
   If you don't have it yet, push the repo and let the Action run.

## Quick deploy (all services)
```bash
chmod +x deploy_cloud_run.sh
./deploy_cloud_run.sh YOUR_PROJECT_ID us-central1
```

This will create services:
- `solvency-planner`
- `solvency-producer`
- `solvency-design`
- `solvency-social`
- `solvency-analytics`
- `solvency-cert`

Each uses env `ROLE` to activate its function in the same image.

## Outputs
The script prints public HTTPS URLs for each agent. 
Use those URLs in your n8n HTTP Request nodes.

## Notes
- Min instances: 0 (true scale-to-zero)
- CPU: 0.25… Memory: 256Mi (fits free tier; adjust if needed)
- Concurrency: 80 (default)… good for spikes
- Authentication: `--allow-unauthenticated` for easy testing; switch off for private use with IAM later.


## New services
- `solvency-compliance` … automated checks for disclosure… risk language… licensing
- `solvency-n8n` … optional Cloud Run instance of n8n for hands free orchestration
  - Note: Cloud Run scales to zero… state is ephemeral unless using external DB… this is fine for demos
  - For persistence… later connect a managed Postgres instance when budget allows
