# Testing Guide

To validate configuration files and the MCP orchestrator locally, run the bootstrap and verify scripts:

```bash
scripts/bootstrap_local.sh
scripts/verify_build.sh
```

The bootstrap script launches the MCP server on port 7801, and the verify script checks JSON/YAML syntax before issuing a dry-run `route_intent` call. A successful run prints the accepted workflow DAG response.
