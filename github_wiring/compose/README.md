# Local Orchestration with Docker Compose

## Up
```bash
cd compose
cp .env.example .env
docker compose up -d
```

- n8n → http://localhost:5678
- Agents → planner 8101… producer 8102… design 8103… social 8104… analytics 8105… cert 8106

## Configure n8n
- Open n8n… import the JSON workflows from `Automation_Pack/n8n_flows`.
- Edit HTTP Request nodes to call local agents… for example:
  - Planner → http://planner:8080/plan
  - Producer → http://producer:8080/bundle
  - Design → http://design:8080/render
  - Social → http://social:8080/schedule
  - Analytics → http://analytics:8080/rollup
  - Cert → http://cert:8080/mint
