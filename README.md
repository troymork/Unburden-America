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
