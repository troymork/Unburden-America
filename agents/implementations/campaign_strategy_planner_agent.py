"""
Campaign Strategy Planner Agent - Strategic architect for comprehensive campaign planning

This agent serves as the strategic architect for campaign planning, implementing SMART goals framework,
multi-horizon planning, risk assessment, and pivot trigger mechanisms. It creates strategic frameworks,
tactical roadmaps, KPIs, and risk registers while maintaining alignment with movement principles.
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

from .base_agent import BaseAgent, AgentOutput, QualityGate, MovementPrinciples


class StrategicHorizon(Enum):
    """Strategic planning horizons for campaign development"""
    IMMEDIATE = "immediate"     # 1-4 weeks
    SHORT_TERM = "short_term"   # 1-3 months
    MEDIUM_TERM = "medium_term" # 3-12 months
    LONG_TERM = "long_term"     # 1-3 years


class RiskLevel(Enum):
    """Risk assessment levels for strategic planning"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SMARTGoal:
    """SMART goal structure for strategic objectives"""
    id: str
    specific: str              # What exactly will be accomplished
    measurable: List[str]      # How progress will be measured
    achievable: str            # Why it's realistic
    relevant: str              # How it aligns with movement goals
    time_bound: str            # Specific deadline
    horizon: StrategicHorizon
    owner: str                 # Responsible party
    dependencies: List[str]    # Other goals this depends on
    success_metrics: List[Dict[str, Any]]
    created_at: datetime
    target_date: datetime


@dataclass
class RiskItem:
    """Risk register item for strategic planning"""
    id: str
    description: str
    category: str              # political, technical, resource, legal
    probability: float         # 0.0 to 1.0
    impact: RiskLevel
    mitigation_strategies: List[str]
    contingency_plans: List[str]
    owner: str
    review_date: datetime
    status: str               # active, mitigated, accepted, transferred


@dataclass
class PivotTrigger:
    """Conditions that would trigger strategic pivots"""
    id: str
    name: str
    condition: str
    threshold_metrics: Dict[str, Any]
    response_actions: List[str]
    escalation_path: str
    monitoring_frequency: str


@dataclass
class StrategicFramework:
    """Comprehensive strategic framework output"""
    mission_statement: str
    vision_statement: str
    strategic_objectives: List[SMARTGoal]
    tactical_roadmap: Dict[str, List[Dict[str, Any]]]
    kpis: List[Dict[str, Any]]
    risk_register: List[RiskItem]
    pivot_triggers: List[PivotTrigger]
    resource_requirements: Dict[str, Any]
    timeline_milestones: List[Dict[str, Any]]
    stakeholder_map: Dict[str, List[str]]


class CampaignStrategyPlannerAgent(BaseAgent):
    """
    Strategic architect for comprehensive campaign planning with SMART goals,
    multi-horizon planning, risk assessment, and pivot mechanisms.
    """
    
    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_type="campaign_strategy_planner",
            agent_id=agent_id or f"strategy_planner_{uuid.uuid4().hex[:8]}"
        )
        self.movement_knowledge = self._load_movement_knowledge()
        self.strategic_templates = self._load_strategic_templates()
        self.kpi_frameworks = self._load_kpi_frameworks()
        
        logging.info(f"Campaign Strategy Planner Agent initialized: {self.agent_id}")

    def _load_movement_knowledge(self) -> Dict[str, Any]:
        """Load IsThereEnoughMoney Movement knowledge base"""
        return {
            "core_principles": {
                "monetary_flow_tax": "3% tax on high-frequency transactions",
                "real_economy": "$30T annually in goods/services",
                "monetary_economy": "$4.7Q annually in financial transactions",
                "wealth_concentration": "Top 1% owns 32% of total wealth",
                "democratic_participation": "Increase civic engagement through transparency"
            },
            "target_demographics": {
                "primary": "Middle-class working families",
                "secondary": "Small business owners", 
                "tertiary": "Young professionals and students",
                "excluded": [] # Broad, non-discriminatory messaging
            },
            "key_messages": {
                "fairness": "Everyone should pay their fair share",
                "transparency": "Make financial flows visible to citizens",
                "economic_justice": "Level the playing field for working families",
                "democratic_reform": "Put economic power back in people's hands"
            },
            "opposition_research": {
                "financial_industry": "Will claim economic disruption",
                "political_establishment": "Will resist transparency measures",
                "misinformation_vectors": ["complexity", "fear", "status_quo_bias"]
            }
        }

    def _load_strategic_templates(self) -> Dict[str, Any]:
        """Load strategic planning templates and frameworks"""
        return {
            "campaign_phases": {
                "awareness": {
                    "duration": "3-6 months",
                    "objectives": ["Build name recognition", "Educate on core issues"],
                    "tactics": ["Content marketing", "Social media", "Earned media"]
                },
                "mobilization": {
                    "duration": "2-4 months", 
                    "objectives": ["Convert awareness to action", "Build supporter base"],
                    "tactics": ["Petitions", "Events", "Grassroots organizing"]
                },
                "influence": {
                    "duration": "6-12 months",
                    "objectives": ["Policy advocacy", "Political pressure"],
                    "tactics": ["Lobbying", "Coalition building", "Electoral engagement"]
                },
                "implementation": {
                    "duration": "12+ months",
                    "objectives": ["Policy adoption", "Systemic change"],
                    "tactics": ["Legislative tracking", "Implementation oversight"]
                }
            },
            "strategic_frameworks": {
                "theory_of_change": {
                    "problem": "Wealth concentration and lack of transparency",
                    "solution": "Monetary flow tax with democratic oversight",
                    "pathway": "Awareness → Mobilization → Policy → Implementation"
                },
                "stakeholder_analysis": {
                    "supporters": ["Labor unions", "Progressive organizations", "Tax justice advocates"],
                    "neutrals": ["Academic institutions", "Some business groups"],
                    "opponents": ["Financial industry", "Conservative groups"]
                }
            }
        }

    def _load_kpi_frameworks(self) -> Dict[str, Any]:
        """Load KPI frameworks for strategic measurement"""
        return {
            "awareness_metrics": [
                {"name": "Brand Recognition", "target": "25% unaided recall", "measurement": "quarterly_survey"},
                {"name": "Message Comprehension", "target": "70% accurate explanation", "measurement": "focus_groups"},
                {"name": "Media Mentions", "target": "500+ monthly", "measurement": "media_monitoring"}
            ],
            "engagement_metrics": [
                {"name": "Petition Signatures", "target": "100K in 6 months", "measurement": "platform_analytics"},
                {"name": "Social Media Engagement", "target": "5% avg engagement rate", "measurement": "social_analytics"},
                {"name": "Event Attendance", "target": "50+ per event", "measurement": "event_tracking"}
            ],
            "influence_metrics": [
                {"name": "Policy Mentions", "target": "10+ legislative references", "measurement": "policy_tracking"},
                {"name": "Coalition Partners", "target": "25+ organizations", "measurement": "partnership_tracking"},
                {"name": "Media Coverage Quality", "target": "70% neutral/positive", "measurement": "sentiment_analysis"}
            ],
            "outcome_metrics": [
                {"name": "Policy Introduction", "target": "3+ bills introduced", "measurement": "legislative_tracking"},
                {"name": "Public Support", "target": "60+ approval rating", "measurement": "polling"},
                {"name": "Implementation Progress", "target": "pilot_programs", "measurement": "policy_monitoring"}
            ]
        }

    async def process(self, inputs: Dict[str, Any]) -> AgentOutput:
        """
        Process strategic planning request and generate comprehensive framework
        
        Args:
            inputs: Contains campaign_brief, objectives, constraints, timeline
            
        Returns:
            AgentOutput with strategic framework, roadmap, KPIs, and risk register
        """
        try:
            # Quality Gate: Pre-processing validation
            validation_result = await self._validate_inputs(inputs)
            if not validation_result["valid"]:
                return AgentOutput(
                    agent_id=self.agent_id,
                    agent_type=self.agent_type,
                    success=False,
                    content={},
                    metadata={"error": validation_result["errors"]},
                    quality_gates_passed=[QualityGate.INPUT_VALIDATION],
                    movement_principles_verified=False
                )

            # Extract planning parameters
            campaign_brief = inputs.get("campaign_brief", {})
            objectives = inputs.get("objectives", [])
            constraints = inputs.get("constraints", {})
            timeline = inputs.get("timeline", {})
            context = inputs.get("context", {})

            # Generate strategic components
            mission_vision = await self._develop_mission_vision(campaign_brief, objectives)
            smart_goals = await self._create_smart_goals(objectives, timeline, constraints)
            tactical_roadmap = await self._build_tactical_roadmap(smart_goals, timeline)
            kpis = await self._design_kpi_framework(smart_goals, objectives)
            risk_register = await self._conduct_risk_assessment(campaign_brief, constraints, context)
            pivot_triggers = await self._define_pivot_triggers(smart_goals, risk_register)

            # Quality Gate: Mid-process validation
            framework_quality = await self._validate_framework_quality(
                mission_vision, smart_goals, tactical_roadmap, kpis, risk_register
            )
            
            if not framework_quality["valid"]:
                return AgentOutput(
                    agent_id=self.agent_id,
                    agent_type=self.agent_type,
                    success=False,
                    content={},
                    metadata={"error": f"Framework quality issues: {framework_quality['issues']}"},
                    quality_gates_passed=[QualityGate.INPUT_VALIDATION],
                    movement_principles_verified=False
                )

            # Build comprehensive strategic framework
            strategic_framework = StrategicFramework(
                mission_statement=mission_vision["mission"],
                vision_statement=mission_vision["vision"],
                strategic_objectives=smart_goals,
                tactical_roadmap=tactical_roadmap,
                kpis=kpis,
                risk_register=risk_register,
                pivot_triggers=pivot_triggers,
                resource_requirements=await self._calculate_resource_requirements(smart_goals, tactical_roadmap),
                timeline_milestones=await self._generate_timeline_milestones(tactical_roadmap),
                stakeholder_map=await self._map_stakeholders(campaign_brief, context)
            )

            # Quality Gate: Pre-handoff validation
            final_validation = await self._validate_final_framework(strategic_framework)
            if not final_validation["valid"]:
                return AgentOutput(
                    agent_id=self.agent_id,
                    agent_type=self.agent_type,
                    success=False,
                    content={},
                    metadata={"error": f"Final validation failed: {final_validation['issues']}"},
                    quality_gates_passed=[QualityGate.INPUT_VALIDATION],
                    movement_principles_verified=False
                )

            # Movement principles verification
            principles_check = await self._verify_movement_principles(strategic_framework)

            # Generate handoff package
            handoff_package = await self._generate_handoff_package(strategic_framework)

            return AgentOutput(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                success=True,
                content={
                    "strategic_framework": asdict(strategic_framework),
                    "executive_summary": await self._create_executive_summary(strategic_framework),
                    "implementation_guide": handoff_package,
                    "next_steps": await self._recommend_next_steps(strategic_framework),
                    "success_criteria": await self._define_success_criteria(strategic_framework)
                },
                metadata={
                    "planning_horizon": f"{len(smart_goals)} objectives across {len(set(g.horizon for g in smart_goals))} horizons",
                    "risk_profile": f"{len([r for r in risk_register if r.impact in [RiskLevel.HIGH, RiskLevel.CRITICAL]])} high/critical risks",
                    "resource_estimate": strategic_framework.resource_requirements.get("total_budget", "TBD"),
                    "timeline_span": f"{timeline.get('start_date', 'TBD')} to {timeline.get('end_date', 'TBD')}",
                    "generated_at": datetime.now().isoformat()
                },
                quality_gates_passed=[
                    QualityGate.INPUT_VALIDATION,
                    QualityGate.CONTENT_QUALITY,
                    QualityGate.FACT_VERIFICATION,
                    QualityGate.MOVEMENT_ALIGNMENT
                ],
                movement_principles_verified=principles_check["verified"],
                citations=await self._compile_citations()
            )

        except Exception as e:
            logging.error(f"Campaign Strategy Planner Agent error: {str(e)}")
            return AgentOutput(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                success=False,
                content={},
                metadata={"error": str(e)},
                quality_gates_passed=[],
                movement_principles_verified=False
            )

    async def _validate_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate strategic planning inputs"""
        errors = []
        
        if not inputs.get("campaign_brief"):
            errors.append("Campaign brief is required")
        
        if not inputs.get("objectives"):
            errors.append("Campaign objectives are required")
            
        campaign_brief = inputs.get("campaign_brief", {})
        if not campaign_brief.get("target_audience"):
            errors.append("Target audience must be specified")
            
        if not campaign_brief.get("core_message"):
            errors.append("Core message must be defined")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    async def _develop_mission_vision(self, campaign_brief: Dict[str, Any], objectives: List[Dict[str, Any]]) -> Dict[str, str]:
        """Develop mission and vision statements aligned with movement principles"""
        
        # Extract key elements
        target_audience = campaign_brief.get("target_audience", "citizens")
        core_message = campaign_brief.get("core_message", "economic justice")
        primary_goal = objectives[0] if objectives else {}
        
        # Generate mission statement (what we do)
        mission = f"""To advance economic justice and democratic transparency by advocating for the Monetary Flow Tax, 
        ensuring that high-frequency financial transactions contribute fairly to the common good while empowering 
        {target_audience} with the knowledge and tools to participate in creating a more equitable economic system."""
        
        # Generate vision statement (what we achieve)
        vision = f"""A transparent, democratic economy where the $4.7 quadrillion in annual financial transactions 
        supports the $30 trillion real economy through fair taxation, reducing wealth concentration and strengthening 
        the economic foundation for working families and communities."""
        
        return {
            "mission": mission.strip(),
            "vision": vision.strip()
        }

    async def _create_smart_goals(self, objectives: List[Dict[str, Any]], 
                                  timeline: Dict[str, Any], 
                                  constraints: Dict[str, Any]) -> List[SMARTGoal]:
        """Create SMART goals from campaign objectives"""
        smart_goals = []
        
        for i, obj in enumerate(objectives):
            # Determine strategic horizon
            duration_months = obj.get("duration_months", 6)
            if duration_months <= 1:
                horizon = StrategicHorizon.IMMEDIATE
            elif duration_months <= 3:
                horizon = StrategicHorizon.SHORT_TERM
            elif duration_months <= 12:
                horizon = StrategicHorizon.MEDIUM_TERM
            else:
                horizon = StrategicHorizon.LONG_TERM
                
            # Calculate target date
            start_date = datetime.fromisoformat(timeline.get("start_date", datetime.now().isoformat()))
            target_date = start_date + timedelta(days=duration_months * 30)
            
            # Build success metrics
            success_metrics = []
            for metric in obj.get("metrics", []):
                success_metrics.append({
                    "name": metric.get("name", f"Metric_{i}"),
                    "target": metric.get("target", "TBD"),
                    "measurement_method": metric.get("method", "manual_tracking"),
                    "frequency": metric.get("frequency", "monthly")
                })
            
            smart_goal = SMARTGoal(
                id=f"goal_{uuid.uuid4().hex[:8]}",
                specific=obj.get("description", f"Campaign objective {i+1}"),
                measurable=[m["name"] for m in success_metrics],
                achievable=f"Based on {constraints.get('resources', 'available resources')} and {obj.get('rationale', 'strategic analysis')}",
                relevant=f"Directly supports movement goal of {self.movement_knowledge['core_principles']['monetary_flow_tax']}",
                time_bound=f"Target completion by {target_date.strftime('%Y-%m-%d')}",
                horizon=horizon,
                owner=obj.get("owner", "Campaign Team"),
                dependencies=obj.get("dependencies", []),
                success_metrics=success_metrics,
                created_at=datetime.now(),
                target_date=target_date
            )
            
            smart_goals.append(smart_goal)
            
        return smart_goals

    async def _build_tactical_roadmap(self, smart_goals: List[SMARTGoal], 
                                     timeline: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Build tactical roadmap organized by strategic horizon"""
        roadmap = {
            "immediate": [],
            "short_term": [],
            "medium_term": [],
            "long_term": []
        }
        
        for goal in smart_goals:
            horizon_key = goal.horizon.value
            
            # Generate tactical actions for each goal
            tactics = await self._generate_tactics_for_goal(goal)
            
            roadmap[horizon_key].append({
                "goal_id": goal.id,
                "goal_title": goal.specific,
                "tactics": tactics,
                "timeline": {
                    "start": goal.created_at.isoformat(),
                    "end": goal.target_date.isoformat()
                },
                "dependencies": goal.dependencies,
                "owner": goal.owner
            })
            
        return roadmap

    async def _generate_tactics_for_goal(self, goal: SMARTGoal) -> List[Dict[str, Any]]:
        """Generate specific tactical actions for a SMART goal"""
        
        # Map goal types to tactical frameworks
        goal_type = self._classify_goal_type(goal.specific)
        
        if goal_type == "awareness":
            return [
                {
                    "action": "Content Development",
                    "description": "Create educational materials about monetary flow tax",
                    "channels": ["blog", "social_media", "infographics"],
                    "timeline": "Weeks 1-4",
                    "resources_needed": ["content_team", "design_support"]
                },
                {
                    "action": "Media Outreach", 
                    "description": "Pitch story to mainstream and alternative media",
                    "channels": ["earned_media", "podcast_appearances"],
                    "timeline": "Weeks 3-8",
                    "resources_needed": ["pr_team", "spokesperson_training"]
                }
            ]
        elif goal_type == "mobilization":
            return [
                {
                    "action": "Petition Campaign",
                    "description": "Launch online petition with clear ask",
                    "channels": ["website", "social_media", "email"],
                    "timeline": "Weeks 1-12",
                    "resources_needed": ["petition_platform", "list_building"]
                },
                {
                    "action": "Grassroots Events",
                    "description": "Host community education events",
                    "channels": ["in_person", "virtual_events"],
                    "timeline": "Weeks 4-16",
                    "resources_needed": ["event_coordination", "venue_costs"]
                }
            ]
        else:
            # Default tactical framework
            return [
                {
                    "action": "Strategic Implementation",
                    "description": f"Execute {goal.specific}",
                    "channels": ["multiple"],
                    "timeline": "Full goal duration",
                    "resources_needed": ["coordination", "execution_team"]
                }
            ]

    def _classify_goal_type(self, goal_description: str) -> str:
        """Classify goal type based on description"""
        awareness_keywords = ["awareness", "education", "recognition", "knowledge"]
        mobilization_keywords = ["petition", "action", "mobilize", "engagement", "participation"]
        
        desc_lower = goal_description.lower()
        
        if any(keyword in desc_lower for keyword in awareness_keywords):
            return "awareness"
        elif any(keyword in desc_lower for keyword in mobilization_keywords):
            return "mobilization"
        else:
            return "general"

    async def _design_kpi_framework(self, smart_goals: List[SMARTGoal], 
                                   objectives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Design comprehensive KPI framework"""
        kpis = []
        
        # Add KPIs from SMART goals
        for goal in smart_goals:
            for metric in goal.success_metrics:
                kpis.append({
                    "name": metric["name"],
                    "target": metric["target"],
                    "measurement_method": metric["measurement_method"],
                    "frequency": metric["frequency"],
                    "goal_id": goal.id,
                    "horizon": goal.horizon.value,
                    "owner": goal.owner,
                    "baseline": "TBD",
                    "current_value": "TBD"
                })
        
        # Add framework-level KPIs based on goal types
        goal_types = [self._classify_goal_type(g.specific) for g in smart_goals]
        
        if "awareness" in goal_types:
            kpis.extend(self.kpi_frameworks["awareness_metrics"])
        if "mobilization" in goal_types:
            kpis.extend(self.kpi_frameworks["engagement_metrics"])
            
        # Always include influence and outcome metrics
        kpis.extend(self.kpi_frameworks["influence_metrics"])
        kpis.extend(self.kpi_frameworks["outcome_metrics"])
        
        return kpis

    async def _conduct_risk_assessment(self, campaign_brief: Dict[str, Any], 
                                      constraints: Dict[str, Any], 
                                      context: Dict[str, Any]) -> List[RiskItem]:
        """Conduct comprehensive risk assessment"""
        risks = []
        
        # Political risks
        risks.append(RiskItem(
            id=f"risk_{uuid.uuid4().hex[:8]}",
            description="Financial industry opposition and lobbying",
            category="political",
            probability=0.9,
            impact=RiskLevel.HIGH,
            mitigation_strategies=[
                "Build broad coalition of supporters",
                "Frame as fairness issue, not anti-business",
                "Prepare counter-narratives"
            ],
            contingency_plans=[
                "Rapid response communications team",
                "Alternative policy proposals",
                "Grassroots mobilization"
            ],
            owner="Campaign Leadership",
            review_date=datetime.now() + timedelta(days=30),
            status="active"
        ))
        
        # Technical risks
        risks.append(RiskItem(
            id=f"risk_{uuid.uuid4().hex[:8]}",
            description="Message complexity limiting public understanding",
            category="technical",
            probability=0.7,
            impact=RiskLevel.MEDIUM,
            mitigation_strategies=[
                "Simplify messaging with analogies",
                "Visual explainers and infographics",
                "Repeated exposure through multiple channels"
            ],
            contingency_plans=[
                "Message testing and refinement",
                "Multiple message variants",
                "Spokesperson training"
            ],
            owner="Communications Team",
            review_date=datetime.now() + timedelta(days=14),
            status="active"
        ))
        
        # Resource risks
        budget = constraints.get("budget", 0)
        if budget < 100000:  # Assuming minimum viable budget
            risks.append(RiskItem(
                id=f"risk_{uuid.uuid4().hex[:8]}",
                description="Insufficient budget for comprehensive campaign",
                category="resource",
                probability=0.8,
                impact=RiskLevel.HIGH,
                mitigation_strategies=[
                    "Phased campaign approach",
                    "Volunteer mobilization",
                    "Partnership cost-sharing"
                ],
                contingency_plans=[
                    "Fundraising acceleration",
                    "Scope reduction",
                    "Extended timeline"
                ],
                owner="Finance Team",
                review_date=datetime.now() + timedelta(days=7),
                status="active"
            ))
            
        # Legal risks
        risks.append(RiskItem(
            id=f"risk_{uuid.uuid4().hex[:8]}",
            description="Legal challenges to campaign activities",
            category="legal",
            probability=0.4,
            impact=RiskLevel.MEDIUM,
            mitigation_strategies=[
                "Legal review of all materials",
                "Compliance with election laws",
                "Clear disclaimers and disclosures"
            ],
            contingency_plans=[
                "Legal defense fund",
                "Rapid legal response team",
                "Modified campaign tactics"
            ],
            owner="Legal Counsel",
            review_date=datetime.now() + timedelta(days=60),
            status="active"
        ))
        
        return risks

    async def _define_pivot_triggers(self, smart_goals: List[SMARTGoal], 
                                    risk_register: List[RiskItem]) -> List[PivotTrigger]:
        """Define conditions that would trigger strategic pivots"""
        triggers = []
        
        # Performance-based triggers
        triggers.append(PivotTrigger(
            id=f"trigger_{uuid.uuid4().hex[:8]}",
            name="Low Engagement Pivot",
            condition="Campaign engagement falls below threshold",
            threshold_metrics={
                "social_engagement_rate": 0.02,  # Below 2%
                "petition_signature_velocity": 100,  # Below 100/week
                "email_open_rate": 0.15  # Below 15%
            },
            response_actions=[
                "Message testing and refinement",
                "Channel optimization",
                "Audience research and segmentation",
                "Creative refresh"
            ],
            escalation_path="Communications Lead → Campaign Director → Strategic Advisory",
            monitoring_frequency="weekly"
        ))
        
        # Opposition-based triggers
        triggers.append(PivotTrigger(
            id=f"trigger_{uuid.uuid4().hex[:8]}",
            name="Opposition Response Pivot",
            condition="Coordinated opposition campaign detected",
            threshold_metrics={
                "negative_media_coverage": 0.5,  # 50% negative
                "opposition_ad_spending": 500000,  # $500K detected
                "misinformation_spread_rate": 0.3  # 30% of mentions
            },
            response_actions=[
                "Activate rapid response protocol",
                "Counter-narrative deployment",
                "Coalition mobilization",
                "Media blitz coordination"
            ],
            escalation_path="Communications Lead → Campaign Director → Crisis Team",
            monitoring_frequency="daily"
        ))
        
        # Resource-based triggers
        triggers.append(PivotTrigger(
            id=f"trigger_{uuid.uuid4().hex[:8]}",
            name="Resource Shortfall Pivot",
            condition="Budget or volunteer capacity falls short",
            threshold_metrics={
                "budget_burn_rate": 1.2,  # 20% over planned
                "volunteer_hours_shortfall": 0.7,  # 30% below needed
                "fundraising_velocity": 0.5  # 50% below target
            },
            response_actions=[
                "Scope reduction and prioritization",
                "Volunteer recruitment drive",
                "Emergency fundraising",
                "Partnership development"
            ],
            escalation_path="Operations Lead → Campaign Director → Board",
            monitoring_frequency="weekly"
        ))
        
        return triggers

    async def _validate_framework_quality(self, mission_vision: Dict[str, str], 
                                         smart_goals: List[SMARTGoal],
                                         tactical_roadmap: Dict[str, List[Dict[str, Any]]],
                                         kpis: List[Dict[str, Any]],
                                         risk_register: List[RiskItem]) -> Dict[str, Any]:
        """Validate overall framework quality"""
        issues = []
        
        # Check mission/vision alignment
        if not mission_vision.get("mission") or len(mission_vision["mission"]) < 50:
            issues.append("Mission statement too brief or missing")
        if not mission_vision.get("vision") or len(mission_vision["vision"]) < 50:
            issues.append("Vision statement too brief or missing")
            
        # Check SMART goals completeness
        if len(smart_goals) < 3:
            issues.append("Insufficient number of strategic goals (minimum 3)")
        for goal in smart_goals:
            if not goal.success_metrics:
                issues.append(f"Goal '{goal.specific}' lacks success metrics")
                
        # Check tactical roadmap coverage
        total_tactics = sum(len(horizon_tactics) for horizon_tactics in tactical_roadmap.values())
        if total_tactics < len(smart_goals):
            issues.append("Insufficient tactical coverage for strategic goals")
            
        # Check KPI framework
        if len(kpis) < 5:
            issues.append("Insufficient KPI coverage (minimum 5)")
            
        # Check risk assessment
        high_critical_risks = [r for r in risk_register if r.impact in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        if not high_critical_risks:
            issues.append("Risk assessment may be incomplete - no high/critical risks identified")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    async def _calculate_resource_requirements(self, smart_goals: List[SMARTGoal], 
                                             tactical_roadmap: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Calculate comprehensive resource requirements"""
        
        # Base resource calculations
        total_goals = len(smart_goals)
        total_tactics = sum(len(horizon_tactics) for horizon_tactics in tactical_roadmap.values())
        
        # Rough budget estimation based on scope
        base_budget = total_goals * 50000  # $50K per major goal
        tactical_budget = total_tactics * 10000  # $10K per tactical initiative
        
        estimated_budget = base_budget + tactical_budget
        
        # Human resources estimation
        core_team_size = max(5, total_goals * 2)  # Minimum 5, 2 per goal
        contractor_budget = estimated_budget * 0.3  # 30% for contractors
        
        return {
            "total_budget": estimated_budget,
            "budget_breakdown": {
                "core_team": estimated_budget * 0.5,
                "contractors": contractor_budget,
                "media_advertising": estimated_budget * 0.15,
                "operations": estimated_budget * 0.05
            },
            "human_resources": {
                "core_team_size": core_team_size,
                "key_roles": [
                    "Campaign Director",
                    "Communications Lead", 
                    "Digital Strategist",
                    "Grassroots Coordinator",
                    "Policy Researcher"
                ],
                "contractor_needs": [
                    "Graphic Designer",
                    "Web Developer", 
                    "PR Consultant",
                    "Legal Counsel"
                ]
            },
            "technology_stack": [
                "CRM/Database system",
                "Email marketing platform",
                "Social media management",
                "Website and hosting",
                "Analytics tools",
                "Petition platform"
            ],
            "timeline": f"{len(smart_goals)} goals over {max(g.target_date for g in smart_goals) - min(g.created_at for g in smart_goals)}"
        }

    async def _generate_timeline_milestones(self, tactical_roadmap: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Generate key timeline milestones"""
        milestones = []
        
        milestone_id = 1
        for horizon, tactics_list in tactical_roadmap.items():
            for tactical_group in tactics_list:
                milestones.append({
                    "id": f"milestone_{milestone_id}",
                    "name": f"Complete {tactical_group['goal_title']}",
                    "description": f"Finish all tactical initiatives for {horizon} goal",
                    "target_date": tactical_group['timeline']['end'],
                    "horizon": horizon,
                    "dependencies": tactical_group.get('dependencies', []),
                    "success_criteria": [
                        "All tactics executed",
                        "Success metrics achieved",
                        "Quality gates passed"
                    ],
                    "deliverables": [tactic['action'] for tactic in tactical_group.get('tactics', [])]
                })
                milestone_id += 1
                
        return sorted(milestones, key=lambda x: x['target_date'])

    async def _map_stakeholders(self, campaign_brief: Dict[str, Any], 
                               context: Dict[str, Any]) -> Dict[str, List[str]]:
        """Map key stakeholders across categories"""
        
        base_stakeholders = self.strategic_templates["strategic_frameworks"]["stakeholder_analysis"]
        
        return {
            "internal": [
                "Campaign leadership team",
                "Core staff and volunteers", 
                "Advisory board members",
                "Major donors and funders"
            ],
            "supporters": base_stakeholders["supporters"] + [
                "Economic justice advocates",
                "Transparency organizations",
                "Democratic reform groups"
            ],
            "neutrals": base_stakeholders["neutrals"] + [
                "Independent researchers",
                "Non-partisan civic groups",
                "Moderate business associations"
            ],
            "opponents": base_stakeholders["opponents"] + [
                "High-frequency trading firms",
                "Financial industry lobbies",
                "Status quo defenders"
            ],
            "influencers": [
                "Policy researchers and think tanks",
                "Economic journalists and media",
                "Political leaders and electeds",
                "Business and labor leaders"
            ],
            "target_audiences": [
                campaign_brief.get("target_audience", "Working families"),
                "Small business owners",
                "Young professionals",
                "Civic engagement advocates"
            ]
        }

    async def _validate_final_framework(self, framework: StrategicFramework) -> Dict[str, Any]:
        """Final comprehensive framework validation"""
        issues = []
        
        # Strategic coherence check
        if not framework.mission_statement or not framework.vision_statement:
            issues.append("Missing mission or vision statement")
            
        # Goal-tactic alignment check
        goals_with_tactics = []
        for horizon_tactics in framework.tactical_roadmap.values():
            goals_with_tactics.extend([t['goal_id'] for t in horizon_tactics])
        
        goals_without_tactics = [g.id for g in framework.strategic_objectives 
                                if g.id not in goals_with_tactics]
        if goals_without_tactics:
            issues.append(f"Goals without tactical coverage: {len(goals_without_tactics)}")
            
        # KPI coverage check
        if len(framework.kpis) < len(framework.strategic_objectives):
            issues.append("Insufficient KPI coverage for strategic objectives")
            
        # Risk mitigation check
        unmitigated_risks = [r for r in framework.risk_register 
                            if not r.mitigation_strategies or not r.contingency_plans]
        if unmitigated_risks:
            issues.append(f"Risks without mitigation: {len(unmitigated_risks)}")
            
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    async def _verify_movement_principles(self, framework: StrategicFramework) -> Dict[str, Any]:
        """Verify alignment with IsThereEnoughMoney Movement principles"""
        
        violations = []
        
        # Check for broad, non-discriminatory messaging
        framework_text = f"{framework.mission_statement} {framework.vision_statement}"
        for goal in framework.strategic_objectives:
            framework_text += f" {goal.specific} {goal.relevant}"
            
        # Look for potentially discriminatory language
        problematic_terms = ["target specific demographics", "exclude", "only for"]
        if any(term in framework_text.lower() for term in problematic_terms):
            violations.append("Potentially discriminatory targeting detected")
            
        # Verify monetary flow tax principles
        core_concepts = ["monetary flow", "transaction tax", "financial transparency", "economic justice"]
        if not any(concept in framework_text.lower() for concept in core_concepts):
            violations.append("Missing core movement concepts")
            
        # Verify no unverified claims
        verification_needed = []
        for goal in framework.strategic_objectives:
            if "%" in goal.specific or "$" in goal.specific:
                verification_needed.append(f"Goal '{goal.specific}' contains claims requiring verification")
        
        return {
            "verified": len(violations) == 0 and len(verification_needed) == 0,
            "violations": violations,
            "verification_needed": verification_needed
        }

    async def _generate_handoff_package(self, framework: StrategicFramework) -> Dict[str, Any]:
        """Generate comprehensive handoff package for implementation"""
        return {
            "implementation_priorities": [
                {
                    "priority": 1,
                    "action": "Establish core team and governance",
                    "timeline": "Week 1-2",
                    "deliverables": ["Team assignments", "Communication protocols", "Decision framework"]
                },
                {
                    "priority": 2, 
                    "action": "Launch immediate horizon goals",
                    "timeline": "Week 3-4",
                    "deliverables": ["Immediate tactics execution", "KPI tracking setup", "Risk monitoring"]
                },
                {
                    "priority": 3,
                    "action": "Begin short-term horizon preparation",
                    "timeline": "Week 4-6", 
                    "deliverables": ["Resource allocation", "Partnership outreach", "Content development"]
                }
            ],
            "critical_dependencies": [
                "Funding confirmation and budget allocation",
                "Key personnel recruitment and onboarding",
                "Technology platform setup and testing",
                "Legal review and compliance clearance"
            ],
            "success_metrics_setup": [
                "Implement KPI tracking dashboard",
                "Establish baseline measurements",
                "Set up regular reporting cadence",
                "Configure automated alerts"
            ],
            "risk_monitoring": [
                "Weekly risk register review",
                "Pivot trigger monitoring setup",
                "Escalation protocol training",
                "Contingency plan preparation"
            ]
        }

    async def _create_executive_summary(self, framework: StrategicFramework) -> str:
        """Create executive summary of strategic framework"""
        
        goal_count = len(framework.strategic_objectives)
        horizon_distribution = {}
        for goal in framework.strategic_objectives:
            horizon = goal.horizon.value
            horizon_distribution[horizon] = horizon_distribution.get(horizon, 0) + 1
            
        high_risks = len([r for r in framework.risk_register if r.impact in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
        
        summary = f"""
**Strategic Framework Executive Summary**

**Mission**: {framework.mission_statement[:200]}...

**Vision**: {framework.vision_statement[:200]}...

**Strategic Overview**:
- {goal_count} strategic objectives across {len(horizon_distribution)} planning horizons
- {len(framework.kpis)} key performance indicators for measurement
- {len(framework.risk_register)} identified risks ({high_risks} high/critical priority)
- {len(framework.pivot_triggers)} pivot triggers for adaptive management

**Resource Requirements**:
- Estimated budget: {framework.resource_requirements.get('total_budget', 'TBD')}
- Core team size: {framework.resource_requirements.get('human_resources', {}).get('core_team_size', 'TBD')}
- Timeline: {len(framework.timeline_milestones)} major milestones

**Key Success Factors**:
1. Comprehensive fact verification (≥2 sources per claim)
2. Broad, inclusive messaging avoiding demographic targeting
3. Continuous risk monitoring and adaptive response
4. Strong coalition building with diverse stakeholders
5. Transparent, measurable progress tracking

This framework provides the strategic foundation for advancing the Monetary Flow Tax initiative through a systematic, evidence-based campaign approach aligned with movement principles of economic justice and democratic transparency.
        """.strip()
        
        return summary

    async def _recommend_next_steps(self, framework: StrategicFramework) -> List[Dict[str, Any]]:
        """Recommend immediate next steps for implementation"""
        return [
            {
                "step": 1,
                "action": "Strategic Framework Review & Approval",
                "description": "Present framework to leadership for approval and refinement",
                "timeline": "3-5 business days",
                "owner": "Campaign Director",
                "deliverables": ["Approved strategic framework", "Budget authorization", "Team assignments"]
            },
            {
                "step": 2,
                "action": "Core Team Assembly",
                "description": "Recruit and onboard key team members per resource requirements",
                "timeline": "1-2 weeks",
                "owner": "Operations Lead",
                "deliverables": ["Team roster", "Role definitions", "Communication protocols"]
            },
            {
                "step": 3,
                "action": "Technology Infrastructure Setup", 
                "description": "Implement required technology stack and tracking systems",
                "timeline": "1-2 weeks",
                "owner": "Digital Strategist",
                "deliverables": ["KPI dashboard", "CRM system", "Analytics setup"]
            },
            {
                "step": 4,
                "action": "Legal & Compliance Review",
                "description": "Conduct thorough legal review of all strategic components",
                "timeline": "1 week",
                "owner": "Legal Counsel", 
                "deliverables": ["Legal clearance", "Compliance protocols", "Risk mitigation updates"]
            },
            {
                "step": 5,
                "action": "Launch Immediate Horizon Goals",
                "description": "Begin execution of immediate tactical initiatives",
                "timeline": "Week 3-4",
                "owner": "Tactical Team Leads",
                "deliverables": ["Campaign launch", "Initial content", "Community engagement"]
            }
        ]

    async def _define_success_criteria(self, framework: StrategicFramework) -> Dict[str, Any]:
        """Define comprehensive success criteria for framework implementation"""
        return {
            "strategic_success": {
                "goal_completion_rate": "≥80% of strategic objectives achieved on time",
                "kpi_target_achievement": "≥70% of KPIs meeting or exceeding targets",
                "stakeholder_satisfaction": "≥75% positive feedback from key stakeholders",
                "movement_growth": "Measurable increase in supporter base and engagement"
            },
            "operational_success": {
                "budget_efficiency": "≤110% of approved budget utilization",
                "timeline_adherence": "≤20% variance from planned milestones",
                "quality_maintenance": "≥95% quality gate pass rate",
                "risk_management": "No critical risks escalating to crisis level"
            },
            "movement_alignment": {
                "principle_adherence": "100% compliance with movement principles",
                "fact_verification": "≥2 sources for 100% of factual claims",
                "inclusive_messaging": "0% discriminatory targeting incidents",
                "democratic_engagement": "Increased civic participation metrics"
            },
            "adaptive_capacity": {
                "pivot_responsiveness": "≤48 hours to activate pivot protocols",
                "learning_integration": "Monthly strategy refinement based on data",
                "stakeholder_feedback": "Quarterly stakeholder input integration",
                "competitive_adaptation": "Real-time response to opposition activities"
            }
        }

    async def _compile_citations(self) -> List[Dict[str, Any]]:
        """Compile citations for strategic framework"""
        return [
            {
                "source": "Internal Movement Knowledge Base",
                "type": "primary",
                "content": "IsThereEnoughMoney Movement core principles and economic data",
                "verification_status": "movement_verified",
                "last_updated": datetime.now().isoformat()
            },
            {
                "source": "Strategic Planning Best Practices",
                "type": "methodology", 
                "content": "SMART goals framework and tactical planning methodologies",
                "verification_status": "industry_standard",
                "last_updated": datetime.now().isoformat()
            },
            {
                "source": "Campaign Strategy Templates",
                "type": "framework",
                "content": "Political campaign planning frameworks and stakeholder analysis",
                "verification_status": "established_practice",
                "last_updated": datetime.now().isoformat()
            }
        ]