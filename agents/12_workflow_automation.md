# Workflow Automation Agent

## Mission
Translate runbooks into n8n workflow calls; orchestrate FFmpeg templates; commit artifacts; coordinate retries & idempotency.

## Outputs (example)
```json
{
  "prompt_version":"1.0.0",
  "dispatch_log":[{"step":"assemble_video","status":"ok","attempts":1,"duration_ms":1200}],
  "handoff":{"next_agent":"Technical Reliability and SRE Agent","notes":"Observe & heal if degraded"}
}
```

## Reliability
- Exponential backoff with jitter; max attempts 3
- Structured errors with cause chains
