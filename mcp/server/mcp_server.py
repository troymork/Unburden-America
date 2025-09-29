#!/usr/bin/env python3
"""
Minimal JSON-RPC MCP-like shim (dev only).
- /rpc endpoint accepts {"method": "...","params": {...},"id": "..."}.
- Wires to agents via config/agents.manifest.json.
- Uses memory adapters in ./../memory/adapters.
NOTE: This is a dev scaffold (no secrets, no auth). Put behind localhost only.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os, sys, importlib.util

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST = os.path.join(ROOT, "config", "agents.manifest.json")
MEMORY_ADAPTER = os.path.join(ROOT, "memory", "adapters", "memory_local.py")

def load_json(p): 
    with open(p, "r") as f: return json.load(f)

def load_adapter(path):
    spec = importlib.util.spec_from_file_location("mem", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

class Handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_POST(self):
        if self.path != "/rpc": return self._json(404, {"error":"not found"})
        length = int(self.headers.get("Content-Length","0"))
        body = self.rfile.read(length)
        try:
            req = json.loads(body)
            method = req.get("method"); params = req.get("params",{}); _id = req.get("id")
            mem = load_adapter(MEMORY_ADAPTER)
            if method == "get_memory":
                return self._json(200, {"id":_id,"result": mem.get(params)})
            if method == "write_memory":
                return self._json(200, {"id":_id,"result": mem.put(params)})
            if method == "route_intent":
                # minimal echo for dry-run; orchestrator logic lives in agents/ORCHESTRATION_AGENT.md
                dag = {"nodes":["fact_check","compliance","produce"],"edges":[["fact_check","compliance"],["compliance","produce"]]}
                return self._json(200, {"id":_id,"result":{"workflow_dag": dag, "status":"accepted"}})
            return self._json(400, {"id":_id,"error":"unknown method"})
        except Exception as e:
            return self._json(500, {"error": str(e)})

def main():
    port = int(os.environ.get("MCP_PORT","7801"))
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"[MCP] listening on 127.0.0.1:{port}")
    server.serve_forever()

if __name__ == "__main__":
    main()
