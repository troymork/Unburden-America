#!/usr/bin/env bash
set -euo pipefail
python3 mcp/server/mcp_server.py &
echo "[dev] MCP server started on 7801 (background)."
