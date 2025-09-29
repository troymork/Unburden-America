# Dev-only in-memory "KV + documents" adapter.
# For production, replace with Postgres/Vector DB and add ACLs.
DB = {"policy_knowledge": [], "campaign_memory": [], "compliance_memory": [], "stakeholder_memory": [], "performance_memory": []}

def get(params):
    scope = params.get("scope"); q = params.get("q")
    if scope and scope in DB:
        if not q: return {"scope": scope, "items": DB[scope]}
        return {"scope": scope, "items": [x for x in DB[scope] if q.lower() in str(x).lower()]}
    return {"scopes": list(DB.keys())}

def put(params):
    scope = params.get("scope"); item = params.get("item")
    if scope not in DB: return {"ok": False, "error": "unknown scope"}
    DB[scope].append(item)
    return {"ok": True, "count": len(DB[scope])}
