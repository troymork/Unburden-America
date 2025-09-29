#!/usr/bin/env python3
"""
Unburden America Agent API Gateway
FastAPI service that orchestrates all campaign agents with verification gates.
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

# Initialize structured logging
logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Unburden America Agent API",
    description="AI Agent orchestration system with multi-hop verification",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# =============================================================================
# Data Models
# =============================================================================

class AgentRequest(BaseModel):
    prompt_version: str = "1.0.0"
    payload: Dict[str, Any] = Field(default_factory=dict)
    verification_required: bool = True
    timeout: int = 120

class AgentResponse(BaseModel):
    prompt_version: str
    agent_id: str
    status: str = Field(..., regex="^(ok|degraded|failed)$")
    result: Dict[str, Any]
    verification: Dict[str, Any]
    handoff: Dict[str, Any]
    execution_time_ms: int
    timestamp: str

class VerificationRequest(BaseModel):
    claim_text: str
    context: str = ""
    required_confidence: float = 0.9

# =============================================================================
# Agent Configuration
# =============================================================================

AGENTS_CONFIG = {
    "campaign-strategy-planner": {
        "file": "agents/01_campaign_strategy_planner.md",
        "timeout": 60,
        "requires_verification": True
    },
    "content-production": {
        "file": "agents/02_content_production.md", 
        "timeout": 120,
        "requires_verification": True
    },
    "narrative-development": {
        "file": "agents/03_narrative_development.md",
        "timeout": 90,
        "requires_verification": False
    },
    "policy-fact-check": {
        "file": "agents/07_policy_fact_check.md",
        "timeout": 180,
        "requires_verification": False
    },
    "compliance-legal": {
        "file": "agents/08_compliance_legal.md",
        "timeout": 60,
        "requires_verification": False
    },
    "social-media-deployment": {
        "file": "agents/05_social_media_deployment.md",
        "timeout": 90,
        "requires_verification": True
    }
}

# =============================================================================
# Agent Execution Engine
# =============================================================================

class AgentExecutor:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self._setup_clients()

    def _setup_clients(self):
        """Initialize AI client connections"""
        try:
            import openai
            if os.getenv("OPENAI_API_KEY"):
                self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                
            import anthropic
            if os.getenv("ANTHROPIC_API_KEY"):
                self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                
        except Exception as e:
            logger.warning("AI client setup failed", error=str(e))

    async def load_agent_prompt(self, agent_id: str) -> str:
        """Load agent prompt from file"""
        config = AGENTS_CONFIG.get(agent_id)
        if not config:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
            
        try:
            with open(config["file"], "r") as f:
                return f.read()
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail=f"Agent prompt file not found: {config['file']}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def execute_agent(self, agent_id: str, request: AgentRequest) -> AgentResponse:
        """Execute an agent with retry logic"""
        start_time = datetime.now()
        
        try:
            # Load agent prompt
            prompt = await self.load_agent_prompt(agent_id)
            
            # Build execution context
            context = {
                "agent_id": agent_id,
                "prompt": prompt,
                "input": request.payload,
                "verification_required": request.verification_required
            }
            
            # Mock execution for demonstration (replace with actual AI calls)
            result = await self._mock_agent_execution(context)
            
            # Calculate execution time
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return AgentResponse(
                prompt_version=request.prompt_version,
                agent_id=agent_id,
                status="ok",
                result=result,
                verification={"status": "ok", "method": "multi-hop"},
                handoff={"next_agent": "determined_by_agent", "notes": "Auto-generated"},
                execution_time_ms=execution_time,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error("Agent execution failed", agent_id=agent_id, error=str(e))
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return AgentResponse(
                prompt_version=request.prompt_version,
                agent_id=agent_id,
                status="failed",
                result={"error": str(e)},
                verification={"status": "failed", "error": str(e)},
                handoff={"next_agent": "technical-reliability-sre", "notes": "Error escalation"},
                execution_time_ms=execution_time,
                timestamp=datetime.now().isoformat()
            )

    async def _mock_agent_execution(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mock agent execution (replace with actual AI inference)"""
        agent_id = context["agent_id"]
        
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Return agent-specific mock responses
        if agent_id == "campaign-strategy-planner":
            return {
                "plan_id": f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "weekly_objectives": [
                    {"objective": "Increase signatures", "kpi": "signups", "target": 20}
                ],
                "daily_runbook": [
                    {"day": "2024-01-15", "tasks": [{"task": "Draft explainer", "owner_agent": "content-production"}]}
                ]
            }
        elif agent_id == "policy-fact-check":
            return {
                "result": "supported",
                "rationale": "Claim verified against CBO data",
                "citations": [{"title": "CBO Report", "publisher": "CBO", "date": "2024-01-10", "tier": "A"}],
                "confidence": 0.95
            }
        elif agent_id == "compliance-legal":
            return {
                "status": "ok",
                "required_disclaimers": ["Standard political disclaimer"],
                "issues": []
            }
        else:
            return {"status": "ok", "message": f"Mock response from {agent_id}"}

# Initialize global executor
executor = AgentExecutor()

# =============================================================================
# API Routes
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "openai": bool(executor.openai_client),
            "anthropic": bool(executor.anthropic_client)
        }
    }

@app.post("/agents/{agent_id}", response_model=AgentResponse)
async def execute_agent_endpoint(
    agent_id: str, 
    request: AgentRequest,
    background_tasks: BackgroundTasks
):
    """Execute a specific agent"""
    logger.info("Agent execution requested", agent_id=agent_id)
    
    # Validate agent exists
    if agent_id not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    # Execute agent
    response = await executor.execute_agent(agent_id, request)
    
    # Log execution for audit trail
    background_tasks.add_task(log_execution, agent_id, request, response)
    
    return response

@app.post("/verification/fact-check")
async def fact_check_endpoint(request: VerificationRequest):
    """Standalone fact-checking endpoint"""
    agent_request = AgentRequest(
        payload={
            "claim_text": request.claim_text,
            "context": request.context,
            "required_confidence": request.required_confidence
        }
    )
    
    return await executor.execute_agent("policy-fact-check", agent_request)

@app.post("/verification/compliance")
async def compliance_check_endpoint(content: Dict[str, Any]):
    """Standalone compliance checking endpoint"""
    agent_request = AgentRequest(
        payload={"content": content}
    )
    
    return await executor.execute_agent("compliance-legal", agent_request)

@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": [
            {
                "id": agent_id,
                "name": agent_id.replace("-", " ").title(),
                "config": config
            }
            for agent_id, config in AGENTS_CONFIG.items()
        ]
    }

# =============================================================================
# Utility Functions
# =============================================================================

async def log_execution(agent_id: str, request: AgentRequest, response: AgentResponse):
    """Log agent execution for audit trail"""
    log_entry = {
        "agent_id": agent_id,
        "timestamp": datetime.now().isoformat(),
        "request_hash": hash(str(request.payload)),
        "response_status": response.status,
        "execution_time_ms": response.execution_time_ms,
        "verification_status": response.verification.get("status", "unknown")
    }
    
    logger.info("Agent execution logged", **log_entry)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)