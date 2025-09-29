[![CI](https://github.com/troymork/Unburden-America/actions/workflows/agents-ci.yml/badge.svg)](https://github.com/troymork/Unburden-America/actions/workflows/agents-ci.yml)

# Unburden America… Solvency Automation

## Quickstart … jump links

• ➜ **Notion import pack** … [/notion](notion)
• ➜ **n8n workflows** … [/n8n_flows](n8n_flows)
• ➜ **Local stack compose** … [/github_wiring/compose](github_wiring/compose)

### Zero cost local run … compose

```bash
cd github_wiring/compose
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build
open http://localhost:5678
```

## Dev Quickstart

1) Start MCP shim
```bash
scripts/bootstrap_local.sh
```
2) Verify build
```bash
scripts/verify_build.sh
```
3) Import n8n pack (optional) → `n8n_pack/`

