# GitHub Wiring — Repos and CI

Repos to create in the **troymork** org/user:

1. **solvency-automation**
   - Holds n8n flows, agent prompts, certificate templates, FFmpeg scripts, and infra-as-code.
   - CI: none required… optional JSON lint.

2. **solvency-site**
   - Next.js static-export site that reads JSON content from `/content`.
   - CI: GitHub Actions builds and deploys to GitHub Pages on `main`.

3. **solvency-agents** (optional)
   - Minimal HTTP servers for Planner… Producer… Design… Social… Analytics… Cert.
   - CI: Docker build and push to GHCR.
