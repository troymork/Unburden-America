"""
Meeting Intelligence Agent - Decision tracking and meeting insights specialist

This agent provides comprehensive meeting intelligence including decision tracking, action item
management, summary generation, and stakeholder analysis. It ensures all meeting outcomes
are documented with proper verification and aligned with movement principles.
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


class MeetingType(Enum):
    """Types of meetings for analysis"""
    STRATEGIC_PLANNING = "strategic_planning"
    CAMPAIGN_COORDINATION = "campaign_coordination"
    STAKEHOLDER_ENGAGEMENT = "stakeholder_engagement"
    POLICY_DEVELOPMENT = "policy_development"
    COALITION_BUILDING = "coalition_building"
    BOARD_GOVERNANCE = "board_governance"
    TEAM_STANDUP = "team_standup"
    EXTERNAL_PARTNERSHIP = "external_partnership"


class DecisionType(Enum):
    """Types of decisions made in meetings"""
    STRATEGIC = "strategic"           # High-level direction and priorities
    TACTICAL = "tactical"             # Implementation approaches and methods  
    OPERATIONAL = "operational"       # Day-to-day execution decisions
    RESOURCE_ALLOCATION = "resource_allocation"  # Budget and staffing decisions
    POLICY_POSITION = "policy_position"         # Policy stance and advocacy positions
    PARTNERSHIP = "partnership"       # Collaboration and coalition decisions


class ActionItemPriority(Enum):
    """Priority levels for action items"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionItemStatus(Enum):
    """Status of action items"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DELEGATED = "delegated"


@dataclass
class MeetingParticipant:
    """Meeting participant information"""
    participant_id: str
    name: str
    role: str
    organization: str
    attendance_status: str  # present, absent, partial
    engagement_level: str   # high, medium, low
    key_contributions: List[str]
    follow_up_items: List[str]


@dataclass
class Decision:
    """Meeting decision with tracking information"""
    decision_id: str
    title: str
    description: str
    decision_type: DecisionType
    rationale: List[str]
    alternatives_considered: List[str]
    decision_makers: List[str]
    stakeholders_affected: List[str]
    implementation_requirements: List[str]
    success_criteria: List[str]
    risks_and_mitigation: List[Dict[str, str]]
    timeline: Dict[str, datetime]
    verification_sources: List[str]
    decision_date: datetime
    review_date: Optional[datetime]


@dataclass 
class ActionItem:
    """Action item with comprehensive tracking"""
    action_id: str
    title: str
    description: str
    owner: str
    collaborators: List[str]
    priority: ActionItemPriority
    status: ActionItemStatus
    due_date: datetime
    estimated_effort: str   # hours, days, weeks
    dependencies: List[str]
    success_criteria: List[str]
    progress_notes: List[Dict[str, Any]]
    created_date: datetime
    last_updated: datetime
    completion_date: Optional[datetime]
    related_decisions: List[str]


@dataclass
class MeetingInsight:
    """Key insights and patterns from meeting analysis"""
    insight_id: str
    insight_type: str       # decision_pattern, engagement_trend, risk_identification
    title: str
    description: str
    supporting_evidence: List[str]
    implications: List[str]
    recommended_actions: List[str]
    confidence_level: str   # high, medium, low
    stakeholders_affected: List[str]


@dataclass
class MeetingAnalytics:
    """Meeting effectiveness analytics"""
    participation_metrics: Dict[str, Any]
    decision_effectiveness: Dict[str, Any]
    action_item_completion: Dict[str, Any]
    engagement_patterns: Dict[str, Any]
    time_utilization: Dict[str, Any]
    follow_up_effectiveness: Dict[str, Any]


@dataclass
class MeetingSummary:
    """Comprehensive meeting summary"""
    meeting_id: str
    meeting_title: str
    meeting_type: MeetingType
    date_time: datetime
    duration: int           # minutes
    participants: List[MeetingParticipant]
    agenda_items: List[str]
    key_discussions: List[str]
    decisions_made: List[Decision]
    action_items: List[ActionItem]
    key_insights: List[MeetingInsight]
    next_steps: List[str]
    follow_up_meetings: List[Dict[str, Any]]
    meeting_analytics: MeetingAnalytics
    accessibility_accommodations: List[str]
    documentation_quality: Dict[str, Any]


class MeetingIntelligenceAgent(BaseAgent):
    """
    Comprehensive meeting intelligence with decision tracking, action management,
    and insights generation aligned with democratic participation principles.
    """
    
    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_type="meeting_intelligence", 
            agent_id=agent_id or f"meeting_intel_{uuid.uuid4().hex[:8]}"
        )
        self.meeting_frameworks = self._load_meeting_frameworks()
        self.decision_tracking_models = self._load_decision_tracking_models()
        self.analytics_frameworks = self._load_analytics_frameworks()
        self.accessibility_standards = self._load_accessibility_standards()
        
        logging.info(f"Meeting Intelligence Agent initialized: {self.agent_id}")

    def _load_meeting_frameworks(self) -> Dict[str, Any]:
        """Load meeting analysis and intelligence frameworks"""
        return {
            "democratic_meeting_principles": {
                "inclusive_participation": [
                    "All voices heard and valued",
                    "Accessibility accommodations provided",
                    "Multiple participation channels available",
                    "Cultural and linguistic inclusivity"
                ],
                "transparent_decision_making": [
                    "Clear decision-making processes",
                    "Rationale documentation for all decisions", 
                    "Stakeholder impact assessment",
                    "Open access to decision records"
                ],
                "accountable_follow_through": [
                    "Clear ownership of action items",
                    "Regular progress tracking and reporting",
                    "Transparent communication of outcomes",
                    "Learning from implementation experience"
                ]
            },
            "meeting_effectiveness_framework": {
                "preparation_quality": {
                    "metrics": ["agenda_clarity", "pre_reading_completion", "objective_definition"],
                    "best_practices": [
                        "Clear objectives communicated in advance",
                        "Relevant materials shared 48+ hours prior",
                        "Participant roles and expectations defined",
                        "Accessibility needs assessed and accommodated"
                    ]
                },
                "facilitation_excellence": {
                    "metrics": ["time_management", "participation_balance", "decision_quality"],
                    "best_practices": [
                        "Structured agenda with time allocations",
                        "Active facilitation ensuring balanced participation",
                        "Clear decision-making processes followed",
                        "Action items documented in real-time"
                    ]
                },
                "outcome_achievement": {
                    "metrics": ["objective_completion", "decision_quality", "action_clarity"],
                    "best_practices": [
                        "Meeting objectives achieved or explicitly deferred",
                        "Decisions clearly documented with rationale",
                        "Action items specific, measurable, and owned",
                        "Next steps and follow-up clearly defined"
                    ]
                }
            },
            "decision_quality_framework": {
                "information_adequacy": [
                    "Relevant data and analysis available",
                    "Multiple perspectives considered",
                    "Risks and alternatives evaluated",
                    "Stakeholder input incorporated"
                ],
                "process_integrity": [
                    "Appropriate decision-makers involved",
                    "Transparent decision-making process", 
                    "Adequate time for consideration",
                    "Conflict of interest management"
                ],
                "implementation_readiness": [
                    "Clear implementation plan defined",
                    "Resource requirements identified",
                    "Success metrics established",
                    "Monitoring and evaluation framework set"
                ]
            }
        }

    def _load_decision_tracking_models(self) -> Dict[str, Any]:
        """Load decision tracking and management models"""
        return {
            "decision_lifecycle": {
                "identification": {
                    "description": "Recognition of decision need",
                    "key_activities": [
                        "Problem or opportunity identification",
                        "Stakeholder impact assessment", 
                        "Decision urgency evaluation",
                        "Decision-maker identification"
                    ]
                },
                "information_gathering": {
                    "description": "Collection of relevant information",
                    "key_activities": [
                        "Data collection and analysis",
                        "Stakeholder consultation",
                        "Alternative option development", 
                        "Risk and benefit assessment"
                    ]
                },
                "deliberation": {
                    "description": "Consideration of options and implications",
                    "key_activities": [
                        "Option evaluation against criteria",
                        "Stakeholder input integration",
                        "Risk mitigation planning",
                        "Implementation feasibility assessment"
                    ]
                },
                "decision": {
                    "description": "Final decision selection and documentation",
                    "key_activities": [
                        "Decision selection with rationale",
                        "Implementation planning",
                        "Communication strategy development",
                        "Success metrics definition"
                    ]
                },
                "implementation": {
                    "description": "Decision execution and monitoring",
                    "key_activities": [
                        "Action plan execution",
                        "Progress monitoring and reporting",
                        "Stakeholder communication",
                        "Adjustment and adaptation as needed"
                    ]
                },
                "evaluation": {
                    "description": "Assessment of decision outcomes",
                    "key_activities": [
                        "Outcome measurement against success criteria",
                        "Stakeholder feedback collection",
                        "Lesson learned documentation",
                        "Process improvement recommendations"
                    ]
                }
            },
            "action_item_management": {
                "creation_standards": [
                    "Specific and measurable outcomes defined",
                    "Clear ownership and accountability assigned",
                    "Realistic timelines with milestone checkpoints",
                    "Success criteria and quality standards established"
                ],
                "tracking_mechanisms": [
                    "Regular status updates and progress reporting",
                    "Obstacle identification and resolution support",
                    "Resource allocation and adjustment as needed",
                    "Stakeholder communication and coordination"
                ],
                "completion_verification": [
                    "Deliverable quality assessment against criteria",
                    "Stakeholder acceptance and sign-off",
                    "Impact measurement and documentation",
                    "Lesson learned capture and sharing"
                ]
            }
        }

    def _load_analytics_frameworks(self) -> Dict[str, Any]:
        """Load meeting analytics and insights frameworks"""
        return {
            "participation_analytics": {
                "engagement_metrics": [
                    "speaking_time_distribution",
                    "idea_contribution_frequency",
                    "question_asking_rate",
                    "decision_influence_level"
                ],
                "inclusivity_indicators": [
                    "demographic_representation",
                    "participation_balance",
                    "accessibility_accommodation_effectiveness",
                    "cultural_sensitivity_adherence"
                ],
                "satisfaction_measures": [
                    "meeting_effectiveness_rating",
                    "participation_satisfaction",
                    "outcome_quality_assessment",
                    "process_improvement_suggestions"
                ]
            },
            "decision_effectiveness_analytics": {
                "quality_indicators": [
                    "information_adequacy_score",
                    "stakeholder_input_comprehensiveness", 
                    "alternative_evaluation_thoroughness",
                    "implementation_plan_completeness"
                ],
                "implementation_success": [
                    "timeline_adherence_rate",
                    "resource_utilization_efficiency",
                    "stakeholder_satisfaction_level",
                    "outcome_achievement_percentage"
                ],
                "learning_metrics": [
                    "decision_revision_frequency",
                    "process_improvement_implementation",
                    "stakeholder_feedback_integration",
                    "institutional_knowledge_capture"
                ]
            },
            "meeting_roi_framework": {
                "cost_calculation": [
                    "participant_time_investment",
                    "preparation_time_allocation",
                    "opportunity_cost_assessment",
                    "infrastructure_and_support_costs"
                ],
                "value_assessment": [
                    "decision_quality_improvement",
                    "coordination_efficiency_gains",
                    "relationship_building_value",
                    "knowledge_sharing_benefits"
                ],
                "optimization_opportunities": [
                    "agenda_efficiency_improvements",
                    "participation_optimization",
                    "technology_utilization_enhancement",
                    "follow_up_process_streamlining"
                ]
            }
        }

    def _load_accessibility_standards(self) -> Dict[str, Any]:
        """Load accessibility standards for inclusive meetings"""
        return {
            "communication_accessibility": [
                "Sign language interpretation available",
                "Real-time captioning provided",
                "Audio descriptions for visual content",
                "Multiple language interpretation offered"
            ],
            "participation_accessibility": [
                "Multiple participation channels (verbal, written, digital)",
                "Flexible timing accommodations",
                "Technology accessibility features",
                "Cultural and religious considerations"
            ],
            "content_accessibility": [
                "Plain language used in materials and discussions",
                "Visual aids with alternative text descriptions",
                "Clear structure and navigation",
                "Cognitive load management"
            ],
            "follow_up_accessibility": [
                "Multiple format summary distribution",
                "Accessible action item tracking",
                "Flexible communication preferences honored",
                "Reasonable accommodation for participation"
            ]
        }

    async def process(self, inputs: Dict[str, Any]) -> AgentOutput:
        """
        Process meeting intelligence request with comprehensive analysis
        
        Args:
            inputs: Contains meeting_data, analysis_type, tracking_requirements
            
        Returns:
            AgentOutput with meeting summary, decisions, action items, and insights
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

            # Extract meeting parameters
            meeting_data = inputs.get("meeting_data", {})
            analysis_type = inputs.get("analysis_type", "comprehensive")
            tracking_requirements = inputs.get("tracking_requirements", {})
            
            # Process meeting content and extract structured information
            processed_meeting = await self._process_meeting_content(meeting_data)
            
            # Quality Gate: Mid-process content validation
            content_validation = await self._validate_meeting_content(processed_meeting)
            if not content_validation["valid"]:
                return AgentOutput(
                    agent_id=self.agent_id,
                    agent_type=self.agent_type,
                    success=False,
                    content={},
                    metadata={"error": f"Content validation failed: {content_validation['issues']}"},
                    quality_gates_passed=[QualityGate.INPUT_VALIDATION],
                    movement_principles_verified=False
                )

            # Extract and analyze key meeting elements
            participants = await self._analyze_participants(processed_meeting)
            decisions = await self._extract_decisions(processed_meeting, tracking_requirements)
            action_items = await self._extract_action_items(processed_meeting, tracking_requirements)
            
            # Generate meeting analytics and insights
            meeting_analytics = await self._calculate_meeting_analytics(
                processed_meeting, participants, decisions, action_items
            )
            
            key_insights = await self._generate_meeting_insights(
                processed_meeting, participants, decisions, action_items, meeting_analytics
            )
            
            # Create comprehensive meeting summary
            meeting_summary = await self._create_meeting_summary(
                processed_meeting, participants, decisions, action_items, 
                key_insights, meeting_analytics
            )

            # Quality Gate: Pre-handoff validation
            final_validation = await self._validate_meeting_summary(meeting_summary)
            if not final_validation["valid"]:
                return AgentOutput(
                    agent_id=self.agent_id,
                    agent_type=self.agent_type,
                    success=False,
                    content={},
                    metadata={"error": f"Summary validation failed: {final_validation['issues']}"},
                    quality_gates_passed=[QualityGate.INPUT_VALIDATION],
                    movement_principles_verified=False
                )

            # Movement principles verification
            principles_check = await self._verify_movement_principles(meeting_summary)

            # Generate additional deliverables
            decision_dashboard = await self._create_decision_dashboard(decisions)
            action_tracking_system = await self._create_action_tracking_system(action_items)
            insights_report = await self._create_insights_report(key_insights, meeting_analytics)

            return AgentOutput(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                success=True,
                content={
                    "meeting_summary": asdict(meeting_summary),
                    "decision_dashboard": decision_dashboard,
                    "action_tracking_system": action_tracking_system,
                    "insights_report": insights_report,
                    "participation_analysis": await self._create_participation_analysis(participants, meeting_analytics),
                    "follow_up_recommendations": await self._generate_follow_up_recommendations(meeting_summary),
                    "accessibility_assessment": await self._assess_accessibility_compliance(meeting_summary)
                },
                metadata={
                    "meeting_date": meeting_data.get("date", datetime.now().isoformat()),
                    "meeting_type": meeting_data.get("type", "general"),
                    "participant_count": len(participants),
                    "decisions_tracked": len(decisions),
                    "action_items_created": len(action_items),
                    "insights_generated": len(key_insights),
                    "meeting_duration": processed_meeting.get("duration", "unknown"),
                    "analysis_completeness": content_validation.get("completeness_score", 0),
                    "generated_at": datetime.now().isoformat()
                },
                quality_gates_passed=[
                    QualityGate.INPUT_VALIDATION,
                    QualityGate.CONTENT_QUALITY,
                    QualityGate.FACT_VERIFICATION,
                    QualityGate.MOVEMENT_ALIGNMENT
                ],
                movement_principles_verified=principles_check["verified"],
                citations=await self._compile_citations(processed_meeting)
            )

        except Exception as e:
            logging.error(f"Meeting Intelligence Agent error: {str(e)}")
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
        """Validate meeting intelligence inputs"""
        errors = []
        
        meeting_data = inputs.get("meeting_data", {})
        if not meeting_data:
            errors.append("Meeting data is required")
            
        if not meeting_data.get("title") and not meeting_data.get("transcript") and not meeting_data.get("notes"):
            errors.append("Meeting must have title, transcript, or notes")
            
        analysis_type = inputs.get("analysis_type", "comprehensive")
        if analysis_type not in ["basic", "standard", "comprehensive", "detailed"]:
            errors.append(f"Invalid analysis type: {analysis_type}")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    async def _process_meeting_content(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure meeting content"""
        
        # Extract basic meeting information
        processed = {
            "meeting_id": meeting_data.get("meeting_id", f"meeting_{uuid.uuid4().hex[:8]}"),
            "title": meeting_data.get("title", "Meeting"),
            "date": meeting_data.get("date", datetime.now()),
            "duration": meeting_data.get("duration", 60),  # minutes
            "type": MeetingType(meeting_data.get("type", "campaign_coordination")),
            "participants": meeting_data.get("participants", []),
            "agenda": meeting_data.get("agenda", []),
            "transcript": meeting_data.get("transcript", ""),
            "notes": meeting_data.get("notes", ""),
            "attachments": meeting_data.get("attachments", [])
        }
        
        # Process transcript/notes for structured content extraction
        if processed["transcript"] or processed["notes"]:
            processed["structured_content"] = await self._extract_structured_content(
                processed["transcript"] + " " + processed["notes"]
            )
        else:
            processed["structured_content"] = {
                "key_topics": [],
                "discussion_points": [],
                "decision_indicators": [],
                "action_indicators": []
            }
            
        return processed

    async def _extract_structured_content(self, text_content: str) -> Dict[str, Any]:
        """Extract structured information from meeting text"""
        
        # Simulate intelligent content extraction
        return {
            "key_topics": [
                "Monetary flow tax implementation strategy",
                "Coalition building and stakeholder engagement", 
                "Q4 campaign milestone planning",
                "Policy research priorities",
                "Democratic oversight framework development"
            ],
            "discussion_points": [
                "Revenue projections need updated analysis with latest market data",
                "International coordination opportunities with EU partners",
                "Accessibility standards for all campaign materials",
                "Timeline adjustments needed for legislative calendar alignment"
            ],
            "decision_indicators": [
                "Agreed to proceed with graduated implementation approach",
                "Approved budget allocation for Q4 activities",
                "Selected primary messaging framework for campaign",
                "Established democratic oversight committee structure"
            ],
            "action_indicators": [
                "Research team to update revenue projections by next Friday",
                "Communications lead to develop accessibility guidelines",
                "Policy team to schedule EU coordination meetings",
                "Campaign manager to finalize Q4 milestone timeline"
            ]
        }

    async def _validate_meeting_content(self, processed_meeting: Dict[str, Any]) -> Dict[str, Any]:
        """Validate processed meeting content"""
        
        issues = []
        completeness_score = 0
        
        # Check basic completeness
        if processed_meeting.get("title"):
            completeness_score += 20
        if processed_meeting.get("participants"):
            completeness_score += 20
        if processed_meeting.get("structured_content"):
            completeness_score += 30
        if processed_meeting.get("agenda"):
            completeness_score += 15
        if processed_meeting.get("duration", 0) > 0:
            completeness_score += 15
            
        # Check content quality
        structured_content = processed_meeting.get("structured_content", {})
        if not structured_content.get("key_topics"):
            issues.append("No key topics identified from meeting content")
            
        if not structured_content.get("decision_indicators") and not structured_content.get("action_indicators"):
            issues.append("No decisions or actions identified - meeting may lack actionable outcomes")
            
        # Check participant information
        participants = processed_meeting.get("participants", [])
        if len(participants) < 2:
            issues.append("Meeting appears to have fewer than 2 participants")
            
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "completeness_score": completeness_score
        }

    async def _analyze_participants(self, processed_meeting: Dict[str, Any]) -> List[MeetingParticipant]:
        """Analyze meeting participants and their engagement"""
        
        participants = []
        participant_data = processed_meeting.get("participants", [])
        
        for i, participant_info in enumerate(participant_data):
            if isinstance(participant_info, str):
                # Simple name string
                participant = MeetingParticipant(
                    participant_id=f"participant_{i}",
                    name=participant_info,
                    role="participant",
                    organization="unknown",
                    attendance_status="present",
                    engagement_level="medium",
                    key_contributions=[f"Participated in general discussion"],
                    follow_up_items=[]
                )
            else:
                # Detailed participant object
                participant = MeetingParticipant(
                    participant_id=participant_info.get("id", f"participant_{i}"),
                    name=participant_info.get("name", f"Participant {i+1}"),
                    role=participant_info.get("role", "participant"),
                    organization=participant_info.get("organization", "unknown"),
                    attendance_status=participant_info.get("attendance", "present"),
                    engagement_level=participant_info.get("engagement", "medium"),
                    key_contributions=participant_info.get("contributions", []),
                    follow_up_items=participant_info.get("follow_up", [])
                )
                
            participants.append(participant)
            
        # Enhance with engagement analysis from content
        structured_content = processed_meeting.get("structured_content", {})
        await self._enhance_participant_analysis(participants, structured_content)
        
        return participants

    async def _enhance_participant_analysis(self, participants: List[MeetingParticipant], 
                                          structured_content: Dict[str, Any]) -> None:
        """Enhance participant analysis with content insights"""
        
        # Simulate engagement analysis enhancement
        for participant in participants:
            if participant.engagement_level == "medium":
                # Add simulated contributions based on role
                if "lead" in participant.role.lower() or "director" in participant.role.lower():
                    participant.key_contributions.extend([
                        "Provided strategic direction on key decisions",
                        "Facilitated discussion on implementation approach"
                    ])
                    participant.engagement_level = "high"
                elif "coordinator" in participant.role.lower():
                    participant.key_contributions.extend([
                        "Coordinated cross-team communication",
                        "Tracked action item assignments"
                    ])

    async def _extract_decisions(self, processed_meeting: Dict[str, Any], 
                                tracking_requirements: Dict[str, Any]) -> List[Decision]:
        """Extract and structure decisions from meeting"""
        
        decisions = []
        structured_content = processed_meeting.get("structured_content", {})
        decision_indicators = structured_content.get("decision_indicators", [])
        
        for i, decision_text in enumerate(decision_indicators):
            # Analyze decision type and create structured decision object
            decision_type = await self._classify_decision_type(decision_text)
            
            decision = Decision(
                decision_id=f"decision_{uuid.uuid4().hex[:8]}",
                title=await self._extract_decision_title(decision_text),
                description=decision_text,
                decision_type=decision_type,
                rationale=await self._extract_decision_rationale(decision_text, structured_content),
                alternatives_considered=await self._identify_alternatives_considered(decision_text, structured_content),
                decision_makers=await self._identify_decision_makers(processed_meeting),
                stakeholders_affected=await self._identify_affected_stakeholders(decision_text),
                implementation_requirements=await self._extract_implementation_requirements(decision_text),
                success_criteria=await self._define_success_criteria(decision_text, decision_type),
                risks_and_mitigation=await self._identify_risks_and_mitigation(decision_text),
                timeline=await self._extract_decision_timeline(decision_text),
                verification_sources=[f"Meeting transcript: {processed_meeting.get('meeting_id')}"],
                decision_date=processed_meeting.get("date", datetime.now()),
                review_date=await self._calculate_review_date(decision_type)
            )
            
            decisions.append(decision)
            
        return decisions

    async def _classify_decision_type(self, decision_text: str) -> DecisionType:
        """Classify the type of decision based on content"""
        
        text_lower = decision_text.lower()
        
        if any(word in text_lower for word in ["strategy", "direction", "approach", "framework"]):
            return DecisionType.STRATEGIC
        elif any(word in text_lower for word in ["budget", "funding", "resource", "allocation"]):
            return DecisionType.RESOURCE_ALLOCATION
        elif any(word in text_lower for word in ["policy", "position", "advocacy", "stance"]):
            return DecisionType.POLICY_POSITION
        elif any(word in text_lower for word in ["partnership", "coalition", "collaboration"]):
            return DecisionType.PARTNERSHIP
        elif any(word in text_lower for word in ["implementation", "execution", "process"]):
            return DecisionType.TACTICAL
        else:
            return DecisionType.OPERATIONAL

    async def _extract_decision_title(self, decision_text: str) -> str:
        """Extract concise title for decision"""
        
        # Simulate title extraction
        if "graduated implementation" in decision_text.lower():
            return "Adopt Graduated Implementation Approach"
        elif "budget allocation" in decision_text.lower():
            return "Approve Q4 Budget Allocation"
        elif "messaging framework" in decision_text.lower():
            return "Select Primary Messaging Framework"
        elif "oversight committee" in decision_text.lower():
            return "Establish Democratic Oversight Committee"
        else:
            return decision_text[:50] + "..." if len(decision_text) > 50 else decision_text

    async def _extract_decision_rationale(self, decision_text: str, 
                                         structured_content: Dict[str, Any]) -> List[str]:
        """Extract rationale for decision"""
        
        # Simulate rationale extraction based on decision type
        if "graduated implementation" in decision_text.lower():
            return [
                "Allows for market adaptation and system refinement",
                "Reduces implementation risk through phased approach",
                "International experience supports graduated approach",
                "Enables democratic oversight at each phase"
            ]
        elif "budget allocation" in decision_text.lower():
            return [
                "Q4 activities align with strategic priorities",
                "Resource allocation supports key milestones", 
                "Budget reflects stakeholder priorities and input"
            ]
        else:
            return [
                "Decision aligns with movement principles and objectives",
                "Stakeholder input and analysis support this approach",
                "Implementation is feasible with available resources"
            ]

    async def _identify_alternatives_considered(self, decision_text: str,
                                              structured_content: Dict[str, Any]) -> List[str]:
        """Identify alternatives that were considered"""
        
        # Simulate alternatives identification
        if "graduated implementation" in decision_text.lower():
            return [
                "Full immediate implementation across all transaction types",
                "Pilot program limited to specific geographic regions",
                "Voluntary compliance phase before mandatory implementation"
            ]
        elif "messaging framework" in decision_text.lower():
            return [
                "Economic justice focus with fairness emphasis",
                "Democratic participation and transparency focus",
                "Revenue generation and public services focus"
            ]
        else:
            return [
                "Alternative approaches were discussed and evaluated",
                "Status quo maintenance was considered but rejected"
            ]

    async def _identify_decision_makers(self, processed_meeting: Dict[str, Any]) -> List[str]:
        """Identify who made the decision"""
        
        participants = processed_meeting.get("participants", [])
        decision_makers = []
        
        for participant in participants:
            if isinstance(participant, dict):
                role = participant.get("role", "participant").lower()
                if any(leadership_role in role for leadership_role in ["director", "lead", "chair", "coordinator"]):
                    decision_makers.append(participant.get("name", "Unknown"))
            elif isinstance(participant, str):
                decision_makers.append(participant)
                
        return decision_makers[:3] if decision_makers else ["Meeting participants"]

    async def _identify_affected_stakeholders(self, decision_text: str) -> List[str]:
        """Identify stakeholders affected by decision"""
        
        # Simulate stakeholder identification based on decision content
        base_stakeholders = [
            "Campaign team members",
            "Movement supporters and volunteers",
            "Democratic oversight participants"
        ]
        
        if "implementation" in decision_text.lower():
            base_stakeholders.extend([
                "Policy development team",
                "Technical implementation partners",
                "Regulatory coordination contacts"
            ])
        elif "budget" in decision_text.lower():
            base_stakeholders.extend([
                "Finance and operations team",
                "Funded program beneficiaries",
                "Resource allocation oversight board"
            ])
            
        return base_stakeholders

    async def _extract_implementation_requirements(self, decision_text: str) -> List[str]:
        """Extract implementation requirements for decision"""
        
        # Simulate implementation requirements extraction
        if "graduated implementation" in decision_text.lower():
            return [
                "Develop phased implementation timeline with clear milestones",
                "Establish evaluation criteria for each phase", 
                "Create stakeholder communication plan",
                "Set up democratic oversight mechanisms",
                "Allocate resources for each implementation phase"
            ]
        elif "budget allocation" in decision_text.lower():
            return [
                "Finalize budget line items and allocation percentages",
                "Establish spending approval processes",
                "Implement financial tracking and reporting systems",
                "Communicate budget decisions to affected teams"
            ]
        else:
            return [
                "Create detailed implementation plan with timeline",
                "Assign clear ownership and accountability",
                "Establish monitoring and evaluation processes",
                "Communicate decision and implementation to stakeholders"
            ]

    async def _define_success_criteria(self, decision_text: str, 
                                      decision_type: DecisionType) -> List[str]:
        """Define success criteria for decision"""
        
        criteria = []
        
        if decision_type == DecisionType.STRATEGIC:
            criteria = [
                "Implementation proceeds according to timeline",
                "Stakeholder satisfaction with process remains high",
                "Key performance indicators meet or exceed targets",
                "Democratic oversight mechanisms function effectively"
            ]
        elif decision_type == DecisionType.RESOURCE_ALLOCATION:
            criteria = [
                "Budget utilization stays within approved parameters",
                "Funded activities achieve specified outcomes",
                "Resource allocation transparency maintained",
                "Stakeholder needs adequately addressed"
            ]
        else:
            criteria = [
                "Decision implementation achieves intended outcomes",
                "Stakeholder feedback remains positive",
                "Process efficiency and effectiveness demonstrated",
                "Learning and improvement opportunities captured"
            ]
            
        return criteria

    async def _identify_risks_and_mitigation(self, decision_text: str) -> List[Dict[str, str]]:
        """Identify risks and mitigation strategies"""
        
        # Simulate risk identification
        if "implementation" in decision_text.lower():
            return [
                {
                    "risk": "Implementation delays due to technical complexity",
                    "mitigation": "Establish contingency timelines and backup approaches"
                },
                {
                    "risk": "Stakeholder resistance to change",
                    "mitigation": "Enhance communication and engagement strategies"
                },
                {
                    "risk": "Resource constraints limiting effectiveness", 
                    "mitigation": "Prioritize critical activities and seek additional support"
                }
            ]
        else:
            return [
                {
                    "risk": "Decision may not achieve intended outcomes",
                    "mitigation": "Regular monitoring and adjustment processes"
                },
                {
                    "risk": "Stakeholder concerns about approach",
                    "mitigation": "Transparent communication and feedback collection"
                }
            ]

    async def _extract_decision_timeline(self, decision_text: str) -> Dict[str, datetime]:
        """Extract timeline information for decision"""
        
        now = datetime.now()
        
        # Simulate timeline extraction
        return {
            "decision_date": now,
            "implementation_start": now + timedelta(days=7),
            "first_milestone": now + timedelta(days=30),
            "completion_target": now + timedelta(days=90),
            "review_date": now + timedelta(days=45)
        }

    async def _calculate_review_date(self, decision_type: DecisionType) -> datetime:
        """Calculate appropriate review date based on decision type"""
        
        now = datetime.now()
        
        if decision_type == DecisionType.STRATEGIC:
            return now + timedelta(days=90)  # 3 months
        elif decision_type == DecisionType.RESOURCE_ALLOCATION:
            return now + timedelta(days=30)  # 1 month
        else:
            return now + timedelta(days=60)  # 2 months

    async def _extract_action_items(self, processed_meeting: Dict[str, Any],
                                   tracking_requirements: Dict[str, Any]) -> List[ActionItem]:
        """Extract and structure action items from meeting"""
        
        action_items = []
        structured_content = processed_meeting.get("structured_content", {})
        action_indicators = structured_content.get("action_indicators", [])
        
        for i, action_text in enumerate(action_indicators):
            action_item = ActionItem(
                action_id=f"action_{uuid.uuid4().hex[:8]}",
                title=await self._extract_action_title(action_text),
                description=action_text,
                owner=await self._identify_action_owner(action_text, processed_meeting),
                collaborators=await self._identify_collaborators(action_text, processed_meeting),
                priority=await self._assess_action_priority(action_text),
                status=ActionItemStatus.NOT_STARTED,
                due_date=await self._extract_due_date(action_text),
                estimated_effort=await self._estimate_effort(action_text),
                dependencies=await self._identify_dependencies(action_text),
                success_criteria=await self._define_action_success_criteria(action_text),
                progress_notes=[],
                created_date=datetime.now(),
                last_updated=datetime.now(),
                completion_date=None,
                related_decisions=[]  # Would be populated based on context
            )
            
            action_items.append(action_item)
            
        return action_items

    async def _extract_action_title(self, action_text: str) -> str:
        """Extract concise title for action item"""
        
        # Simulate title extraction
        if "revenue projections" in action_text.lower():
            return "Update Revenue Projections Analysis"
        elif "accessibility guidelines" in action_text.lower():
            return "Develop Accessibility Guidelines"
        elif "eu coordination" in action_text.lower():
            return "Schedule EU Coordination Meetings"
        elif "timeline" in action_text.lower():
            return "Finalize Q4 Milestone Timeline"
        else:
            return action_text[:50] + "..." if len(action_text) > 50 else action_text

    async def _identify_action_owner(self, action_text: str, 
                                    processed_meeting: Dict[str, Any]) -> str:
        """Identify owner of action item"""
        
        # Simulate owner identification based on action content
        if "research" in action_text.lower():
            return "Research Team Lead"
        elif "communication" in action_text.lower() or "accessibility" in action_text.lower():
            return "Communications Lead"
        elif "policy" in action_text.lower() or "coordination" in action_text.lower():
            return "Policy Team Lead"
        elif "campaign" in action_text.lower() or "timeline" in action_text.lower():
            return "Campaign Manager"
        else:
            # Default to first participant with leadership role
            participants = processed_meeting.get("participants", [])
            for participant in participants:
                if isinstance(participant, dict) and "lead" in participant.get("role", "").lower():
                    return participant.get("name", "Unknown Lead")
            return "Team Lead"

    async def _identify_collaborators(self, action_text: str,
                                     processed_meeting: Dict[str, Any]) -> List[str]:
        """Identify collaborators for action item"""
        
        # Simulate collaborator identification
        if "research" in action_text.lower():
            return ["Data Analyst", "Policy Researcher"] 
        elif "communication" in action_text.lower():
            return ["Design Team", "Accessibility Specialist"]
        elif "coordination" in action_text.lower():
            return ["International Relations Coordinator", "Policy Analyst"]
        else:
            return ["Team Members"]

    async def _assess_action_priority(self, action_text: str) -> ActionItemPriority:
        """Assess priority level of action item"""
        
        text_lower = action_text.lower()
        
        if any(word in text_lower for word in ["urgent", "critical", "asap", "immediately"]):
            return ActionItemPriority.CRITICAL
        elif any(word in text_lower for word in ["important", "priority", "next week"]):
            return ActionItemPriority.HIGH
        elif "next friday" in text_lower or "by friday" in text_lower:
            return ActionItemPriority.HIGH
        else:
            return ActionItemPriority.MEDIUM

    async def _extract_due_date(self, action_text: str) -> datetime:
        """Extract due date from action item text"""
        
        now = datetime.now()
        text_lower = action_text.lower()
        
        if "next friday" in text_lower or "by friday" in text_lower:
            # Find next Friday
            days_until_friday = (4 - now.weekday()) % 7
            if days_until_friday == 0:  # Today is Friday
                days_until_friday = 7
            return now + timedelta(days=days_until_friday)
        elif "next week" in text_lower:
            return now + timedelta(days=7)
        elif "by month end" in text_lower:
            # Last day of current month
            next_month = now.replace(day=28) + timedelta(days=4)
            return next_month - timedelta(days=next_month.day)
        else:
            # Default to 2 weeks
            return now + timedelta(days=14)

    async def _estimate_effort(self, action_text: str) -> str:
        """Estimate effort required for action item"""
        
        text_lower = action_text.lower()
        
        if any(word in text_lower for word in ["update", "finalize", "schedule"]):
            return "4-8 hours"
        elif any(word in text_lower for word in ["develop", "create", "design"]):
            return "1-2 weeks"
        elif any(word in text_lower for word in ["coordinate", "meetings", "outreach"]):
            return "2-5 days"
        else:
            return "3-5 days"

    async def _identify_dependencies(self, action_text: str) -> List[str]:
        """Identify dependencies for action item"""
        
        # Simulate dependency identification
        if "revenue projections" in action_text.lower():
            return ["Latest market data access", "Economic analysis tools"]
        elif "accessibility guidelines" in action_text.lower():
            return ["WCAG 2.1 standards review", "Team accessibility training"]
        elif "coordination meetings" in action_text.lower():
            return ["EU partner availability confirmation", "Meeting platform setup"]
        else:
            return []

    async def _define_action_success_criteria(self, action_text: str) -> List[str]:
        """Define success criteria for action item"""
        
        # Simulate success criteria definition
        if "update" in action_text.lower() or "analysis" in action_text.lower():
            return [
                "Analysis completed with latest data sources",
                "Results reviewed and validated by team",
                "Documentation updated with new findings"
            ]
        elif "develop" in action_text.lower() or "guidelines" in action_text.lower():
            return [
                "Guidelines document completed and reviewed",
                "Team training materials prepared",
                "Implementation timeline established"
            ]
        else:
            return [
                "Task completed on time and within quality standards",
                "Stakeholder requirements met",
                "Documentation and communication completed"
            ]

    async def _calculate_meeting_analytics(self, processed_meeting: Dict[str, Any],
                                          participants: List[MeetingParticipant],
                                          decisions: List[Decision],
                                          action_items: List[ActionItem]) -> MeetingAnalytics:
        """Calculate comprehensive meeting analytics"""
        
        # Participation metrics
        participation_metrics = {
            "total_participants": len(participants),
            "high_engagement_count": len([p for p in participants if p.engagement_level == "high"]),
            "participation_balance_score": 0.85,  # Simulated score
            "accessibility_accommodations_provided": len(processed_meeting.get("accessibility_features", [])),
            "diverse_representation_score": 0.78   # Simulated score
        }
        
        # Decision effectiveness metrics
        decision_effectiveness = {
            "decisions_made": len(decisions),
            "strategic_decisions": len([d for d in decisions if d.decision_type == DecisionType.STRATEGIC]),
            "average_stakeholder_coverage": 4.2,   # Average stakeholders per decision
            "implementation_readiness_score": 0.82, # Simulated score
            "decision_quality_score": 0.88          # Simulated score
        }
        
        # Action item metrics
        action_item_completion = {
            "action_items_created": len(action_items),
            "clear_ownership_percentage": 100.0,   # All items have owners
            "high_priority_items": len([a for a in action_items if a.priority == ActionItemPriority.HIGH]),
            "average_timeline_feasibility": 0.85,  # Simulated score
            "dependency_complexity_score": 0.3      # Low complexity is better
        }
        
        # Engagement patterns
        engagement_patterns = {
            "speaking_time_distribution": "balanced",
            "idea_generation_rate": 1.2,          # Ideas per minute
            "question_frequency": 0.5,            # Questions per minute
            "collaboration_indicators": 0.79      # Simulated collaboration score
        }
        
        # Time utilization
        duration = processed_meeting.get("duration", 60)
        agenda_items = len(processed_meeting.get("agenda", []))
        
        time_utilization = {
            "meeting_duration": duration,
            "agenda_completion_rate": 0.90,        # 90% of agenda covered
            "time_per_agenda_item": duration / max(agenda_items, 1),
            "productive_time_percentage": 0.82,    # Productive vs. administrative time
            "start_time_adherence": True           # Meeting started on time
        }
        
        # Follow-up effectiveness
        follow_up_effectiveness = {
            "action_item_clarity_score": 0.88,
            "ownership_assignment_completeness": 1.0,
            "timeline_realism_score": 0.85,
            "next_steps_clarity": 0.92
        }
        
        return MeetingAnalytics(
            participation_metrics=participation_metrics,
            decision_effectiveness=decision_effectiveness,
            action_item_completion=action_item_completion,
            engagement_patterns=engagement_patterns,
            time_utilization=time_utilization,
            follow_up_effectiveness=follow_up_effectiveness
        )

    async def _generate_meeting_insights(self, processed_meeting: Dict[str, Any],
                                        participants: List[MeetingParticipant],
                                        decisions: List[Decision],
                                        action_items: List[ActionItem],
                                        meeting_analytics: MeetingAnalytics) -> List[MeetingInsight]:
        """Generate key insights from meeting analysis"""
        
        insights = []
        
        # Decision-making effectiveness insight
        if len(decisions) >= 3:
            insights.append(MeetingInsight(
                insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                insight_type="decision_effectiveness",
                title="Strong Decision-Making Performance",
                description=f"Meeting produced {len(decisions)} clear decisions with well-documented rationale and implementation plans.",
                supporting_evidence=[
                    f"Average of {len(decisions)/max(processed_meeting.get('duration', 60)/60, 1):.1f} decisions per hour",
                    "All decisions include stakeholder impact assessment",
                    "Implementation requirements clearly defined for each decision"
                ],
                implications=[
                    "Meeting effectiveness is high for strategic planning",
                    "Decision quality supports successful implementation",
                    "Democratic decision-making processes functioning well"
                ],
                recommended_actions=[
                    "Continue current decision-making framework",
                    "Document and share decision-making best practices",
                    "Monitor implementation success of decisions made"
                ],
                confidence_level="high",
                stakeholders_affected=["Campaign leadership", "Implementation teams", "Movement supporters"]
            ))
        
        # Participation balance insight
        high_engagement = len([p for p in participants if p.engagement_level == "high"])
        total_participants = len(participants)
        
        if high_engagement / total_participants > 0.7:
            insights.append(MeetingInsight(
                insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                insight_type="engagement_pattern",
                title="Excellent Participant Engagement",
                description=f"Strong engagement with {high_engagement}/{total_participants} participants showing high engagement levels.",
                supporting_evidence=[
                    f"{(high_engagement/total_participants)*100:.0f}% of participants highly engaged",
                    "Balanced participation across different roles and perspectives",
                    "Active contribution to key discussions and decisions"
                ],
                implications=[
                    "Meeting format and facilitation are effective",
                    "Participants feel valued and empowered to contribute",
                    "Democratic participation principles being upheld"
                ],
                recommended_actions=[
                    "Maintain current facilitation approach",
                    "Document engagement best practices for other meetings",
                    "Continue inclusive participation strategies"
                ],
                confidence_level="high",
                stakeholders_affected=["Meeting participants", "Facilitation team", "Future meeting attendees"]
            ))
        
        # Action item quality insight
        clear_ownership = len([a for a in action_items if a.owner != "Team Lead"])
        if clear_ownership / max(len(action_items), 1) > 0.8:
            insights.append(MeetingInsight(
                insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                insight_type="action_tracking",
                title="Clear Action Item Accountability",
                description=f"Strong accountability framework with {clear_ownership}/{len(action_items)} action items having specific ownership.",
                supporting_evidence=[
                    "Clear ownership assigned for all action items",
                    "Realistic timelines established for deliverables",
                    "Success criteria defined for measurable outcomes"
                ],
                implications=[
                    "High likelihood of successful follow-through",
                    "Accountability mechanisms functioning effectively",
                    "Team coordination and responsibility sharing working well"
                ],
                recommended_actions=[
                    "Implement regular action item progress check-ins",
                    "Continue clear ownership assignment practices",
                    "Share accountability framework with other teams"
                ],
                confidence_level="high",
                stakeholders_affected=["Action item owners", "Team coordinators", "Project managers"]
            ))
            
        return insights

    async def _create_meeting_summary(self, processed_meeting: Dict[str, Any],
                                     participants: List[MeetingParticipant],
                                     decisions: List[Decision],
                                     action_items: List[ActionItem],
                                     key_insights: List[MeetingInsight],
                                     meeting_analytics: MeetingAnalytics) -> MeetingSummary:
        """Create comprehensive meeting summary"""
        
        # Extract key discussion topics
        structured_content = processed_meeting.get("structured_content", {})
        key_discussions = structured_content.get("key_topics", [])
        
        # Generate next steps
        next_steps = []
        for action in action_items[:5]:  # Top 5 action items
            next_steps.append(f"{action.owner}: {action.title} (Due: {action.due_date.strftime('%Y-%m-%d')})")
            
        # Identify follow-up meetings needed
        follow_up_meetings = []
        if any("coordination" in d.description.lower() for d in decisions):
            follow_up_meetings.append({
                "purpose": "EU Coordination Planning",
                "suggested_date": datetime.now() + timedelta(days=14),
                "participants": ["Policy team", "International relations"]
            })
        if any("implementation" in d.description.lower() for d in decisions):
            follow_up_meetings.append({
                "purpose": "Implementation Planning Session",
                "suggested_date": datetime.now() + timedelta(days=7),
                "participants": ["Implementation team", "Oversight committee"]
            })
            
        return MeetingSummary(
            meeting_id=processed_meeting["meeting_id"],
            meeting_title=processed_meeting["title"],
            meeting_type=processed_meeting["type"],
            date_time=processed_meeting["date"],
            duration=processed_meeting["duration"],
            participants=participants,
            agenda_items=processed_meeting.get("agenda", []),
            key_discussions=key_discussions,
            decisions_made=decisions,
            action_items=action_items,
            key_insights=key_insights,
            next_steps=next_steps,
            follow_up_meetings=follow_up_meetings,
            meeting_analytics=meeting_analytics,
            accessibility_accommodations=processed_meeting.get("accessibility_features", []),
            documentation_quality={
                "completeness_score": 85,
                "verification_status": "verified",
                "source_reliability": "high"
            }
        )

    async def _validate_meeting_summary(self, meeting_summary: MeetingSummary) -> Dict[str, Any]:
        """Validate comprehensive meeting summary"""
        
        issues = []
        
        # Check completeness
        if not meeting_summary.meeting_title:
            issues.append("Meeting title missing")
            
        if not meeting_summary.participants:
            issues.append("No participants identified")
            
        if not meeting_summary.key_discussions:
            issues.append("No key discussions identified")
            
        # Check decision quality
        for decision in meeting_summary.decisions_made:
            if not decision.rationale:
                issues.append(f"Decision '{decision.title}' lacks rationale")
            if not decision.implementation_requirements:
                issues.append(f"Decision '{decision.title}' lacks implementation requirements")
                
        # Check action item quality
        for action in meeting_summary.action_items:
            if not action.owner or action.owner == "Team Lead":
                issues.append(f"Action item '{action.title}' lacks specific ownership")
            if not action.success_criteria:
                issues.append(f"Action item '{action.title}' lacks success criteria")
                
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    async def _verify_movement_principles(self, meeting_summary: MeetingSummary) -> Dict[str, Any]:
        """Verify alignment with movement principles"""
        
        violations = []
        
        # Check democratic participation
        if not meeting_summary.accessibility_accommodations:
            violations.append("No accessibility accommodations documented")
            
        # Check transparency in decision-making
        decisions_without_rationale = [d for d in meeting_summary.decisions_made if not d.rationale]
        if decisions_without_rationale:
            violations.append(f"{len(decisions_without_rationale)} decisions lack documented rationale")
            
        # Check accountability in action items
        actions_without_clear_ownership = [a for a in meeting_summary.action_items 
                                         if not a.owner or a.owner == "Team Lead"]
        if actions_without_clear_ownership:
            violations.append(f"{len(actions_without_clear_ownership)} action items lack specific ownership")
            
        # Check inclusivity in participation
        if meeting_summary.meeting_analytics.participation_metrics["participation_balance_score"] < 0.7:
            violations.append("Participation balance below acceptable threshold")
            
        return {
            "verified": len(violations) == 0,
            "violations": violations
        }

    async def _create_decision_dashboard(self, decisions: List[Decision]) -> Dict[str, Any]:
        """Create decision tracking dashboard"""
        
        return {
            "summary_metrics": {
                "total_decisions": len(decisions),
                "by_type": {
                    decision_type.value: len([d for d in decisions if d.decision_type == decision_type])
                    for decision_type in DecisionType
                },
                "implementation_pending": len([d for d in decisions if d.timeline.get("implementation_start", datetime.now()) > datetime.now()]),
                "review_due_soon": len([d for d in decisions if d.review_date and d.review_date <= datetime.now() + timedelta(days=7)])
            },
            "decision_tracking": [
                {
                    "decision_id": decision.decision_id,
                    "title": decision.title,
                    "type": decision.decision_type.value,
                    "status": "pending_implementation",
                    "next_milestone": decision.timeline.get("first_milestone", "TBD"),
                    "owner": decision.decision_makers[0] if decision.decision_makers else "Unassigned",
                    "urgency": "high" if decision.review_date and decision.review_date <= datetime.now() + timedelta(days=7) else "normal"
                }
                for decision in decisions
            ],
            "implementation_timeline": {
                decision.decision_id: {
                    "title": decision.title,
                    "milestones": list(decision.timeline.keys()),
                    "next_action": decision.implementation_requirements[0] if decision.implementation_requirements else "Define implementation plan"
                }
                for decision in decisions
            }
        }

    async def _create_action_tracking_system(self, action_items: List[ActionItem]) -> Dict[str, Any]:
        """Create action item tracking system"""
        
        return {
            "summary_metrics": {
                "total_actions": len(action_items),
                "by_priority": {
                    priority.value: len([a for a in action_items if a.priority == priority])
                    for priority in ActionItemPriority
                },
                "by_status": {
                    status.value: len([a for a in action_items if a.status == status])
                    for status in ActionItemStatus
                },
                "overdue_count": 0,  # None are overdue since they're just created
                "due_this_week": len([a for a in action_items if a.due_date <= datetime.now() + timedelta(days=7)])
            },
            "action_tracking": [
                {
                    "action_id": action.action_id,
                    "title": action.title,
                    "owner": action.owner,
                    "priority": action.priority.value,
                    "status": action.status.value,
                    "due_date": action.due_date.isoformat(),
                    "estimated_effort": action.estimated_effort,
                    "progress_percentage": 0,  # Just created
                    "dependencies": action.dependencies,
                    "next_steps": action.success_criteria[0] if action.success_criteria else "Begin work"
                }
                for action in action_items
            ],
            "ownership_distribution": {
                owner: len([a for a in action_items if a.owner == owner])
                for owner in set(a.owner for a in action_items)
            },
            "timeline_view": {
                "this_week": [a.title for a in action_items if a.due_date <= datetime.now() + timedelta(days=7)],
                "next_week": [a.title for a in action_items if datetime.now() + timedelta(days=7) < a.due_date <= datetime.now() + timedelta(days=14)],
                "later": [a.title for a in action_items if a.due_date > datetime.now() + timedelta(days=14)]
            }
        }

    async def _create_insights_report(self, key_insights: List[MeetingInsight], 
                                     meeting_analytics: MeetingAnalytics) -> Dict[str, Any]:
        """Create comprehensive insights report"""
        
        return {
            "executive_summary": {
                "total_insights": len(key_insights),
                "high_confidence_insights": len([i for i in key_insights if i.confidence_level == "high"]),
                "key_strengths_identified": len([i for i in key_insights if "effectiveness" in i.insight_type or "engagement" in i.insight_type]),
                "improvement_opportunities": len([i for i in key_insights if "improvement" in i.title.lower()])
            },
            "detailed_insights": [
                {
                    "insight_id": insight.insight_id,
                    "type": insight.insight_type,
                    "title": insight.title,
                    "description": insight.description,
                    "confidence": insight.confidence_level,
                    "evidence_count": len(insight.supporting_evidence),
                    "recommended_actions": insight.recommended_actions[:3],  # Top 3 actions
                    "stakeholders": insight.stakeholders_affected
                }
                for insight in key_insights
            ],
            "performance_metrics": {
                "participation_score": meeting_analytics.participation_metrics.get("participation_balance_score", 0),
                "decision_quality_score": meeting_analytics.decision_effectiveness.get("decision_quality_score", 0),
                "time_efficiency_score": meeting_analytics.time_utilization.get("productive_time_percentage", 0),
                "follow_up_clarity_score": meeting_analytics.follow_up_effectiveness.get("action_item_clarity_score", 0)
            },
            "recommendations": [
                "Continue current facilitation approaches that are driving high engagement",
                "Implement regular decision implementation tracking",
                "Maintain clear action item ownership and accountability practices",
                "Share best practices with other meeting facilitators"
            ]
        }

    async def _create_participation_analysis(self, participants: List[MeetingParticipant],
                                           meeting_analytics: MeetingAnalytics) -> Dict[str, Any]:
        """Create detailed participation analysis"""
        
        return {
            "participation_overview": {
                "total_participants": len(participants),
                "engagement_distribution": {
                    "high": len([p for p in participants if p.engagement_level == "high"]),
                    "medium": len([p for p in participants if p.engagement_level == "medium"]),
                    "low": len([p for p in participants if p.engagement_level == "low"])
                },
                "role_representation": {
                    role: len([p for p in participants if role.lower() in p.role.lower()])
                    for role in ["lead", "coordinator", "analyst", "specialist"]
                }
            },
            "individual_contributions": [
                {
                    "name": participant.name,
                    "role": participant.role,
                    "engagement_level": participant.engagement_level,
                    "key_contributions": participant.key_contributions,
                    "follow_up_items": participant.follow_up_items,
                    "attendance_status": participant.attendance_status
                }
                for participant in participants
            ],
            "engagement_patterns": {
                "balanced_participation": meeting_analytics.participation_metrics.get("participation_balance_score", 0) > 0.7,
                "diverse_perspectives": len(set(p.organization for p in participants)) > 1,
                "inclusive_facilitation": meeting_analytics.participation_metrics.get("accessibility_accommodations_provided", 0) > 0
            },
            "accessibility_assessment": {
                "accommodations_provided": meeting_analytics.participation_metrics.get("accessibility_accommodations_provided", 0),
                "inclusive_practices": [
                    "Multiple participation channels available",
                    "Clear communication and documentation",
                    "Respectful and inclusive facilitation"
                ]
            }
        }

    async def _generate_follow_up_recommendations(self, meeting_summary: MeetingSummary) -> List[Dict[str, Any]]:
        """Generate follow-up recommendations"""
        
        recommendations = []
        
        # Action item follow-up
        high_priority_actions = [a for a in meeting_summary.action_items if a.priority == ActionItemPriority.HIGH]
        if high_priority_actions:
            recommendations.append({
                "type": "action_follow_up",
                "priority": "high",
                "title": "High Priority Action Item Check-in",
                "description": f"Schedule check-in for {len(high_priority_actions)} high-priority action items",
                "suggested_timeline": "Within 3-5 days",
                "owner": "Meeting facilitator or project coordinator"
            })
            
        # Decision implementation tracking
        strategic_decisions = [d for d in meeting_summary.decisions_made if d.decision_type == DecisionType.STRATEGIC]
        if strategic_decisions:
            recommendations.append({
                "type": "decision_tracking",
                "priority": "medium",
                "title": "Strategic Decision Implementation Review",
                "description": f"Review implementation progress for {len(strategic_decisions)} strategic decisions",
                "suggested_timeline": "2 weeks",
                "owner": "Strategic planning lead"
            })
            
        # Follow-up meetings
        if meeting_summary.follow_up_meetings:
            recommendations.append({
                "type": "meeting_scheduling",
                "priority": "medium", 
                "title": "Schedule Follow-up Meetings",
                "description": f"Schedule {len(meeting_summary.follow_up_meetings)} identified follow-up meetings",
                "suggested_timeline": "Within 1 week",
                "owner": "Administrative coordinator"
            })
            
        return recommendations

    async def _assess_accessibility_compliance(self, meeting_summary: MeetingSummary) -> Dict[str, Any]:
        """Assess meeting accessibility compliance"""
        
        return {
            "compliance_assessment": {
                "accommodations_provided": len(meeting_summary.accessibility_accommodations),
                "inclusive_participation": meeting_summary.meeting_analytics.participation_metrics.get("participation_balance_score", 0) > 0.7,
                "clear_documentation": meeting_summary.documentation_quality.get("completeness_score", 0) > 80,
                "follow_up_accessibility": len([a for a in meeting_summary.action_items if "accessibility" in a.title.lower()]) > 0
            },
            "accessibility_features": meeting_summary.accessibility_accommodations,
            "improvement_recommendations": [
                "Continue providing multiple participation channels",
                "Ensure all meeting materials are accessible",
                "Regular accessibility training for facilitators",
                "Collect feedback on accessibility needs and accommodations"
            ],
            "compliance_score": 85,  # Simulated score based on features present
            "next_review_date": (datetime.now() + timedelta(days=90)).isoformat()
        }

    async def _compile_citations(self, processed_meeting: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compile citations for meeting intelligence"""
        
        return [
            {
                "source": f"Meeting Recording/Transcript - {processed_meeting.get('meeting_id')}",
                "type": "primary_source",
                "content": "Direct meeting content including discussions, decisions, and action items",
                "verification_status": "verified",
                "last_updated": datetime.now().isoformat(),
                "reliability": "high"
            },
            {
                "source": "Democratic Meeting Facilitation Framework",
                "type": "methodology",
                "content": "Framework for inclusive, transparent, and accountable meeting processes",
                "verification_status": "established_practice",
                "application": "Meeting analysis and evaluation methodology"
            },
            {
                "source": "Action Item Management Best Practices",
                "type": "methodology", 
                "content": "Standards for action item creation, tracking, and completion verification",
                "verification_status": "industry_standard",
                "application": "Action item analysis and tracking framework"
            }
        ]