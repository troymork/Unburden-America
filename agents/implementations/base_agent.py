#!/usr/bin/env python3
"""
Base Agent Framework for IsThereEnoughMoney Movement
====================================================

This module provides the foundational framework for all AI agents in the
movement's automation pipeline, ensuring consistency, compliance, and quality.
"""

import asyncio
import logging
import datetime
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    BLOCKED = "blocked"

class QualityGateResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"

@dataclass
class Source:
    """Represents a source for fact-checking and verification"""
    url: str
    title: str
    source_type: str  # 'government', 'academic', 'news', 'primary', 'secondary'
    reliability_score: float  # 0.0 to 1.0
    date_accessed: str
    content_hash: Optional[str] = None
    archive_url: Optional[str] = None

@dataclass
class FactCheck:
    """Represents a fact-check result"""
    claim: str
    verification_status: str  # 'verified', 'disputed', 'uncertain', 'false'
    sources: List[Source]
    confidence_level: float  # 0.0 to 1.0
    notes: str
    checked_by: str
    checked_at: str

@dataclass
class ComplianceCheck:
    """Represents a compliance review result"""
    category: str  # 'legal', 'platform', 'accessibility', 'privacy'
    status: str   # 'compliant', 'non_compliant', 'needs_review'
    details: str
    recommendations: List[str]
    reviewed_by: str
    reviewed_at: str

@dataclass
class AgentOutput:
    """Standard output format for all agents"""
    agent_id: str
    agent_type: str
    status: AgentStatus
    primary_output: Dict[str, Any]
    metadata: Dict[str, Any]
    quality_scores: Dict[str, float]
    fact_checks: List[FactCheck]
    compliance_checks: List[ComplianceCheck]
    sources_used: List[Source]
    execution_time_ms: int
    created_at: str
    error_log: List[str] = None
    
    def __post_init__(self):
        if self.error_log is None:
            self.error_log = []

class BaseAgent(ABC):
    """Base class for all agents in the IsThereEnoughMoney movement"""
    
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.status = AgentStatus.IDLE
        self.capabilities = []
        self.quality_gates = []
        self.movement_principles = self._load_movement_principles()
        self.created_at = datetime.datetime.utcnow().isoformat()
        
    def _load_movement_principles(self) -> Dict[str, Any]:
        """Load core principles of the IsThereEnoughMoney movement"""
        return {
            "core_mission": "Tax the system, not the people",
            "verification_standard": "≥2 independent high-quality sources + cross-verification",
            "messaging_guidelines": {
                "no_targeted_political_persuasion": True,
                "broad_non_discriminatory": True,
                "focus_on_economic_facts": True,
                "avoid_partisan_language": True
            },
            "dual_economy_framework": {
                "real_economy_size": "~$30 Trillion (GDP)",
                "monetary_economy_size": "~$4.7 Quadrillion (Financial flows)",
                "proposed_tax_rate": "0.5% on monetary flows",
                "debt_elimination_target": "8 years"
            },
            "compliance_priorities": [
                "legal_compliance",
                "platform_terms_compliance", 
                "accessibility_standards",
                "privacy_protection"
            ]
        }
    
    @abstractmethod
    async def process(self, inputs: Dict[str, Any]) -> AgentOutput:
        """
        Process inputs and return structured output.
        Must be implemented by all agent subclasses.
        """
        pass
    
    @abstractmethod
    def get_agent_type(self) -> str:
        """Return the agent type identifier"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
    
    @abstractmethod
    def get_quality_gates(self) -> List[str]:
        """Return list of quality gates this agent must pass"""
        pass
    
    async def execute_with_monitoring(self, inputs: Dict[str, Any]) -> AgentOutput:
        """Execute agent processing with monitoring and error handling"""
        start_time = datetime.datetime.utcnow()
        self.status = AgentStatus.PROCESSING
        
        try:
            logger.info(f"Agent {self.agent_id} ({self.get_agent_type()}) starting processing")
            
            # Pre-processing validation
            await self._validate_inputs(inputs)
            
            # Main processing
            result = await self.process(inputs)
            
            # Post-processing quality checks
            await self._apply_quality_gates(result)
            
            # Final validation
            await self._validate_movement_compliance(result)
            
            self.status = AgentStatus.COMPLETED
            result.status = AgentStatus.COMPLETED
            
            end_time = datetime.datetime.utcnow()
            result.execution_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            logger.info(f"Agent {self.agent_id} completed successfully in {result.execution_time_ms}ms")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            error_msg = f"Agent {self.agent_id} failed: {str(e)}"
            logger.error(error_msg)
            
            # Return error result
            end_time = datetime.datetime.utcnow()
            return AgentOutput(
                agent_id=self.agent_id,
                agent_type=self.get_agent_type(),
                status=AgentStatus.ERROR,
                primary_output={"error": str(e)},
                metadata={"inputs": inputs},
                quality_scores={},
                fact_checks=[],
                compliance_checks=[],
                sources_used=[],
                execution_time_ms=int((end_time - start_time).total_seconds() * 1000),
                created_at=start_time.isoformat(),
                error_log=[error_msg]
            )
    
    async def _validate_inputs(self, inputs: Dict[str, Any]):
        """Validate input parameters"""
        if not isinstance(inputs, dict):
            raise ValueError("Inputs must be a dictionary")
        
        # Check for required movement context
        if "context" not in inputs:
            inputs["context"] = "IsThereEnoughMoney Movement"
        
        # Ensure compliance with movement principles
        if "messaging_tone" not in inputs:
            inputs["messaging_tone"] = "factual_non_partisan"
    
    async def _apply_quality_gates(self, result: AgentOutput):
        """Apply quality gates specific to this agent"""
        gates = self.get_quality_gates()
        
        for gate in gates:
            gate_result = await self._check_quality_gate(gate, result)
            if gate_result == QualityGateResult.FAIL:
                raise ValueError(f"Quality gate '{gate}' failed")
            elif gate_result == QualityGateResult.WARNING:
                result.error_log.append(f"Quality gate '{gate}' issued warning")
    
    async def _check_quality_gate(self, gate_name: str, result: AgentOutput) -> QualityGateResult:
        """Check a specific quality gate"""
        
        if gate_name == "source_verification":
            # Require at least 2 sources for any factual claims
            if len(result.sources_used) < 2 and result.fact_checks:
                return QualityGateResult.FAIL
                
        elif gate_name == "dual_fact_check":
            # Require fact-checking for all claims
            if result.fact_checks and any(fc.confidence_level < 0.8 for fc in result.fact_checks):
                return QualityGateResult.WARNING
                
        elif gate_name == "compliance_review":
            # Require passing compliance checks
            if result.compliance_checks and any(cc.status == "non_compliant" for cc in result.compliance_checks):
                return QualityGateResult.FAIL
                
        elif gate_name == "movement_alignment":
            # Check alignment with movement principles
            if not await self._check_movement_alignment(result):
                return QualityGateResult.FAIL
        
        return QualityGateResult.PASS
    
    async def _check_movement_alignment(self, result: AgentOutput) -> bool:
        """Check if output aligns with movement principles"""
        
        # Check for partisan language (context-aware check)
        output_text = json.dumps(result.primary_output).lower()
        
        # Only flag clearly partisan usage, not neutral economic terms
        partisan_contexts = [
            "democrats are", "republicans are", "liberal agenda", "conservative agenda",
            "left-wing", "right-wing", "socialist agenda", "capitalist agenda",
            "vote democrat", "vote republican", "liberal policies", "conservative policies"
        ]
        
        for context in partisan_contexts:
            if context in output_text:
                logger.warning(f"Potential partisan context detected: {context}")
                return False
        
        # Allow neutral usage of economic terms
        return True
    
    async def _validate_movement_compliance(self, result: AgentOutput):
        """Validate compliance with movement standards"""
        
        # Ensure all factual claims have sources
        if result.fact_checks:
            for fact_check in result.fact_checks:
                if len(fact_check.sources) < 2:
                    raise ValueError(f"Insufficient sources for claim: {fact_check.claim}")
        
        # Ensure quality scores meet minimum thresholds
        min_quality_threshold = 0.7
        for metric, score in result.quality_scores.items():
            if score < min_quality_threshold:
                logger.warning(f"Low quality score for {metric}: {score}")
    
    def create_source(self, url: str, title: str, source_type: str, 
                     reliability_score: float = 0.8) -> Source:
        """Helper method to create a Source object"""
        return Source(
            url=url,
            title=title,
            source_type=source_type,
            reliability_score=reliability_score,
            date_accessed=datetime.datetime.utcnow().isoformat()
        )
    
    def create_fact_check(self, claim: str, verification_status: str,
                         sources: List[Source], confidence_level: float,
                         notes: str = "") -> FactCheck:
        """Helper method to create a FactCheck object"""
        return FactCheck(
            claim=claim,
            verification_status=verification_status,
            sources=sources,
            confidence_level=confidence_level,
            notes=notes,
            checked_by=self.agent_id,
            checked_at=datetime.datetime.utcnow().isoformat()
        )
    
    def create_compliance_check(self, category: str, status: str,
                              details: str, recommendations: List[str] = None) -> ComplianceCheck:
        """Helper method to create a ComplianceCheck object"""
        return ComplianceCheck(
            category=category,
            status=status,
            details=details,
            recommendations=recommendations or [],
            reviewed_by=self.agent_id,
            reviewed_at=datetime.datetime.utcnow().isoformat()
        )
    
    async def simulate_processing_delay(self, min_seconds: float = 0.1, max_seconds: float = 2.0):
        """Simulate realistic processing time for development/testing"""
        import random
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)

class MovementKnowledgeBase:
    """Knowledge base containing key facts about the IsThereEnoughMoney movement"""
    
    @staticmethod
    def get_core_facts() -> Dict[str, Any]:
        """Return core movement facts with sources"""
        return {
            "monetary_economy_size": {
                "value": "4.7_quadrillion_usd",
                "description": "Total flow of money through high-volume financial settlement systems",
                "confidence": 0.95,
                "sources": [
                    "Federal Reserve Payment System Statistics",
                    "Bank for International Settlements (BIS) Reports",
                    "DTCC Settlement Volume Data"
                ]
            },
            "real_economy_size": {
                "value": "30_trillion_usd",
                "description": "US Gross Domestic Product - production of goods and services",
                "confidence": 0.99,
                "sources": [
                    "Bureau of Economic Analysis (BEA)",
                    "Federal Reserve Economic Data (FRED)",
                    "Congressional Budget Office (CBO)"
                ]
            },
            "scale_difference": {
                "value": "150x",
                "description": "Monetary economy is ~150 times larger than real economy",
                "confidence": 0.90,
                "calculation": "4.7Q / 30T ≈ 150"
            },
            "proposed_tax_rate": {
                "value": "0.005",
                "description": "0.5% tax on monetary flows (50 cents per $100)",
                "rationale": "Ultra-low rate on massive base generates significant revenue"
            },
            "debt_elimination_timeline": {
                "value": "8_years",
                "description": "Target timeline to eliminate US national debt",
                "assumptions": "Consistent application of monetary flow tax revenue"
            }
        }
    
    @staticmethod
    def get_messaging_guidelines() -> Dict[str, str]:
        """Return approved messaging guidelines"""
        return {
            "primary_message": "Tax the system, not the people",
            "tone": "Hopeful, factual, non-partisan",
            "avoid": "Partisan attacks, fear-mongering, complex jargon",
            "focus": "Economic opportunity, shared prosperity, practical solutions",
            "target_audience": "Working families, small business owners, fiscal conservatives and progressives"
        }

# Export key classes
__all__ = [
    'BaseAgent', 'AgentOutput', 'AgentStatus', 'Source', 'FactCheck', 
    'ComplianceCheck', 'QualityGateResult', 'MovementKnowledgeBase'
]