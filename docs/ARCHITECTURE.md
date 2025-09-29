# System Architecture

## Topology
- **Orchestration Service (MCP-aware)** — routes intents to policy agents; enforces gates.
- **Agent Services** — each policy agent runs as a microservice (stateless) with external memory.
- **Memory Layer** — five-pillar stores with retrieval & summarization adapters.
- **Pipelines** — ETL for FRED, Treasury, SEC, CBO, Census; normalized datasets.
- **Compliance Layer** — FEC/legal/QA gates, audit logging, redaction, approvals.
- **n8n** — operator-facing workflows (main campaign, petition flow, error handling).

## MCP (Model Context Protocol)
- Manifests describe tools, prompts, memory bindings per agent.
- JSON-RPC over localhost or gateway; streaming responses enabled.
- Context caches: hot/warm/cold tiers; policy-bound retrieval.

## Failure Handling
- Circuit breakers; exponential backoff; idempotent operations.
- State checkpoints per stage; resumable jobs; audit trails.

## Security & Privacy
- Least privilege, role-based tokens, encryption in transit/at rest.
- PII minimization; access logging; consent & disclosure controls.

## CI/CD
- Lint + schema validation.
- Orchestrator dry-run with sample task.
- Optional container build matrix (disabled by default).
