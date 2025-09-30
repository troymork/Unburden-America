#!/usr/bin/env python3
"""
Agent Factory for IsThereEnoughMoney Movement
=============================================

This factory creates and manages AI agent instances, providing a unified
interface for the orchestrator to interact with all movement agents.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Type, Union
import datetime
from enum import Enum

# Import base classes
from agents.implementations.base_agent import BaseAgent, AgentOutput, AgentStatus, MovementKnowledgeBase

# Import agent implementations
from agents.implementations.content_producer_agent import ContentProducerAgent
from agents.implementations.fact_checker_agent import FactCheckerAgent
from agents.implementations.compliance_reviewer_agent import ComplianceReviewerAgent

logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Agent types available in the system"""
    CONTENT_PRODUCER = "content_producer"
    FACT_CHECKER = "fact_checker"
    COMPLIANCE_REVIEWER = "compliance_reviewer"
    SOCIAL_MEDIA = "social_media"
    ANALYTICS = "analytics"
    PETITION_OPTIMIZER = "petition_optimizer"
    FUNDRAISING = "fundraising"
    NARRATIVE_DEVELOPER = "narrative_developer"
    VISUAL_DESIGNER = "visual_designer"

class MockAgent(BaseAgent):
    """Mock agent for agents not yet implemented"""
    
    def __init__(self, agent_type: str, capabilities: List[str], quality_gates: List[str], agent_id: str = None):
        super().__init__(agent_id)
        self._agent_type = agent_type
        self.capabilities = capabilities
        self.quality_gates = quality_gates
    
    def get_agent_type(self) -> str:
        return self._agent_type
    
    def get_capabilities(self) -> List[str]:
        return self.capabilities
    
    def get_quality_gates(self) -> List[str]:
        return self.quality_gates
    
    async def process(self, inputs: Dict[str, Any]) -> AgentOutput:
        """Mock processing - returns simulated output"""
        
        # Simulate processing time
        await self.simulate_processing_delay(0.5, 2.0)
        
        logger.info(f"Mock {self._agent_type} agent processing: {inputs.get('description', 'No description')}")
        
        # Generate mock output based on agent type
        if self._agent_type == "social_media":
            primary_output = {
                "posts_created": 3,
                "platforms": ["twitter", "facebook", "instagram"],
                "engagement_forecast": {"likes": 150, "shares": 45, "comments": 28},
                "hashtags": ["#TaxTheSystem", "#UnburdenAmerica", "#IsThereEnoughMoney"],
                "scheduling": "Posts scheduled for optimal engagement times"
            }
        elif self._agent_type == "analytics":
            primary_output = {
                "metrics": {
                    "reach": 12500,
                    "engagement_rate": 0.065,
                    "conversion_rate": 0.032,
                    "roi_estimate": 3.2
                },
                "insights": [
                    "Economic messaging resonates well with target audience",
                    "Visual content performs 40% better than text-only",
                    "Peak engagement occurs during evening hours"
                ],
                "recommendations": [
                    "Increase visual content production",
                    "Focus on economic education themes",
                    "Optimize posting schedule for evening distribution"
                ]
            }
        elif self._agent_type == "petition_optimizer":
            primary_output = {
                "optimization_results": {
                    "conversion_rate_improvement": 0.23,
                    "form_abandonment_reduction": 0.18,
                    "mobile_usability_score": 0.92
                },
                "a_b_test_results": {
                    "headline_winner": "Tax the System, Not the People - Sign Now",
                    "cta_winner": "Add Your Voice",
                    "confidence_level": 0.95
                },
                "recommendations": [
                    "Implement winning headline variation",
                    "Reduce form fields from 8 to 5",
                    "Add trust indicators above signature form"
                ]
            }
        elif self._agent_type == "fundraising":
            primary_output = {
                "campaign_setup": {
                    "donation_tiers": [25, 50, 100, 250, 500],
                    "suggested_recurring_options": ["monthly", "quarterly"],
                    "donor_journey_stages": 5
                },
                "ethical_optimizations": [
                    "Clear fund usage transparency",
                    "No dark pattern donation flows", 
                    "Respectful follow-up cadence",
                    "Easy cancellation options"
                ],
                "projected_metrics": {
                    "average_donation": 75,
                    "conversion_rate": 0.028,
                    "donor_retention": 0.65
                }
            }
        elif self._agent_type == "narrative_developer":
            primary_output = {
                "narrative_structure": {
                    "hero": "American families and small businesses",
                    "challenge": "Crushing tax burden and national debt",
                    "mentor": "IsThereEnoughMoney movement",
                    "solution": "Monetary Flow Tax on financial systems",
                    "transformation": "Debt-free America with lower taxes"
                },
                "story_beats": [
                    "Current struggle with existing tax system",
                    "Discovery of the two-economy insight", 
                    "Vision of abundance through smart taxation",
                    "Call to join the movement"
                ],
                "emotional_arc": "Hope -> Understanding -> Empowerment -> Action"
            }
        elif self._agent_type == "visual_designer":
            primary_output = {
                "design_system": {
                    "color_palette": ["#2563eb", "#1d4ed8", "#f59e0b", "#10b981"],
                    "typography": "Clean, accessible sans-serif fonts",
                    "accessibility_score": 0.94
                },
                "visual_concepts": [
                    "Ping-pong ball vs basketball size comparison",
                    "Burden-lifting imagery (chains breaking)",
                    "Bridge to abundant future visualization",
                    "System vs people contrast graphics"
                ],
                "asset_delivery": {
                    "infographics": 3,
                    "social_media_templates": 12,
                    "web_graphics": 6,
                    "presentation_slides": 15
                }
            }
        else:
            primary_output = {
                "status": "completed",
                "message": f"Mock {self._agent_type} processing completed",
                "simulated": True
            }
        
        return AgentOutput(
            agent_id=self.agent_id,
            agent_type=self._agent_type,
            status=AgentStatus.COMPLETED,
            primary_output=primary_output,
            metadata={
                "mock_agent": True,
                "simulated_processing": True,
                "agent_capabilities": self.capabilities
            },
            quality_scores={
                "mock_quality_score": 0.85,
                "simulation_accuracy": 0.75
            },
            fact_checks=[],
            compliance_checks=[],
            sources_used=[],
            execution_time_ms=1500,  # Simulated
            created_at=datetime.datetime.utcnow().isoformat()
        )

class AgentFactory:
    """Factory for creating and managing AI agents"""
    
    def __init__(self):
        self.agent_registry: Dict[AgentType, Type[BaseAgent]] = {}
        self.active_agents: Dict[str, BaseAgent] = {}
        self.agent_configs = self._load_agent_configurations()
        self._register_agents()
    
    def _load_agent_configurations(self) -> Dict[AgentType, Dict[str, Any]]:
        """Load configurations for all agent types"""
        return {
            AgentType.CONTENT_PRODUCER: {
                "class": ContentProducerAgent,
                "description": "Research-driven content generation with source verification",
                "capabilities": ["research", "writing", "fact_verification", "citation"],
                "quality_gates": ["source_verification", "dual_fact_check", "movement_alignment"]
            },
            AgentType.FACT_CHECKER: {
                "class": FactCheckerAgent,
                "description": "Rigorous fact-checking with multiple source verification",
                "capabilities": ["source_validation", "claim_verification", "uncertainty_documentation"],
                "quality_gates": ["minimum_two_sources", "primary_source_preference", "confidence_threshold"]
            },
            AgentType.COMPLIANCE_REVIEWER: {
                "class": ComplianceReviewerAgent,
                "description": "Legal and platform compliance validation",
                "capabilities": ["legal_review", "platform_policy_check", "accessibility_audit"],
                "quality_gates": ["legal_compliance", "platform_compliance", "accessibility_standards"]
            },
            AgentType.SOCIAL_MEDIA: {
                "class": MockAgent,
                "description": "Multi-platform social media automation and management",
                "capabilities": ["content_scheduling", "engagement_tracking", "platform_optimization"],
                "quality_gates": ["platform_compliance", "brand_consistency"]
            },
            AgentType.ANALYTICS: {
                "class": MockAgent,
                "description": "Campaign performance tracking and predictive analytics",
                "capabilities": ["impact_measurement", "predictive_modeling", "ROI_analysis"],
                "quality_gates": ["data_accuracy", "attribution_validation"]
            },
            AgentType.PETITION_OPTIMIZER: {
                "class": MockAgent,
                "description": "Petition funnel optimization and conversion tracking",
                "capabilities": ["funnel_analysis", "A/B_testing", "conversion_optimization"],
                "quality_gates": ["consent_validation", "UX_standards"]
            },
            AgentType.FUNDRAISING: {
                "class": MockAgent,
                "description": "Ethical fundraising optimization and donor management",
                "capabilities": ["donor_journey_mapping", "ethical_ask_optimization", "retention_analysis"],
                "quality_gates": ["ethical_standards", "compliance_check"]
            },
            AgentType.NARRATIVE_DEVELOPER: {
                "class": MockAgent,
                "description": "Strategic narrative development using Hero's Journey framework",
                "capabilities": ["story_architecture", "emotional_arc_design", "accessibility_adaptation"],
                "quality_gates": ["narrative_coherence", "emotional_impact_validation"]
            },
            AgentType.VISUAL_DESIGNER: {
                "class": MockAgent,
                "description": "Accessibility-first visual design and brand consistency",
                "capabilities": ["visual_design", "accessibility_optimization", "brand_application"],
                "quality_gates": ["accessibility_compliance", "brand_consistency"]
            }
        }
    
    def _register_agents(self):
        """Register all agent classes in the factory"""
        for agent_type, config in self.agent_configs.items():
            self.agent_registry[agent_type] = config["class"]
            logger.info(f"Registered agent: {agent_type.value}")
    
    def create_agent(self, agent_type: Union[str, AgentType], agent_id: str = None) -> BaseAgent:
        """Create an agent instance of the specified type"""
        
        # Convert string to enum if needed
        if isinstance(agent_type, str):
            try:
                agent_type = AgentType(agent_type)
            except ValueError:
                raise ValueError(f"Unknown agent type: {agent_type}")
        
        if agent_type not in self.agent_registry:
            raise ValueError(f"Agent type {agent_type.value} not registered")
        
        agent_class = self.agent_registry[agent_type]
        config = self.agent_configs[agent_type]
        
        # Create agent instance
        if agent_class == MockAgent:
            # Mock agents need additional parameters
            agent = agent_class(
                agent_type=agent_type.value,
                capabilities=config["capabilities"],
                quality_gates=config["quality_gates"],
                agent_id=agent_id
            )
        else:
            agent = agent_class(agent_id)
        
        # Store in active agents
        self.active_agents[agent.agent_id] = agent
        
        logger.info(f"Created {agent_type.value} agent with ID: {agent.agent_id}")
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Retrieve an active agent by ID"""
        return self.active_agents.get(agent_id)
    
    def get_agent_by_type(self, agent_type: Union[str, AgentType]) -> Optional[BaseAgent]:
        """Get the first active agent of the specified type"""
        
        if isinstance(agent_type, str):
            try:
                agent_type = AgentType(agent_type)
            except ValueError:
                return None
        
        for agent in self.active_agents.values():
            if agent.get_agent_type() == agent_type.value:
                return agent
        
        return None
    
    def list_available_agent_types(self) -> List[Dict[str, Any]]:
        """List all available agent types with their configurations"""
        
        agent_list = []
        for agent_type, config in self.agent_configs.items():
            agent_list.append({
                "type": agent_type.value,
                "description": config["description"],
                "capabilities": config["capabilities"],
                "quality_gates": config["quality_gates"],
                "implemented": config["class"] != MockAgent
            })
        
        return agent_list
    
    def get_active_agents_summary(self) -> Dict[str, Any]:
        """Get summary of all active agents"""
        
        summary = {
            "total_agents": len(self.active_agents),
            "agents_by_type": {},
            "agents": []
        }
        
        for agent in self.active_agents.values():
            agent_type = agent.get_agent_type()
            
            if agent_type not in summary["agents_by_type"]:
                summary["agents_by_type"][agent_type] = 0
            summary["agents_by_type"][agent_type] += 1
            
            summary["agents"].append({
                "id": agent.agent_id,
                "type": agent_type,
                "status": agent.status.value,
                "capabilities": agent.get_capabilities(),
                "created_at": agent.created_at
            })
        
        return summary
    
    async def execute_agent_task(self, agent_type: Union[str, AgentType], 
                               inputs: Dict[str, Any]) -> AgentOutput:
        """Execute a task using the specified agent type"""
        
        # Get or create agent
        agent = self.get_agent_by_type(agent_type)
        if not agent:
            agent = self.create_agent(agent_type)
        
        # Execute task with monitoring
        try:
            result = await agent.execute_with_monitoring(inputs)
            logger.info(f"Agent task completed: {agent.get_agent_type()} -> {result.status.value}")
            return result
            
        except Exception as e:
            logger.error(f"Agent task failed: {agent.get_agent_type()} -> {str(e)}")
            raise
    
    def cleanup_inactive_agents(self, max_idle_hours: int = 24):
        """Clean up agents that have been inactive for too long"""
        
        cutoff_time = datetime.datetime.utcnow() - datetime.timedelta(hours=max_idle_hours)
        inactive_agents = []
        
        for agent_id, agent in self.active_agents.items():
            created_time = datetime.datetime.fromisoformat(agent.created_at)
            if created_time < cutoff_time and agent.status == AgentStatus.IDLE:
                inactive_agents.append(agent_id)
        
        for agent_id in inactive_agents:
            del self.active_agents[agent_id]
            logger.info(f"Cleaned up inactive agent: {agent_id}")
        
        return len(inactive_agents)
    
    def shutdown_all_agents(self):
        """Shutdown all active agents"""
        
        for agent in self.active_agents.values():
            agent.status = AgentStatus.IDLE
        
        self.active_agents.clear()
        logger.info("All agents shut down")

# Global agent factory instance
agent_factory = AgentFactory()

# Convenience functions for external use
def create_agent(agent_type: Union[str, AgentType], agent_id: str = None) -> BaseAgent:
    """Create an agent using the global factory"""
    return agent_factory.create_agent(agent_type, agent_id)

def execute_agent_task(agent_type: Union[str, AgentType], inputs: Dict[str, Any]) -> AgentOutput:
    """Execute an agent task using the global factory"""
    return asyncio.run(agent_factory.execute_agent_task(agent_type, inputs))

def get_available_agents() -> List[Dict[str, Any]]:
    """Get list of available agent types"""
    return agent_factory.list_available_agent_types()

def get_active_agents_info() -> Dict[str, Any]:
    """Get information about active agents"""
    return agent_factory.get_active_agents_summary()

# Export key classes and functions
__all__ = [
    'AgentFactory', 'AgentType', 'MockAgent', 'agent_factory',
    'create_agent', 'execute_agent_task', 'get_available_agents', 'get_active_agents_info'
]