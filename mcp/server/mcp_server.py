#!/usr/bin/env python3
"""
Enhanced MCP Server for IsThereEnoughMoney Movement
- Integrates with Enhanced Orchestrator for AI agent coordination
- /rpc endpoint accepts {"method": "...","params": {...},"id": "..."}.
- Supports advanced workflow orchestration and real-time status tracking
- Uses memory adapters for persistence and state management
NOTE: This is a development server (no auth). Put behind localhost only.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os, sys, importlib.util, asyncio, threading
import traceback
from typing import Dict, Any

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST = os.path.join(ROOT, "config", "agents.manifest.json")
MEMORY_ADAPTER = os.path.join(ROOT, "memory", "adapters", "memory_local.py")
ORCHESTRATOR_PATH = os.path.join(ROOT, "orchestration")

# Add orchestrator to Python path
sys.path.insert(0, ORCHESTRATOR_PATH)

def load_json(p): 
    with open(p, "r") as f: return json.load(f)

def load_adapter(path):
    spec = importlib.util.spec_from_file_location("mem", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

# Initialize the enhanced orchestrator
try:
    from enhanced_orchestrator import orchestrator, Priority
    ORCHESTRATOR_AVAILABLE = True
    print("[MCP] Enhanced Orchestrator loaded successfully")
except ImportError as e:
    ORCHESTRATOR_AVAILABLE = False
    print(f"[MCP] Warning: Enhanced Orchestrator not available: {e}")

# Event loop for async operations
LOOP = None
LOOP_THREAD = None

def setup_event_loop():
    """Setup asyncio event loop for orchestrator operations"""
    global LOOP, LOOP_THREAD
    
    def run_loop():
        global LOOP
        LOOP = asyncio.new_event_loop()
        asyncio.set_event_loop(LOOP)
        LOOP.run_forever()
    
    LOOP_THREAD = threading.Thread(target=run_loop, daemon=True)
    LOOP_THREAD.start()
    
    # Wait for loop to be available
    import time
    for _ in range(10):
        if LOOP is not None:
            break
        time.sleep(0.1)

def run_async_in_thread(coro):
    """Run async coroutine in the event loop thread"""
    if LOOP is None:
        setup_event_loop()
    
    future = asyncio.run_coroutine_threadsafe(coro, LOOP)
    return future.result(timeout=30)  # 30 second timeout

class Handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        """Handle GET requests for health check"""
        if self.path == "/health":
            return self._json(200, {
                "status": "healthy",
                "orchestrator_available": ORCHESTRATOR_AVAILABLE,
                "timestamp": self._get_timestamp(),
                "server_version": "1.0.0",
                "endpoints": ["/health", "/rpc", "/status"]
            })
        else:
            return self._json(404, {"error": "endpoint not found"})

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path not in ["/rpc", "/status", "/health"]: 
            return self._json(404, {"error":"endpoint not found"})
        
        # Health check endpoint
        if self.path == "/health":
            return self._json(200, {
                "status": "healthy",
                "orchestrator_available": ORCHESTRATOR_AVAILABLE,
                "timestamp": self._get_timestamp()
            })
        
        length = int(self.headers.get("Content-Length","0"))
        body = self.rfile.read(length) if length > 0 else b'{}'
        
        try:
            req = json.loads(body) if body else {}
            method = req.get("method")
            params = req.get("params", {})
            _id = req.get("id", "1")
            
            # Handle status endpoint
            if self.path == "/status":
                workflow_id = params.get("workflow_id")
                return self._handle_status_request(workflow_id, _id)
            
            # Handle RPC methods
            if method == "get_memory":
                return self._handle_memory_get(params, _id)
            elif method == "write_memory":
                return self._handle_memory_write(params, _id)
            elif method == "route_intent":
                return self._handle_route_intent(params, _id)
            elif method == "get_workflow_status":
                return self._handle_workflow_status(params, _id)
            elif method == "list_workflows":
                return self._handle_list_workflows(params, _id)
            elif method == "get_agent_registry":
                return self._handle_get_agent_registry(params, _id)
            elif method == "get_task_output":
                return self._handle_get_task_output(params, _id)
            else:
                return self._json(400, {"id": _id, "error": f"unknown method: {method}"})
                
        except json.JSONDecodeError as e:
            return self._json(400, {"error": f"invalid JSON: {str(e)}"})
        except Exception as e:
            print(f"[MCP] Error handling request: {e}")
            traceback.print_exc()
            return self._json(500, {"error": f"internal server error: {str(e)}"})

    def _get_timestamp(self):
        """Get current timestamp"""
        import datetime
        return datetime.datetime.utcnow().isoformat() + "Z"

    def _handle_memory_get(self, params: Dict[str, Any], request_id: str):
        """Handle memory get operations"""
        try:
            mem = load_adapter(MEMORY_ADAPTER)
            result = mem.get(params)
            return self._json(200, {"id": request_id, "result": result})
        except Exception as e:
            return self._json(500, {"id": request_id, "error": f"memory get failed: {str(e)}"})

    def _handle_memory_write(self, params: Dict[str, Any], request_id: str):
        """Handle memory write operations"""
        try:
            mem = load_adapter(MEMORY_ADAPTER)
            result = mem.put(params)
            return self._json(200, {"id": request_id, "result": result})
        except Exception as e:
            return self._json(500, {"id": request_id, "error": f"memory write failed: {str(e)}"})

    def _handle_route_intent(self, params: Dict[str, Any], request_id: str):
        """Handle intent routing with enhanced orchestrator"""
        try:
            if not ORCHESTRATOR_AVAILABLE:
                # Fallback to simple DAG response
                dag = {
                    "nodes": ["fact_check", "compliance", "produce"],
                    "edges": [["fact_check", "compliance"], ["compliance", "produce"]]
                }
                return self._json(200, {
                    "id": request_id,
                    "result": {
                        "workflow_dag": dag,
                        "status": "accepted",
                        "message": "Using fallback orchestrator"
                    }
                })
            
            # Extract parameters
            intent = params.get("intent", "")
            payload = params.get("payload", {})
            context_history = params.get("context_history", [])
            priority_str = params.get("priority", "medium")
            
            # Convert priority string to enum
            priority_map = {
                "low": Priority.LOW,
                "medium": Priority.MEDIUM,
                "high": Priority.HIGH,
                "critical": Priority.CRITICAL
            }
            priority = priority_map.get(priority_str.lower(), Priority.MEDIUM)
            
            # Call enhanced orchestrator
            result = run_async_in_thread(
                orchestrator.route_intent(intent, payload, context_history, priority)
            )
            
            return self._json(200, {"id": request_id, "result": result})
            
        except Exception as e:
            print(f"[MCP] Error in route_intent: {e}")
            traceback.print_exc()
            return self._json(500, {
                "id": request_id,
                "error": f"route_intent failed: {str(e)}"
            })

    def _handle_workflow_status(self, params: Dict[str, Any], request_id: str):
        """Handle workflow status requests"""
        try:
            if not ORCHESTRATOR_AVAILABLE:
                return self._json(500, {
                    "id": request_id,
                    "error": "Enhanced orchestrator not available"
                })
            
            workflow_id = params.get("workflow_id")
            if not workflow_id:
                return self._json(400, {
                    "id": request_id,
                    "error": "workflow_id parameter required"
                })
            
            status = orchestrator.get_workflow_status(workflow_id)
            return self._json(200, {"id": request_id, "result": status})
            
        except Exception as e:
            return self._json(500, {
                "id": request_id,
                "error": f"workflow status failed: {str(e)}"
            })

    def _handle_list_workflows(self, params: Dict[str, Any], request_id: str):
        """Handle list workflows requests"""
        try:
            if not ORCHESTRATOR_AVAILABLE:
                return self._json(500, {
                    "id": request_id,
                    "error": "Enhanced orchestrator not available"
                })
            
            # Get summary of all active workflows
            workflows = []
            for workflow_id, workflow in orchestrator.active_workflows.items():
                workflows.append({
                    "workflow_id": workflow_id,
                    "name": workflow.name,
                    "status": workflow.status.value,
                    "created_at": workflow.created_at,
                    "task_count": len(workflow.tasks)
                })
            
            return self._json(200, {
                "id": request_id,
                "result": {
                    "workflows": workflows,
                    "total_count": len(workflows),
                    "timestamp": self._get_timestamp()
                }
            })
            
        except Exception as e:
            return self._json(500, {
                "id": request_id,
                "error": f"list workflows failed: {str(e)}"
            })

    def _handle_get_agent_registry(self, params: Dict[str, Any], request_id: str):
        """Handle agent registry requests"""
        try:
            if not ORCHESTRATOR_AVAILABLE:
                return self._json(500, {
                    "id": request_id,
                    "error": "Enhanced orchestrator not available"
                })
            
            # Convert agent registry to serializable format
            registry = {}
            for agent_type, config in orchestrator.agent_registry.items():
                registry[agent_type.value] = config
            
            return self._json(200, {
                "id": request_id,
                "result": {
                    "agents": registry,
                    "agent_count": len(registry),
                    "timestamp": self._get_timestamp()
                }
            })
            
        except Exception as e:
            return self._json(500, {
                "id": request_id,
                "error": f"get agent registry failed: {str(e)}"
            })

    def _handle_status_request(self, workflow_id: str, request_id: str):
        """Handle status endpoint requests"""
        try:
            if workflow_id:
                # Get specific workflow status
                return self._handle_workflow_status({"workflow_id": workflow_id}, request_id)
            else:
                # Get general system status
                status = {
                    "system_status": "operational",
                    "orchestrator_available": ORCHESTRATOR_AVAILABLE,
                    "active_workflows": len(orchestrator.active_workflows) if ORCHESTRATOR_AVAILABLE else 0,
                    "timestamp": self._get_timestamp()
                }
                
                if ORCHESTRATOR_AVAILABLE:
                    # Add workflow summaries
                    workflow_summary = {}
                    for status_type in ["pending", "in_progress", "completed", "failed"]:
                        count = sum(1 for w in orchestrator.active_workflows.values() 
                                  if w.status.value == status_type)
                        workflow_summary[status_type] = count
                    status["workflow_summary"] = workflow_summary
                
                return self._json(200, {"id": request_id, "result": status})
                
        except Exception as e:
            return self._json(500, {
                "id": request_id,
                "error": f"status request failed: {str(e)}"
            })

    def _handle_get_task_output(self, params: Dict[str, Any], request_id: str):
        """Handle task output retrieval requests"""
        try:
            if not ORCHESTRATOR_AVAILABLE:
                return self._json(500, {
                    "id": request_id,
                    "error": "Enhanced orchestrator not available"
                })
            
            workflow_id = params.get("workflow_id")
            task_id = params.get("task_id")
            
            if not workflow_id:
                return self._json(400, {
                    "id": request_id,
                    "error": "workflow_id parameter required"
                })
            
            # Find the workflow
            workflow = orchestrator.active_workflows.get(workflow_id)
            if not workflow:
                return self._json(404, {
                    "id": request_id,
                    "error": f"Workflow {workflow_id} not found"
                })
            
            print(f"[DEBUG] Workflow {workflow_id} found with {len(workflow.tasks)} tasks")
            
            # If task_id specified, return specific task output
            if task_id:
                task = next((t for t in workflow.tasks if t.task_id == task_id), None)
                if not task:
                    return self._json(404, {
                        "id": request_id,
                        "error": f"Task {task_id} not found in workflow"
                    })
                
                print(f"[DEBUG] Task {task_id} found with attributes: {dir(task)}")
                print(f"[DEBUG] Task outputs: {getattr(task, 'outputs', 'NO OUTPUTS ATTR')}")
                
                return self._json(200, {
                    "id": request_id,
                    "result": {
                        "task_id": task.task_id,
                        "agent_type": task.agent_type.value,
                        "status": task.status.value,
                        "outputs": self._make_json_serializable(getattr(task, 'outputs', {})),
                        "verification_sources": self._make_json_serializable(getattr(task, 'verification_sources', [])),
                        "compliance_notes": getattr(task, 'compliance_notes', ""),
                        "timestamp": self._get_timestamp()
                    }
                })
            
            # Otherwise return all task outputs for the workflow
            task_outputs = []
            for i, task in enumerate(workflow.tasks):
                print(f"[DEBUG] Task {i}: {task.task_id}, Agent: {task.agent_type}, Status: {task.status}")
                print(f"[DEBUG] Task {i} has outputs attr: {hasattr(task, 'outputs')}")
                if hasattr(task, 'outputs'):
                    print(f"[DEBUG] Task {i} outputs: {task.outputs}")
                
                task_outputs.append({
                    "task_id": task.task_id,
                    "agent_type": task.agent_type.value,
                    "status": task.status.value,
                    "outputs": self._make_json_serializable(getattr(task, 'outputs', {})),
                    "verification_sources": self._make_json_serializable(getattr(task, 'verification_sources', [])),
                    "compliance_notes": getattr(task, 'compliance_notes', "")
                })
            
            return self._json(200, {
                "id": request_id,
                "result": {
                    "workflow_id": workflow_id,
                    "workflow_name": workflow.name,
                    "workflow_status": workflow.status.value,
                    "task_outputs": task_outputs,
                    "timestamp": self._get_timestamp()
                }
            })
            
        except Exception as e:
            import traceback
            print(f"[ERROR] get_task_output failed: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return self._json(500, {
                "id": request_id,
                "error": f"get task output failed: {str(e)}"
            })

    def _make_json_serializable(self, obj):
        """Convert complex objects to JSON serializable format"""
        if hasattr(obj, '__dict__'):
            # Convert objects with attributes to dictionaries
            result = {}
            for key, value in obj.__dict__.items():
                result[key] = self._make_json_serializable(value)
            return result
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._make_json_serializable(value) for key, value in obj.items()}
        else:
            # For basic types, return as-is
            try:
                json.dumps(obj)  # Test if it's JSON serializable
                return obj
            except (TypeError, ValueError):
                return str(obj)  # Convert non-serializable to string

def main():
    port = int(os.environ.get("MCP_PORT","7801"))
    
    # Initialize event loop for async operations
    if ORCHESTRATOR_AVAILABLE:
        print("[MCP] Setting up event loop for orchestrator...")
        setup_event_loop()
        print("[MCP] Event loop initialized successfully")
    
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"[MCP] Enhanced server listening on 0.0.0.0:{port}")
    print(f"[MCP] Available endpoints:")
    print(f"  POST /rpc - JSON-RPC interface")
    print(f"  GET/POST /status - System status")
    print(f"  GET /health - Health check")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[MCP] Shutting down server...")
        if LOOP and not LOOP.is_closed():
            LOOP.call_soon_threadsafe(LOOP.stop)
        server.server_close()

if __name__ == "__main__":
    main()
