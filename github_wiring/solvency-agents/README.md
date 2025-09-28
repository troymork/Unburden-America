# solvency-agents

Multiplexed FastAPI container… role controlled by `ROLE` env… endpoints vary per role.

## Local test
```bash
docker build -t solvency-agent .
docker run -e ROLE=planner -p 8080:8080 solvency-agent
curl http://localhost:8080/plan -X POST -H "content-type: application/json" -d '{}'
```

## Publish to GHCR
- Create repo **troymork/solvency-agents** and push these files.
- The included workflow builds and pushes `ghcr.io/troymork/solvency-agent:latest` on push to `main`.
- The compose file in `compose/` already references this image and spins six services with different roles.
