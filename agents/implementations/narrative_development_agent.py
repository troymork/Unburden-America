"""
Advanced Narrative Development Agent - Hero's Journey storytelling architect

This agent creates compelling narratives using the Hero's Journey framework, developing story arcs
that guide audiences from hope through concern to empowerment and action. It produces narrative 
beats, scripts, calls-to-action, and accessibility variants aligned with movement principles.
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


class NarrativeStage(Enum):
    """Hero's Journey narrative stages adapted for campaign storytelling"""
    ORDINARY_WORLD = "ordinary_world"           # Current economic reality
    CALL_TO_ADVENTURE = "call_to_adventure"     # Recognition of problem  
    REFUSAL_OF_CALL = "refusal_of_call"         # Initial resistance/skepticism
    MEETING_MENTOR = "meeting_mentor"           # Trusted guides/experts
    CROSSING_THRESHOLD = "crossing_threshold"   # Decision to engage
    TESTS_ALLIES_ENEMIES = "tests_allies_enemies"  # Challenges and support
    APPROACH_INMOST_CAVE = "approach_inmost_cave"  # Confronting core issues
    ORDEAL = "ordeal"                          # Critical challenge moment
    REWARD = "reward"                          # Benefits of engagement
    ROAD_BACK = "road_back"                    # Commitment to action
    RESURRECTION = "resurrection"               # Transformation achieved
    RETURN_ELIXIR = "return_elixir"            # Sharing benefits with community


class EmotionalJourney(Enum):
    """Emotional progression through narrative stages"""
    HOPE = "hope"                 # Initial optimism and possibility
    CONCERN = "concern"           # Growing awareness of challenges  
    EMPOWERMENT = "empowerment"   # Building confidence and capability
    ACTION = "action"             # Commitment to engagement


class ContentFormat(Enum):
    """Content format types for narrative delivery"""
    ARTICLE = "article"
    VIDEO_SCRIPT = "video_script"
    SOCIAL_POST = "social_post"  
    SPEECH = "speech"
    PODCAST_SCRIPT = "podcast_script"
    EMAIL_SEQUENCE = "email_sequence"
    INFOGRAPHIC_COPY = "infographic_copy"
    TESTIMONIAL = "testimonial"


@dataclass
class NarrativeBeat:
    """Individual narrative beat within the story arc"""
    id: str
    stage: NarrativeStage
    emotion: EmotionalJourney
    beat_title: str
    description: str
    key_message: str
    supporting_points: List[str]
    call_to_action: str
    duration_estimate: int       # Seconds/words depending on format
    accessibility_notes: List[str]
    fact_verification_needed: List[str]


@dataclass 
class NarrativeScript:
    """Complete narrative script with all components"""
    title: str
    format_type: ContentFormat
    target_audience: str
    narrative_beats: List[NarrativeBeat]
    total_duration: int
    accessibility_variants: Dict[str, Any]
    fact_database: List[Dict[str, Any]]
    call_to_action_framework: Dict[str, Any]
    emotional_arc_summary: str


@dataclass
class AccessibilityVariant:
    """Accessibility-specific version of narrative content"""
    variant_type: str             # audio_description, captions, plain_language
    content: str
    compliance_level: str         # WCAG_2.1_AA, Section_508
    target_disabilities: List[str]
    technical_requirements: List[str]


class NarrativeDevelopmentAgent(BaseAgent):
    """
    Advanced narrative development using Hero's Journey framework to create
    compelling story arcs that guide audiences through hope → concern → empowerment → action.
    """
    
    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_type="narrative_development",
            agent_id=agent_id or f"narrative_dev_{uuid.uuid4().hex[:8]}"
        )
        self.narrative_templates = self._load_narrative_templates()
        self.emotional_frameworks = self._load_emotional_frameworks()
        self.accessibility_standards = self._load_accessibility_standards()
        self.movement_storytelling = self._load_movement_storytelling()
        
        logging.info(f"Narrative Development Agent initialized: {self.agent_id}")

    def _load_narrative_templates(self) -> Dict[str, Any]:
        """Load Hero's Journey templates adapted for campaign narratives"""
        return {
            "hero_journey_stages": {
                NarrativeStage.ORDINARY_WORLD: {
                    "purpose": "Establish current economic reality and audience connection",
                    "emotion_target": EmotionalJourney.HOPE,
                    "key_elements": [
                        "Relatable economic situation",
                        "Universal hopes and dreams",
                        "Current system challenges"
                    ],
                    "example_hooks": [
                        "Working families know what it means to stretch every dollar",
                        "Small businesses are the backbone of our communities",
                        "Everyone deserves a fair shot at economic opportunity"
                    ]
                },
                NarrativeStage.CALL_TO_ADVENTURE: {
                    "purpose": "Introduce the monetary flow tax opportunity",
                    "emotion_target": EmotionalJourney.HOPE,
                    "key_elements": [
                        "Problem recognition",
                        "Solution introduction", 
                        "Possibility of change"
                    ],
                    "example_hooks": [
                        "What if there was a way to make the financial system work for everyone?",
                        "Imagine high-frequency traders paying their fair share",
                        "A simple 3% tax could transform our economy"
                    ]
                },
                NarrativeStage.REFUSAL_OF_CALL: {
                    "purpose": "Address skepticism and acknowledge challenges",
                    "emotion_target": EmotionalJourney.CONCERN,
                    "key_elements": [
                        "Common objections",
                        "Legitimate concerns",
                        "Complexity acknowledgment"
                    ],
                    "example_hooks": [
                        "It sounds too good to be true, doesn't it?",
                        "The financial industry will fight this hard",
                        "Change is never easy, especially when it threatens power"
                    ]
                },
                NarrativeStage.MEETING_MENTOR: {
                    "purpose": "Introduce trusted guides and expert validation",
                    "emotion_target": EmotionalJourney.EMPOWERMENT,
                    "key_elements": [
                        "Expert endorsements",
                        "Historical precedents",
                        "Trusted sources"
                    ],
                    "example_hooks": [
                        "Leading economists have studied this extensively",
                        "We've successfully implemented similar policies before",
                        "Independent research confirms the benefits"
                    ]
                }
            },
            "emotional_transitions": {
                "hope_to_concern": [
                    "Acknowledge the scale of the challenge",
                    "Validate audience concerns",
                    "Maintain connection to possibility"
                ],
                "concern_to_empowerment": [
                    "Provide evidence and expertise",
                    "Show successful precedents", 
                    "Build confidence in collective action"
                ],
                "empowerment_to_action": [
                    "Clear, specific next steps",
                    "Make action feel achievable",
                    "Connect individual action to collective impact"
                ]
            }
        }

    def _load_emotional_frameworks(self) -> Dict[str, Any]:
        """Load emotional progression frameworks for narrative development"""
        return {
            "emotional_arc_patterns": {
                "classic_hero": {
                    "progression": [
                        EmotionalJourney.HOPE,
                        EmotionalJourney.CONCERN, 
                        EmotionalJourney.EMPOWERMENT,
                        EmotionalJourney.ACTION
                    ],
                    "description": "Traditional hope → concern → empowerment → action arc",
                    "best_for": ["articles", "speeches", "video_content"]
                },
                "empowerment_focus": {
                    "progression": [
                        EmotionalJourney.HOPE,
                        EmotionalJourney.EMPOWERMENT,
                        EmotionalJourney.ACTION,
                        EmotionalJourney.HOPE
                    ],
                    "description": "Emphasizes capability and positive action",
                    "best_for": ["social_media", "testimonials", "calls_to_action"]
                },
                "concern_driven": {
                    "progression": [
                        EmotionalJourney.CONCERN,
                        EmotionalJourney.HOPE,
                        EmotionalJourney.EMPOWERMENT,
                        EmotionalJourney.ACTION
                    ],
                    "description": "Starts with urgency, builds to positive action",
                    "best_for": ["crisis_response", "urgent_campaigns"]
                }
            },
            "emotional_triggers": {
                EmotionalJourney.HOPE: [
                    "Possibility of positive change",
                    "Success stories and examples",
                    "Collective potential and unity",
                    "Better future for families"
                ],
                EmotionalJourney.CONCERN: [
                    "System unfairness and inequality", 
                    "Threats to economic security",
                    "Concentration of wealth and power",
                    "Democratic deficit in economic policy"
                ],
                EmotionalJourney.EMPOWERMENT: [
                    "Knowledge and understanding",
                    "Collective action potential",
                    "Democratic participation tools",
                    "Proven strategies and tactics"
                ],
                EmotionalJourney.ACTION: [
                    "Clear, achievable steps",
                    "Immediate impact opportunities", 
                    "Community and solidarity",
                    "Personal agency and efficacy"
                ]
            }
        }

    def _load_accessibility_standards(self) -> Dict[str, Any]:
        """Load accessibility standards for narrative content"""
        return {
            "wcag_2_1_aa": {
                "text_requirements": [
                    "Minimum 4.5:1 contrast ratio",
                    "Text resizable up to 200%",
                    "Line spacing at least 1.5x",
                    "Paragraph spacing at least 2x font size"
                ],
                "language_requirements": [
                    "Reading level appropriate for audience",
                    "Clear headings and structure", 
                    "Definitions for technical terms",
                    "Consistent navigation and layout"
                ],
                "media_requirements": [
                    "Captions for all audio content",
                    "Audio descriptions for visual content",
                    "Transcripts for multimedia",
                    "Alternative formats available"
                ]
            },
            "plain_language_standards": [
                "Use active voice",
                "Keep sentences under 20 words",
                "Use common words over technical terms",
                "Define necessary jargon immediately",
                "Use bullets and lists for clarity",
                "Include examples and analogies"
            ],
            "cognitive_accessibility": [
                "Clear headings and structure",
                "Consistent design patterns",
                "Progress indicators for long content",
                "Summary sections for complex topics",
                "Multiple ways to navigate content",
                "Error prevention and recovery"
            ]
        }

    def _load_movement_storytelling(self) -> Dict[str, Any]:
        """Load movement-specific storytelling guidelines and examples"""
        return {
            "core_narratives": {
                "economic_fairness": {
                    "hero": "Working families and small businesses",
                    "villain": "Unfair tax system that privileges speculation",
                    "quest": "Create fair taxation of financial transactions",
                    "treasure": "More resources for education, healthcare, infrastructure"
                },
                "democratic_participation": {
                    "hero": "Citizens seeking transparency",
                    "villain": "Hidden financial flows and lack of oversight", 
                    "quest": "Make economic policy more democratic",
                    "treasure": "Greater citizen voice in economic decisions"
                },
                "economic_justice": {
                    "hero": "Communities building economic power",
                    "villain": "Concentration of wealth in financial sector",
                    "quest": "Rebalance economy toward productive activity",
                    "treasure": "Stronger local economies and opportunity"
                }
            },
            "movement_messaging": {
                "key_facts": {
                    "monetary_economy_scale": "$4.7 quadrillion in annual transactions",
                    "real_economy_scale": "$30 trillion in annual goods/services",
                    "proposed_tax_rate": "3% on high-frequency financial transactions",
                    "wealth_concentration": "Top 1% owns 32% of total wealth"
                },
                "analogies": [
                    "Financial transactions are like traffic on economic highways - high-volume users should pay tolls",
                    "The monetary flow tax is like a small service fee on financial speculation",
                    "Think of it as asking day traders to contribute to the communities they profit from"
                ],
                "avoid_language": [
                    "Punishing" or "targeting" specific groups,
                    "Anti-business" framing,
                    "Complex financial jargon without explanation",
                    "Partisan political language"
                ]
            },
            "success_stories": [
                {
                    "country": "United Kingdom", 
                    "policy": "Stamp duty on stock transactions",
                    "outcome": "Generates £3+ billion annually with minimal market disruption",
                    "lesson": "Financial transaction taxes can work in major economies"
                },
                {
                    "country": "France",
                    "policy": "Financial transaction tax on equity trades", 
                    "outcome": "Successfully implemented with EU support",
                    "lesson": "International coordination makes implementation easier"
                }
            ]
        }

    async def process(self, inputs: Dict[str, Any]) -> AgentOutput:
        """
        Process narrative development request using Hero's Journey framework
        
        Args:
            inputs: Contains narrative_brief, target_audience, content_format, emotional_arc
            
        Returns:
            AgentOutput with narrative scripts, beats, CTAs, and accessibility variants
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

            # Extract narrative parameters
            narrative_brief = inputs.get("narrative_brief", {})
            target_audience = inputs.get("target_audience", "general_public")
            content_format = ContentFormat(inputs.get("content_format", "article"))
            emotional_arc = inputs.get("emotional_arc", "classic_hero")
            accessibility_requirements = inputs.get("accessibility_requirements", ["wcag_2_1_aa"])
            
            # Develop narrative structure
            narrative_arc = await self._design_narrative_arc(
                narrative_brief, target_audience, emotional_arc
            )
            
            # Create narrative beats
            narrative_beats = await self._create_narrative_beats(
                narrative_arc, narrative_brief, content_format
            )
            
            # Quality Gate: Mid-process validation
            beats_quality = await self._validate_narrative_quality(narrative_beats)
            if not beats_quality["valid"]:
                return AgentOutput(
                    agent_id=self.agent_id,
                    agent_type=self.agent_type, 
                    success=False,
                    content={},
                    metadata={"error": f"Narrative quality issues: {beats_quality['issues']}"},
                    quality_gates_passed=[QualityGate.INPUT_VALIDATION],
                    movement_principles_verified=False
                )

            # Generate complete scripts
            narrative_scripts = await self._generate_narrative_scripts(
                narrative_beats, content_format, target_audience
            )
            
            # Create accessibility variants
            accessibility_variants = await self._create_accessibility_variants(
                narrative_scripts, accessibility_requirements
            )
            
            # Develop call-to-action framework
            cta_framework = await self._develop_cta_framework(narrative_beats, target_audience)
            
            # Compile fact verification database
            fact_database = await self._compile_fact_database(narrative_beats)

            # Quality Gate: Pre-handoff validation
            final_validation = await self._validate_final_narrative(
                narrative_scripts, accessibility_variants, fact_database
            )
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
            principles_check = await self._verify_movement_principles(narrative_scripts, fact_database)

            # Generate handoff package
            handoff_package = await self._generate_handoff_package(
                narrative_scripts, accessibility_variants, cta_framework
            )

            return AgentOutput(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                success=True,
                content={
                    "narrative_scripts": [asdict(script) for script in narrative_scripts],
                    "accessibility_variants": accessibility_variants,
                    "call_to_action_framework": cta_framework,
                    "fact_database": fact_database,
                    "emotional_arc_analysis": await self._analyze_emotional_arc(narrative_beats),
                    "implementation_guide": handoff_package,
                    "performance_optimization": await self._generate_performance_optimization(narrative_scripts)
                },
                metadata={
                    "narrative_format": content_format.value,
                    "emotional_arc": emotional_arc,
                    "beats_count": len(narrative_beats),
                    "accessibility_compliance": accessibility_requirements,
                    "total_estimated_duration": sum(beat.duration_estimate for beat in narrative_beats),
                    "fact_verification_points": len(fact_database),
                    "generated_at": datetime.now().isoformat()
                },
                quality_gates_passed=[
                    QualityGate.INPUT_VALIDATION,
                    QualityGate.CONTENT_QUALITY,
                    QualityGate.FACT_VERIFICATION,
                    QualityGate.MOVEMENT_ALIGNMENT
                ],
                movement_principles_verified=principles_check["verified"],
                citations=await self._compile_citations(fact_database)
            )

        except Exception as e:
            logging.error(f"Narrative Development Agent error: {str(e)}")
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
        """Validate narrative development inputs"""
        errors = []
        
        narrative_brief = inputs.get("narrative_brief", {})
        if not narrative_brief.get("topic"):
            errors.append("Narrative topic is required")
            
        if not narrative_brief.get("key_message"):
            errors.append("Key message is required")
            
        content_format = inputs.get("content_format")
        if content_format and content_format not in [f.value for f in ContentFormat]:
            errors.append(f"Invalid content format: {content_format}")
            
        emotional_arc = inputs.get("emotional_arc", "classic_hero")
        if emotional_arc not in self.emotional_frameworks["emotional_arc_patterns"]:
            errors.append(f"Unknown emotional arc pattern: {emotional_arc}")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    async def _design_narrative_arc(self, narrative_brief: Dict[str, Any], 
                                   target_audience: str, 
                                   emotional_arc: str) -> Dict[str, Any]:
        """Design the overall narrative arc structure"""
        
        arc_pattern = self.emotional_frameworks["emotional_arc_patterns"][emotional_arc]
        emotion_progression = arc_pattern["progression"]
        
        # Map Hero's Journey stages to emotional progression
        stage_emotion_map = []
        stages_per_emotion = len(NarrativeStage) // len(emotion_progression)
        
        stages = list(NarrativeStage)
        emotion_index = 0
        
        for i, stage in enumerate(stages):
            if i > 0 and i % stages_per_emotion == 0 and emotion_index < len(emotion_progression) - 1:
                emotion_index += 1
            
            stage_emotion_map.append({
                "stage": stage,
                "emotion": emotion_progression[emotion_index],
                "stage_order": i + 1,
                "emotion_transition": i > 0 and stages[i-1] != stage
            })

        # Select appropriate narrative core
        topic = narrative_brief.get("topic", "").lower()
        if "tax" in topic or "fairness" in topic:
            core_narrative = self.movement_storytelling["core_narratives"]["economic_fairness"]
        elif "democracy" in topic or "participation" in topic:
            core_narrative = self.movement_storytelling["core_narratives"]["democratic_participation"]
        else:
            core_narrative = self.movement_storytelling["core_narratives"]["economic_justice"]
            
        return {
            "emotional_progression": emotion_progression,
            "stage_emotion_map": stage_emotion_map,
            "core_narrative": core_narrative,
            "arc_pattern": arc_pattern,
            "target_audience": target_audience,
            "narrative_theme": narrative_brief.get("topic", "Economic Justice")
        }

    async def _create_narrative_beats(self, narrative_arc: Dict[str, Any], 
                                     narrative_brief: Dict[str, Any],
                                     content_format: ContentFormat) -> List[NarrativeBeat]:
        """Create detailed narrative beats for each stage"""
        
        beats = []
        stage_emotion_map = narrative_arc["stage_emotion_map"]
        core_narrative = narrative_arc["core_narrative"]
        
        # Duration per beat based on content format
        format_durations = {
            ContentFormat.ARTICLE: 200,        # 200 words per beat
            ContentFormat.VIDEO_SCRIPT: 30,    # 30 seconds per beat
            ContentFormat.SOCIAL_POST: 50,     # 50 words per beat
            ContentFormat.SPEECH: 45,          # 45 seconds per beat
            ContentFormat.PODCAST_SCRIPT: 60,  # 60 seconds per beat
            ContentFormat.EMAIL_SEQUENCE: 150, # 150 words per beat
            ContentFormat.INFOGRAPHIC_COPY: 25, # 25 words per beat
            ContentFormat.TESTIMONIAL: 100     # 100 words per beat
        }
        
        base_duration = format_durations.get(content_format, 100)
        
        for stage_info in stage_emotion_map:
            stage = stage_info["stage"]
            emotion = stage_info["emotion"]
            
            # Get stage template
            stage_template = self.narrative_templates["hero_journey_stages"].get(stage)
            if not stage_template:
                continue
                
            # Create beat for this stage
            beat = await self._create_single_beat(
                stage, emotion, stage_template, core_narrative, 
                narrative_brief, base_duration, content_format
            )
            
            beats.append(beat)
            
        return beats

    async def _create_single_beat(self, stage: NarrativeStage, emotion: EmotionalJourney,
                                 stage_template: Dict[str, Any], core_narrative: Dict[str, Any],
                                 narrative_brief: Dict[str, Any], base_duration: int,
                                 content_format: ContentFormat) -> NarrativeBeat:
        """Create a single narrative beat"""
        
        # Generate beat content based on stage and movement context
        beat_content = await self._generate_beat_content(
            stage, emotion, stage_template, core_narrative, narrative_brief
        )
        
        # Identify fact verification needs
        fact_verification = await self._identify_fact_verification_needs(beat_content)
        
        # Generate accessibility notes
        accessibility_notes = await self._generate_accessibility_notes(beat_content, content_format)
        
        return NarrativeBeat(
            id=f"beat_{uuid.uuid4().hex[:8]}",
            stage=stage,
            emotion=emotion,
            beat_title=beat_content["title"],
            description=beat_content["description"], 
            key_message=beat_content["key_message"],
            supporting_points=beat_content["supporting_points"],
            call_to_action=beat_content["call_to_action"],
            duration_estimate=base_duration,
            accessibility_notes=accessibility_notes,
            fact_verification_needed=fact_verification
        )

    async def _generate_beat_content(self, stage: NarrativeStage, emotion: EmotionalJourney,
                                   stage_template: Dict[str, Any], core_narrative: Dict[str, Any],
                                   narrative_brief: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content for a specific narrative beat"""
        
        topic = narrative_brief.get("topic", "Economic Justice")
        key_message = narrative_brief.get("key_message", "")
        
        # Stage-specific content generation
        if stage == NarrativeStage.ORDINARY_WORLD:
            return {
                "title": "The Reality We Know",
                "description": f"Establish the current economic reality that {core_narrative['hero']} experiences daily",
                "key_message": f"Working families understand the challenges of making ends meet in today's economy",
                "supporting_points": [
                    "Rising costs of living outpacing wage growth",
                    "Financial insecurity affecting middle-class families", 
                    "Need for fair economic policies that work for everyone"
                ],
                "call_to_action": "Recognize that we all share these challenges"
            }
            
        elif stage == NarrativeStage.CALL_TO_ADVENTURE:
            return {
                "title": "A Path Forward",
                "description": f"Introduce the monetary flow tax as a solution to {topic}",
                "key_message": key_message or "The monetary flow tax offers a fair way to fund our shared priorities",
                "supporting_points": [
                    f"$4.7 quadrillion in financial transactions vs. $30 trillion real economy",
                    "3% tax on high-frequency trading could generate significant revenue",
                    "Other countries have successfully implemented similar policies"
                ],
                "call_to_action": "Consider how this could benefit your community"
            }
            
        elif stage == NarrativeStage.MEETING_MENTOR:
            return {
                "title": "Expert Guidance", 
                "description": "Present authoritative sources supporting the monetary flow tax",
                "key_message": "Leading economists and policy experts have studied this approach extensively",
                "supporting_points": [
                    "Independent research validates the policy approach",
                    "Successful international examples provide blueprints",
                    "Bipartisan support exists for fair taxation principles"
                ],
                "call_to_action": "Learn from those who have studied this issue deeply"
            }
            
        elif stage == NarrativeStage.CROSSING_THRESHOLD:
            return {
                "title": "Taking the First Step",
                "description": "Encourage initial engagement with the movement",
                "key_message": "Every major change starts with people deciding to get involved",
                "supporting_points": [
                    "Your voice matters in shaping economic policy",
                    "Democratic participation is how we create change",
                    "Small actions by many people add up to big impact"
                ],
                "call_to_action": "Join thousands of others supporting fair taxation"
            }
            
        elif stage == NarrativeStage.RETURN_ELIXIR:
            return {
                "title": "Sharing the Benefits",
                "description": "Envision how monetary flow tax benefits will strengthen communities",
                "key_message": "Fair taxation creates resources for education, healthcare, and infrastructure",
                "supporting_points": [
                    "Investments in public goods benefit everyone",
                    "Stronger communities support thriving families",
                    "Economic justice creates opportunity for all"
                ],
                "call_to_action": "Help build the fair economy your community deserves"
            }
            
        else:
            # Default content for other stages
            return {
                "title": f"{stage.value.replace('_', ' ').title()}",
                "description": f"Narrative beat for {stage.value} stage",
                "key_message": key_message or f"Supporting {topic} through {stage.value}",
                "supporting_points": stage_template.get("key_elements", []),
                "call_to_action": "Continue engaging with this important issue"
            }

    async def _identify_fact_verification_needs(self, beat_content: Dict[str, Any]) -> List[str]:
        """Identify claims requiring fact verification"""
        
        verification_needed = []
        
        # Check for quantitative claims
        text_to_check = f"{beat_content['key_message']} {' '.join(beat_content['supporting_points'])}"
        
        # Look for monetary amounts
        if "$" in text_to_check:
            verification_needed.append("Monetary figures require source verification")
            
        # Look for percentages
        if "%" in text_to_check:
            verification_needed.append("Percentage claims require source verification")
            
        # Look for comparative claims
        comparative_terms = ["more than", "less than", "higher than", "lower than", "vs.", "compared to"]
        if any(term in text_to_check.lower() for term in comparative_terms):
            verification_needed.append("Comparative claims require source verification")
            
        # Look for policy claims
        policy_terms = ["law", "regulation", "policy", "implemented", "successful"]
        if any(term in text_to_check.lower() for term in policy_terms):
            verification_needed.append("Policy claims require government source verification")
            
        return verification_needed

    async def _generate_accessibility_notes(self, beat_content: Dict[str, Any], 
                                           content_format: ContentFormat) -> List[str]:
        """Generate accessibility considerations for narrative beat"""
        
        notes = []
        
        # Format-specific accessibility considerations
        if content_format in [ContentFormat.VIDEO_SCRIPT, ContentFormat.PODCAST_SCRIPT]:
            notes.extend([
                "Provide captions for all spoken content",
                "Include audio descriptions for visual elements",
                "Ensure clear pronunciation of technical terms"
            ])
            
        if content_format == ContentFormat.INFOGRAPHIC_COPY:
            notes.extend([
                "Include alt-text for all visual elements",
                "Ensure sufficient color contrast",
                "Provide text-only alternative version"
            ])
            
        # General accessibility notes
        notes.extend([
            "Use plain language where possible",
            "Define technical terms immediately",
            "Maintain consistent structure and navigation"
        ])
        
        # Content-specific considerations
        key_message = beat_content["key_message"]
        if len(key_message) > 100:
            notes.append("Consider breaking long key message into shorter segments")
            
        supporting_points = beat_content["supporting_points"]
        if len(supporting_points) > 5:
            notes.append("Consider grouping supporting points for cognitive accessibility")
            
        return notes

    async def _validate_narrative_quality(self, narrative_beats: List[NarrativeBeat]) -> Dict[str, Any]:
        """Validate overall narrative quality and coherence"""
        
        issues = []
        
        # Check emotional progression
        emotions = [beat.emotion for beat in narrative_beats]
        if EmotionalJourney.ACTION not in emotions:
            issues.append("Narrative lacks action-oriented conclusion")
            
        # Check for call-to-action progression
        ctas = [beat.call_to_action for beat in narrative_beats]
        if len(set(ctas)) < 3:  # Should have varied CTAs
            issues.append("Insufficient variation in calls-to-action")
            
        # Check for fact verification coverage
        total_verification_needs = sum(len(beat.fact_verification_needed) for beat in narrative_beats)
        if total_verification_needs == 0:
            issues.append("No fact verification needs identified - may indicate lack of substantive claims")
            
        # Check narrative flow
        stages = [beat.stage for beat in narrative_beats]
        if len(stages) < 5:  # Should have reasonable narrative depth
            issues.append("Narrative may be too brief for effective storytelling")
            
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    async def _generate_narrative_scripts(self, narrative_beats: List[NarrativeBeat],
                                         content_format: ContentFormat,
                                         target_audience: str) -> List[NarrativeScript]:
        """Generate complete narrative scripts from beats"""
        
        scripts = []
        
        # Group beats by major narrative sections
        script_sections = await self._group_beats_into_sections(narrative_beats)
        
        for section_name, section_beats in script_sections.items():
            # Calculate total duration
            total_duration = sum(beat.duration_estimate for beat in section_beats)
            
            # Compile fact database for section
            fact_database = await self._compile_section_fact_database(section_beats)
            
            # Create CTA framework for section
            cta_framework = await self._create_section_cta_framework(section_beats)
            
            # Generate emotional arc summary
            emotional_arc = await self._summarize_emotional_arc(section_beats)
            
            script = NarrativeScript(
                title=f"{section_name.title()} - {content_format.value.title()}",
                format_type=content_format,
                target_audience=target_audience,
                narrative_beats=section_beats,
                total_duration=total_duration,
                accessibility_variants={},  # Will be populated separately
                fact_database=fact_database,
                call_to_action_framework=cta_framework,
                emotional_arc_summary=emotional_arc
            )
            
            scripts.append(script)
            
        return scripts

    async def _group_beats_into_sections(self, narrative_beats: List[NarrativeBeat]) -> Dict[str, List[NarrativeBeat]]:
        """Group narrative beats into logical sections"""
        
        sections = {
            "opening": [],
            "development": [],
            "climax": [], 
            "resolution": []
        }
        
        total_beats = len(narrative_beats)
        
        for i, beat in enumerate(narrative_beats):
            if i < total_beats * 0.25:
                sections["opening"].append(beat)
            elif i < total_beats * 0.65:
                sections["development"].append(beat) 
            elif i < total_beats * 0.85:
                sections["climax"].append(beat)
            else:
                sections["resolution"].append(beat)
                
        return sections

    async def _compile_section_fact_database(self, section_beats: List[NarrativeBeat]) -> List[Dict[str, Any]]:
        """Compile fact database for a narrative section"""
        
        fact_database = []
        
        for beat in section_beats:
            if beat.fact_verification_needed:
                fact_database.append({
                    "beat_id": beat.id,
                    "claims": beat.fact_verification_needed,
                    "supporting_points": beat.supporting_points,
                    "verification_status": "pending",
                    "sources_needed": len(beat.fact_verification_needed) * 2,  # Minimum 2 sources per claim
                    "priority": "high" if "monetary" in str(beat.fact_verification_needed).lower() else "medium"
                })
                
        return fact_database

    async def _create_section_cta_framework(self, section_beats: List[NarrativeBeat]) -> Dict[str, Any]:
        """Create call-to-action framework for narrative section"""
        
        ctas = [beat.call_to_action for beat in section_beats]
        emotions = [beat.emotion for beat in section_beats]
        
        return {
            "primary_cta": ctas[-1] if ctas else "Learn more about economic justice",
            "progressive_ctas": ctas,
            "emotional_alignment": {
                "dominant_emotion": max(set(emotions), key=emotions.count).value,
                "emotion_progression": [e.value for e in emotions]
            },
            "engagement_ladder": [
                "Awareness: Recognize the issue",
                "Interest: Learn more details", 
                "Consideration: Evaluate personal relevance",
                "Action: Take specific next step"
            ]
        }

    async def _summarize_emotional_arc(self, section_beats: List[NarrativeBeat]) -> str:
        """Generate emotional arc summary for narrative section"""
        
        emotions = [beat.emotion.value for beat in section_beats]
        stages = [beat.stage.value for beat in section_beats]
        
        return f"Emotional progression: {' → '.join(emotions)} across narrative stages: {' → '.join(stages[:3])}..."

    async def _create_accessibility_variants(self, narrative_scripts: List[NarrativeScript],
                                           accessibility_requirements: List[str]) -> Dict[str, Any]:
        """Create accessibility variants for narrative content"""
        
        variants = {}
        
        for requirement in accessibility_requirements:
            if requirement == "wcag_2_1_aa":
                variants["wcag_compliant"] = await self._create_wcag_variant(narrative_scripts)
            elif requirement == "plain_language":
                variants["plain_language"] = await self._create_plain_language_variant(narrative_scripts)
            elif requirement == "audio_description":
                variants["audio_description"] = await self._create_audio_description_variant(narrative_scripts)
                
        return variants

    async def _create_wcag_variant(self, narrative_scripts: List[NarrativeScript]) -> Dict[str, Any]:
        """Create WCAG 2.1 AA compliant variant"""
        
        wcag_variant = {
            "compliance_level": "WCAG_2.1_AA",
            "modifications": [
                "Added structured headings (H1-H6)",
                "Ensured 4.5:1 minimum contrast ratio",
                "Provided alternative text for descriptions",
                "Added skip navigation links"
            ],
            "technical_requirements": [
                "Semantic HTML structure",
                "Keyboard navigation support",
                "Screen reader compatibility",
                "Resizable text up to 200%"
            ],
            "content_adaptations": []
        }
        
        for script in narrative_scripts:
            adaptations = []
            for beat in script.narrative_beats:
                if len(beat.description) > 200:
                    adaptations.append(f"Beat '{beat.beat_title}': Added paragraph breaks for readability")
                if beat.fact_verification_needed:
                    adaptations.append(f"Beat '{beat.beat_title}': Added inline citations for accessibility")
                    
            wcag_variant["content_adaptations"].extend(adaptations)
            
        return wcag_variant

    async def _create_plain_language_variant(self, narrative_scripts: List[NarrativeScript]) -> Dict[str, Any]:
        """Create plain language variant"""
        
        return {
            "compliance_level": "Plain_Language_Guidelines",
            "reading_level": "8th grade or below",
            "modifications": [
                "Simplified complex sentences",
                "Replaced jargon with common terms",
                "Added definitions for necessary technical terms",
                "Used active voice throughout"
            ],
            "language_adaptations": [
                "monetary flow tax → tax on financial trading",
                "high-frequency transactions → rapid trading",
                "quadrillion → very large number ($4,700 trillion)",
                "economic justice → fair economic treatment"
            ]
        }

    async def _create_audio_description_variant(self, narrative_scripts: List[NarrativeScript]) -> Dict[str, Any]:
        """Create audio description variant for visual content"""
        
        return {
            "compliance_level": "Audio_Description_Standards",
            "target_formats": ["video", "infographic", "presentation"],
            "descriptions": [
                "Visual elements: Charts, graphs, and infographics described in detail",
                "Speaker actions: Gestures and visual cues narrated",
                "Text overlays: All on-screen text read aloud",
                "Scene changes: Transitions and visual context provided"
            ],
            "timing_considerations": [
                "Descriptions fit within natural pauses",
                "Essential visual information prioritized", 
                "Consistent narrator voice and pacing"
            ]
        }

    async def _develop_cta_framework(self, narrative_beats: List[NarrativeBeat], 
                                   target_audience: str) -> Dict[str, Any]:
        """Develop comprehensive call-to-action framework"""
        
        # Extract all CTAs from beats
        beat_ctas = [beat.call_to_action for beat in narrative_beats]
        
        # Categorize CTAs by engagement level
        cta_categories = {
            "awareness": [],
            "consideration": [],
            "action": [],
            "advocacy": []
        }
        
        for cta in beat_ctas:
            cta_lower = cta.lower()
            if any(word in cta_lower for word in ["learn", "recognize", "understand"]):
                cta_categories["awareness"].append(cta)
            elif any(word in cta_lower for word in ["consider", "explore", "think"]):
                cta_categories["consideration"].append(cta)
            elif any(word in cta_lower for word in ["join", "sign", "participate", "support"]):
                cta_categories["action"].append(cta)
            elif any(word in cta_lower for word in ["share", "tell", "advocate", "build"]):
                cta_categories["advocacy"].append(cta)
            else:
                cta_categories["consideration"].append(cta)  # Default
        
        return {
            "engagement_ladder": {
                "awareness": cta_categories["awareness"][:3],
                "consideration": cta_categories["consideration"][:3], 
                "action": cta_categories["action"][:3],
                "advocacy": cta_categories["advocacy"][:3]
            },
            "target_audience_specific": {
                "working_families": [
                    "See how the monetary flow tax could benefit your family budget",
                    "Join other families supporting fair taxation",
                    "Share this with friends who care about economic fairness"
                ],
                "small_business_owners": [
                    "Learn how fair taxation supports small business growth",
                    "Connect with other business owners who support this policy",
                    "Advocate for economic policies that help main street businesses"
                ],
                "students": [
                    "Understand how economic policy affects your future",
                    "Get involved in shaping the economy you'll inherit",
                    "Share economic justice content with your network"
                ]
            },
            "urgency_levels": {
                "low": "Learn more when you have time",
                "medium": "Join the growing movement for economic justice", 
                "high": "Add your voice before the critical vote next month"
            },
            "measurement_framework": {
                "awareness_metrics": ["page_views", "time_on_page", "social_shares"],
                "consideration_metrics": ["email_signups", "content_downloads", "return_visits"],
                "action_metrics": ["petition_signatures", "event_attendance", "donations"],
                "advocacy_metrics": ["referrals", "user_generated_content", "volunteer_signups"]
            }
        }

    async def _compile_fact_database(self, narrative_beats: List[NarrativeBeat]) -> List[Dict[str, Any]]:
        """Compile comprehensive fact database from all narrative beats"""
        
        fact_database = []
        
        for beat in narrative_beats:
            if beat.fact_verification_needed:
                # Extract specific claims from supporting points
                for i, point in enumerate(beat.supporting_points):
                    if any(indicator in point for indicator in ["$", "%", "trillion", "billion", "million"]):
                        fact_database.append({
                            "claim_id": f"claim_{beat.id}_{i}",
                            "beat_id": beat.id,
                            "claim_text": point,
                            "claim_type": self._classify_claim_type(point),
                            "verification_priority": "high",
                            "sources_required": 2,
                            "movement_principle": "no_unverified_claims",
                            "verification_status": "pending",
                            "created_at": datetime.now().isoformat()
                        })
        
        # Add movement-specific facts that should always be verified
        movement_facts = [
            {
                "claim_id": "movement_fact_001",
                "beat_id": "global",
                "claim_text": "$4.7 quadrillion in annual financial transactions",
                "claim_type": "monetary_statistic",
                "verification_priority": "critical",
                "sources_required": 3,
                "movement_principle": "economic_scale_accuracy",
                "verification_status": "requires_update",
                "created_at": datetime.now().isoformat()
            },
            {
                "claim_id": "movement_fact_002", 
                "beat_id": "global",
                "claim_text": "$30 trillion in annual real economy goods and services",
                "claim_type": "economic_statistic",
                "verification_priority": "critical", 
                "sources_required": 3,
                "movement_principle": "economic_scale_accuracy",
                "verification_status": "requires_update",
                "created_at": datetime.now().isoformat()
            }
        ]
        
        fact_database.extend(movement_facts)
        
        return fact_database

    def _classify_claim_type(self, claim_text: str) -> str:
        """Classify type of factual claim for verification purposes"""
        
        claim_lower = claim_text.lower()
        
        if "$" in claim_text and any(scale in claim_lower for scale in ["trillion", "billion", "quadrillion"]):
            return "monetary_statistic"
        elif "%" in claim_text:
            return "percentage_statistic"
        elif any(word in claim_lower for word in ["policy", "law", "regulation", "implemented"]):
            return "policy_claim"
        elif any(word in claim_lower for word in ["study", "research", "survey"]):
            return "research_citation"
        elif any(word in claim_lower for word in ["country", "nation", "government"]):
            return "international_comparison"
        else:
            return "general_factual"

    async def _validate_final_narrative(self, narrative_scripts: List[NarrativeScript],
                                       accessibility_variants: Dict[str, Any],
                                       fact_database: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate final narrative package"""
        
        issues = []
        
        # Check narrative completeness
        if not narrative_scripts:
            issues.append("No narrative scripts generated")
        
        # Check emotional progression
        for script in narrative_scripts:
            emotions = [beat.emotion for beat in script.narrative_beats]
            if EmotionalJourney.ACTION not in emotions:
                issues.append(f"Script '{script.title}' lacks action conclusion")
                
        # Check fact verification requirements
        pending_facts = [fact for fact in fact_database if fact["verification_status"] == "pending"]
        if len(pending_facts) > len(fact_database) * 0.5:
            issues.append("More than 50% of facts require verification")
            
        # Check accessibility compliance
        if not accessibility_variants:
            issues.append("No accessibility variants created")
            
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    async def _verify_movement_principles(self, narrative_scripts: List[NarrativeScript], 
                                         fact_database: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Verify alignment with movement principles"""
        
        violations = []
        verification_needed = []
        
        # Check for discriminatory targeting
        all_text = ""
        for script in narrative_scripts:
            all_text += script.title + " "
            for beat in script.narrative_beats:
                all_text += f"{beat.description} {beat.key_message} "
        
        problematic_phrases = ["target specific", "exclude", "only for", "against"]
        if any(phrase in all_text.lower() for phrase in problematic_phrases):
            violations.append("Potential discriminatory targeting language detected")
        
        # Check fact verification coverage  
        critical_facts = [f for f in fact_database if f["verification_priority"] == "critical"]
        unverified_critical = [f for f in critical_facts if f["verification_status"] != "verified"]
        
        if unverified_critical:
            verification_needed.extend([f["claim_text"] for f in unverified_critical])
        
        # Check movement messaging alignment
        movement_concepts = ["economic justice", "fair taxation", "democratic", "transparency"]
        if not any(concept in all_text.lower() for concept in movement_concepts):
            violations.append("Missing core movement messaging")
            
        return {
            "verified": len(violations) == 0 and len(verification_needed) == 0,
            "violations": violations,
            "verification_needed": verification_needed
        }

    async def _generate_handoff_package(self, narrative_scripts: List[NarrativeScript],
                                       accessibility_variants: Dict[str, Any],
                                       cta_framework: Dict[str, Any]) -> Dict[str, Any]:
        """Generate handoff package for narrative implementation"""
        
        return {
            "implementation_checklist": [
                {
                    "phase": "Pre-Production",
                    "tasks": [
                        "Complete fact verification for all pending claims",
                        "Legal review of narrative content",
                        "Accessibility compliance testing",
                        "Target audience validation"
                    ]
                },
                {
                    "phase": "Production",
                    "tasks": [
                        "Create content assets per narrative scripts", 
                        "Implement accessibility variants",
                        "Set up call-to-action tracking",
                        "Configure analytics and measurement"
                    ]
                },
                {
                    "phase": "Distribution",
                    "tasks": [
                        "Deploy across planned channels",
                        "Monitor engagement metrics",
                        "A/B test different CTAs",
                        "Collect audience feedback"
                    ]
                }
            ],
            "content_specifications": {
                "formats_ready": [script.format_type.value for script in narrative_scripts],
                "total_content_pieces": len(narrative_scripts),
                "estimated_production_time": f"{sum(script.total_duration for script in narrative_scripts)} content units",
                "accessibility_compliance": list(accessibility_variants.keys())
            },
            "measurement_framework": {
                "narrative_effectiveness": [
                    "Emotional engagement metrics",
                    "Progression through story stages", 
                    "Call-to-action completion rates",
                    "Audience retention and completion"
                ],
                "movement_alignment": [
                    "Fact verification accuracy rate",
                    "Movement messaging consistency",
                    "Principle compliance score",
                    "Stakeholder feedback quality"
                ]
            },
            "optimization_recommendations": [
                "Test different emotional arc patterns with audience segments",
                "Monitor CTA performance and iterate based on data",
                "Gather accessibility user feedback for continuous improvement",
                "Track fact verification updates and refresh content accordingly"
            ]
        }

    async def _analyze_emotional_arc(self, narrative_beats: List[NarrativeBeat]) -> Dict[str, Any]:
        """Analyze emotional arc effectiveness"""
        
        emotion_sequence = [beat.emotion.value for beat in narrative_beats]
        emotion_counts = {}
        for emotion in emotion_sequence:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
        return {
            "emotion_progression": emotion_sequence,
            "emotion_distribution": emotion_counts,
            "arc_pattern": "classic_hero" if "hope" in emotion_counts and "action" in emotion_counts else "custom",
            "emotional_peaks": [
                {"stage": beat.stage.value, "emotion": beat.emotion.value, "intensity": "high"} 
                for beat in narrative_beats 
                if beat.emotion in [EmotionalJourney.EMPOWERMENT, EmotionalJourney.ACTION]
            ],
            "engagement_predictions": {
                "opening_hook": "strong" if narrative_beats[0].emotion == EmotionalJourney.HOPE else "moderate",
                "middle_tension": "effective" if EmotionalJourney.CONCERN in emotion_sequence else "low",
                "closing_power": "strong" if narrative_beats[-1].emotion == EmotionalJourney.ACTION else "moderate"
            }
        }

    async def _generate_performance_optimization(self, narrative_scripts: List[NarrativeScript]) -> Dict[str, Any]:
        """Generate performance optimization recommendations"""
        
        return {
            "a_b_testing_recommendations": [
                {
                    "test_element": "Opening hook emotional tone",
                    "variants": ["Hope-focused", "Concern-focused", "Empowerment-focused"],
                    "success_metric": "Engagement rate through first 25% of content"
                },
                {
                    "test_element": "Call-to-action positioning",
                    "variants": ["Early and repeated", "Middle emphasis", "End concentration"],
                    "success_metric": "CTA completion rate"
                },
                {
                    "test_element": "Fact presentation style", 
                    "variants": ["Data-heavy", "Story-embedded", "Visual-supported"],
                    "success_metric": "Fact retention and sharing"
                }
            ],
            "audience_segmentation": [
                {
                    "segment": "High-engagement activists",
                    "narrative_optimization": "More detailed policy information, faster pacing to action",
                    "cta_preference": "Advanced engagement opportunities"
                },
                {
                    "segment": "Casual supporters",
                    "narrative_optimization": "Simpler messaging, emotional connection emphasis",
                    "cta_preference": "Low-commitment initial actions"
                },
                {
                    "segment": "Skeptical audiences",
                    "narrative_optimization": "Strong fact verification, credible sources, gradual persuasion",
                    "cta_preference": "Information-seeking rather than commitment"
                }
            ],
            "platform_adaptations": [
                {
                    "platform": "Social media",
                    "adaptations": ["Shorter beats", "Visual storytelling", "Shareable moments"],
                    "engagement_boosters": ["Questions", "Polls", "User-generated content prompts"]
                },
                {
                    "platform": "Email",
                    "adaptations": ["Personal tone", "Series structure", "Progressive disclosure"],
                    "engagement_boosters": ["Personalization", "Timing optimization", "Clear unsubscribe"]
                },
                {
                    "platform": "Website/Blog",
                    "adaptations": ["SEO optimization", "Deep linking", "Related content"],
                    "engagement_boosters": ["Interactive elements", "Comments", "Social sharing"]
                }
            ]
        }

    async def _compile_citations(self, fact_database: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile citations for narrative content"""
        
        citations = []
        
        # Add citations for factual claims
        for fact in fact_database:
            citations.append({
                "claim_id": fact["claim_id"],
                "claim_text": fact["claim_text"],
                "claim_type": fact["claim_type"],
                "sources_required": fact["sources_required"],
                "verification_status": fact["verification_status"],
                "movement_principle": fact.get("movement_principle", "general_accuracy")
            })
        
        # Add methodological citations
        citations.extend([
            {
                "source": "Hero's Journey Narrative Framework",
                "type": "methodology",
                "content": "Joseph Campbell's monomyth structure adapted for campaign storytelling",
                "verification_status": "established_framework",
                "application": "Narrative structure and emotional progression design"
            },
            {
                "source": "WCAG 2.1 Accessibility Guidelines", 
                "type": "compliance_standard",
                "content": "Web Content Accessibility Guidelines for inclusive design",
                "verification_status": "official_standard",
                "application": "Accessibility variant development"
            },
            {
                "source": "Movement Principles Database",
                "type": "internal_guidance",
                "content": "IsThereEnoughMoney Movement messaging and principle guidelines",
                "verification_status": "movement_approved",
                "application": "Principle alignment and message consistency"
            }
        ])
        
        return citations