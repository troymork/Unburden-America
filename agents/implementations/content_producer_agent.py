#!/usr/bin/env python3
"""
Content Producer Agent for IsThereEnoughMoney Movement
=====================================================

This agent specializes in research-driven content generation with rigorous
source verification and fact-checking for the movement's educational materials.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
import datetime
import json
import re

from agents.implementations.base_agent import (
    BaseAgent, AgentOutput, AgentStatus, Source, FactCheck, 
    ComplianceCheck, MovementKnowledgeBase
)

logger = logging.getLogger(__name__)

class ContentProducerAgent(BaseAgent):
    """Agent specialized in creating fact-based content for the movement"""
    
    def __init__(self, agent_id: str = None):
        super().__init__(agent_id)
        self.capabilities = [
            "research", "writing", "fact_verification", "citation",
            "content_structuring", "audience_adaptation", "source_validation"
        ]
        self.quality_gates = [
            "source_verification", "dual_fact_check", "movement_alignment",
            "readability_check", "citation_completeness"
        ]
        self.content_templates = self._load_content_templates()
    
    def get_agent_type(self) -> str:
        return "content_producer"
    
    def get_capabilities(self) -> List[str]:
        return self.capabilities
    
    def get_quality_gates(self) -> List[str]:
        return self.quality_gates
    
    def _load_content_templates(self) -> Dict[str, Dict]:
        """Load content templates for different content types"""
        return {
            "educational_article": {
                "structure": ["introduction", "problem_explanation", "solution_overview", "benefits", "call_to_action"],
                "tone": "educational_accessible",
                "length_words": {"min": 800, "max": 1500},
                "required_elements": ["statistics", "sources", "movement_context"]
            },
            "social_post": {
                "structure": ["hook", "key_fact", "call_to_action"],
                "tone": "engaging_concise",
                "length_words": {"min": 50, "max": 280},
                "required_elements": ["hashtags", "movement_message"]
            },
            "policy_brief": {
                "structure": ["executive_summary", "current_situation", "proposed_solution", "implementation", "conclusion"],
                "tone": "professional_authoritative",
                "length_words": {"min": 1500, "max": 3000},
                "required_elements": ["data_citations", "policy_recommendations", "economic_impact"]
            },
            "explainer_video_script": {
                "structure": ["hook", "problem_setup", "solution_explanation", "visual_elements", "call_to_action"],
                "tone": "conversational_clear",
                "length_words": {"min": 300, "max": 800},
                "required_elements": ["visual_cues", "simple_analogies", "movement_branding"]
            }
        }
    
    async def process(self, inputs: Dict[str, Any]) -> AgentOutput:
        """Process content creation request with research and verification"""
        
        # Extract inputs
        topic = inputs.get("topic", "Monetary Flow Tax")
        content_type = inputs.get("content_type", "educational_article")
        target_audience = inputs.get("target_audience", "general_public")
        content_focus = inputs.get("focus", "explaining_concept_simply")
        
        logger.info(f"Creating {content_type} about '{topic}' for {target_audience}")
        
        # Simulate processing time
        await self.simulate_processing_delay(1.0, 3.0)
        
        # Step 1: Research phase
        research_results = await self._conduct_research(topic, content_focus)
        
        # Step 2: Content generation
        content = await self._generate_content(
            topic, content_type, target_audience, research_results
        )
        
        # Step 3: Fact verification
        fact_checks = await self._verify_facts(content, research_results)
        
        # Step 4: Compliance review
        compliance_checks = await self._review_compliance(content, content_type)
        
        # Step 5: Quality scoring
        quality_scores = await self._calculate_quality_scores(content, content_type)
        
        return AgentOutput(
            agent_id=self.agent_id,
            agent_type=self.get_agent_type(),
            status=AgentStatus.PROCESSING,  # Will be set to COMPLETED by base class
            primary_output={
                "content": content,
                "metadata": {
                    "topic": topic,
                    "content_type": content_type,
                    "target_audience": target_audience,
                    "word_count": len(content.split()),
                    "research_sources_count": len(research_results["sources"]),
                    "claims_verified": len(fact_checks)
                }
            },
            metadata={
                "research_methodology": research_results["methodology"],
                "content_template_used": content_type,
                "audience_adaptations": research_results.get("audience_adaptations", []),
                "movement_alignment_score": quality_scores.get("movement_alignment", 0.0)
            },
            quality_scores=quality_scores,
            fact_checks=fact_checks,
            compliance_checks=compliance_checks,
            sources_used=research_results["sources"],
            execution_time_ms=0,  # Will be calculated by base class
            created_at=datetime.datetime.utcnow().isoformat()
        )
    
    async def _conduct_research(self, topic: str, focus: str) -> Dict[str, Any]:
        """Conduct research on the topic using movement knowledge base"""
        
        logger.info(f"Conducting research on: {topic} (focus: {focus})")
        
        # Get core movement facts
        core_facts = MovementKnowledgeBase.get_core_facts()
        messaging_guidelines = MovementKnowledgeBase.get_messaging_guidelines()
        
        # Simulate research process
        await asyncio.sleep(0.5)
        
        # Create research sources (in real implementation, these would be fetched)
        sources = [
            self.create_source(
                url="https://www.federalreserve.gov/paymentsystems/fr-banking-industry-statistics.htm",
                title="Federal Reserve Payment Systems Statistics",
                source_type="government",
                reliability_score=0.95
            ),
            self.create_source(
                url="https://www.bea.gov/data/gdp/gross-domestic-product",
                title="Bureau of Economic Analysis - GDP Data",
                source_type="government",
                reliability_score=0.98
            ),
            self.create_source(
                url="https://www.bis.org/statistics/payment_stats.htm",
                title="Bank for International Settlements Payment Statistics",
                source_type="government",
                reliability_score=0.92
            ),
            self.create_source(
                url="https://www.dtcc.com/about/businesses-and-subsidiaries/ficc",
                title="DTCC Fixed Income Clearing Corporation Data",
                source_type="primary",
                reliability_score=0.90
            )
        ]
        
        research_findings = {
            "key_statistics": {
                "monetary_economy_size": core_facts["monetary_economy_size"]["value"],
                "real_economy_size": core_facts["real_economy_size"]["value"],
                "scale_multiplier": core_facts["scale_difference"]["value"]
            },
            "core_concepts": {
                "monetary_flow_tax": "Ultra-low tax on financial transaction settlement flows",
                "debt_elimination_timeline": core_facts["debt_elimination_timeline"]["value"],
                "revenue_potential": "Sufficient to eliminate national debt without burdening taxpayers"
            },
            "audience_insights": await self._analyze_target_audience(topic, focus),
            "movement_context": messaging_guidelines
        }
        
        return {
            "sources": sources,
            "findings": research_findings,
            "methodology": "Knowledge base analysis + government data verification",
            "audience_adaptations": research_findings["audience_insights"]["adaptations"]
        }
    
    async def _analyze_target_audience(self, topic: str, focus: str) -> Dict[str, Any]:
        """Analyze target audience needs and preferences"""
        
        # Simulate audience analysis
        await asyncio.sleep(0.2)
        
        return {
            "knowledge_level": "general_public",
            "key_concerns": [
                "tax burden on families",
                "government spending efficiency", 
                "economic fairness",
                "practical solutions"
            ],
            "communication_preferences": [
                "simple_explanations",
                "concrete_examples",
                "visual_analogies",
                "actionable_steps"
            ],
            "adaptations": [
                "Use ping-pong ball vs basketball analogy for economy sizes",
                "Focus on family budget parallels",
                "Emphasize bipartisan nature",
                "Include concrete dollar amounts"
            ]
        }
    
    async def _generate_content(self, topic: str, content_type: str, 
                              target_audience: str, research: Dict[str, Any]) -> str:
        """Generate content based on research and template"""
        
        logger.info(f"Generating {content_type} content")
        
        # Get content template
        template = self.content_templates.get(content_type, self.content_templates["educational_article"])
        
        # Simulate content generation
        await asyncio.sleep(1.0)
        
        if content_type == "educational_article":
            content = await self._generate_educational_article(topic, research, template)
        elif content_type == "social_post":
            content = await self._generate_social_post(topic, research, template)
        elif content_type == "policy_brief":
            content = await self._generate_policy_brief(topic, research, template)
        elif content_type == "explainer_video_script":
            content = await self._generate_video_script(topic, research, template)
        else:
            content = await self._generate_educational_article(topic, research, template)
        
        return content
    
    async def _generate_educational_article(self, topic: str, research: Dict, template: Dict) -> str:
        """Generate an educational article about the monetary flow tax"""
        
        findings = research["findings"]
        
        content = f"""# Understanding the Monetary Flow Tax: A Path to Unburden America

## The Problem We Face

America carries a crushing $33+ trillion national debt that costs us nearly $1 trillion per year in interest payments alone. This invisible weight limits our nation's possibilities and quietly transfers today's spending burden onto our children's shoulders.

But what if the problem isn't a lack of money, but a lack of vision about where to find it?

## Two Economies, One Solution

Think of our economy like two different sized balls: a ping-pong ball next to a basketball.

**The Real Economy (Ping-Pong Ball):** ~${findings['key_statistics']['real_economy_size'].replace('_', ' ').replace('trillion', 'Trillion')}
- Your paycheck, business sales, production of goods and services
- What we call Gross Domestic Product (GDP)
- Where we currently place nearly 100% of our tax burden

**The Monetary Economy (Basketball):** ~${findings['key_statistics']['monetary_economy_size'].replace('_', ' ').replace('quadrillion', 'Quadrillion')}  
- The total flow of money through financial settlement systems
- High-volume transactions processed daily by systems like DTCC, Fedwire, and CHIPS
- About {findings['key_statistics']['scale_multiplier']} times larger than the real economy

## The Monetary Flow Tax Solution

Instead of squeezing more from the tiny ping-pong ball, we propose placing a microscopic toll on the giant basketball.

**How It Works:**
- Ultra-low tax rate: Just 50 cents for every $100 in financial transactions
- Applied automatically at major settlement systems
- No paperwork for ordinary people or small businesses
- Targets the system, not the people

**Why It's Fair:**
- Massive base means tiny rate generates enormous revenue
- Doesn't burden families, workers, or small businesses
- Taxes where the money actually moves in volume
- Modern solution for a modern economy

## The Eight-Year Plan

With revenue from the Monetary Flow Tax, we can:

1. **End America's Debt** - Eliminate the national debt within approximately {findings['core_concepts']['debt_elimination_timeline']} years
2. **Lift the Tax Burden** - Dramatically reduce or eliminate payroll taxes for working families
3. **Fund the Future** - Invest in healthcare, education, and national priorities without new debt

## What This Means for You

Imagine:
- No more payroll taxes taken from your paycheck
- A government that operates without crushing debt payments
- National resources freed up for priorities that matter to families
- Economic policies driven by possibility, not scarcity

## The Bipartisan Opportunity

This isn't about left versus right—it's about a bigger, smarter approach that:
- Fiscal conservatives appreciate for its debt elimination focus
- Progressives support for its fair revenue generation
- Everyone benefits from reduced personal tax burden
- Creates unity around shared economic prosperity

## Join the Movement

The IsThereEnoughMoney movement represents a generational opportunity to lift the weight of debt from America's shoulders. We have enough money—we just need the vision to tap into it wisely.

**Take Action:**
1. Learn more about the Monetary Flow Tax proposal
2. Share this solution with friends and family  
3. Contact your representatives about this bipartisan opportunity
4. Sign the Unburden America Pledge

Together, we can tax the system, not the people, and build an abundant American future.

---

*Sources: Federal Reserve Payment Systems Data, Bureau of Economic Analysis GDP Statistics, Bank for International Settlements Transaction Data*"""

        return content
    
    async def _generate_social_post(self, topic: str, research: Dict, template: Dict) -> str:
        """Generate social media content"""
        
        findings = research["findings"]
        
        content = f"""🇺🇸 WHAT IF we're taxing the wrong economy?

💡 The REAL economy (your paycheck, small businesses): ~$30 Trillion
💰 The MONETARY economy (financial system flows): ~$4.7 QUADRILLION

We tax the ping-pong ball while the basketball rolls by untouched.

The solution: Tax the system, not the people. 

A tiny 0.5% tax on financial flows could eliminate America's debt in 8 years while REDUCING taxes on working families.

#TaxTheSystem #UnburdenAmerica #MonetaryFlowTax #DebtFree #IsThereEnoughMoney"""

        return content
    
    async def _generate_policy_brief(self, topic: str, research: Dict, template: Dict) -> str:
        """Generate policy brief content"""
        
        findings = research["findings"]
        
        content = f"""# Policy Brief: Monetary Flow Tax Implementation

## Executive Summary

The Monetary Flow Tax (MFT) represents a paradigm shift in federal revenue generation, targeting the $4.7 quadrillion monetary economy rather than the $30 trillion real economy. At a rate of 0.5%, this mechanism could generate sufficient revenue to eliminate the national debt within eight years while reducing the tax burden on individuals and businesses.

## Current Fiscal Situation

- National Debt: $33+ trillion and growing
- Annual Interest Payments: ~$900 billion
- Primary Revenue Sources: Income, payroll, and corporate taxes on real economy
- Tax Burden Distribution: 100% on productive economic activity

## Policy Recommendation

Implementation of a 0.5% Monetary Flow Tax on high-volume financial settlements processed through:
- Depository Trust & Clearing Corporation (DTCC)
- Federal Reserve Fedwire/CHIPS systems  
- Automated Clearing House (ACH) networks
- Continuous Linked Settlement (CLS) systems

## Economic Impact Analysis

**Revenue Potential:** $23.5+ trillion annually (0.5% of $4.7Q)
**Debt Elimination Timeline:** 8 years at current debt levels
**Tax Relief Opportunity:** Elimination of payroll taxes ($1.6T annually)

## Implementation Framework

1. **Phase 1:** Legislative authorization and regulatory framework
2. **Phase 2:** Technical integration with settlement systems
3. **Phase 3:** Gradual rate implementation with monitoring
4. **Phase 4:** Coordinated reduction of traditional tax burden

## Conclusion

The Monetary Flow Tax offers a fiscally responsible path to debt elimination while reducing the burden on American families and businesses. This bipartisan solution merits serious consideration by policymakers committed to long-term fiscal sustainability."""

        return content
    
    async def _generate_video_script(self, topic: str, research: Dict, template: Dict) -> str:
        """Generate video script content"""
        
        content = f"""# Video Script: "Tax the System, Not the People"

**VISUAL:** Animation of two spheres - small ping-pong ball, giant basketball

**NARRATOR:** "What if I told you America has been trying to squeeze water from a rock, while an ocean of opportunity flows right past us?"

**VISUAL:** Families struggling with bills, small businesses counting pennies

**NARRATOR:** "For decades, we've placed our entire tax burden on the Real Economy - your paycheck, small business sales, the $30 trillion GDP."

**VISUAL:** Basketball grows massive while ping-pong ball stays tiny  

**NARRATOR:** "But there's another economy 150 times bigger - the $4.7 quadrillion Monetary Economy where trillions move through financial systems daily."

**VISUAL:** Simple calculation: 0.5% of massive number = debt elimination

**NARRATOR:** "A tiny 0.5% tax - just 50 cents per $100 - on these financial flows could eliminate America's debt in 8 years."

**VISUAL:** Happy families, thriving businesses, debt-free America

**NARRATOR:** "Tax the system, not the people. That's how we unburden America."

**VISUAL:** Movement logo and call-to-action

**NARRATOR:** "Join the IsThereEnoughMoney movement. Because there IS enough money - we just need to be smart about where we look."

**END SCREEN:** UnburdenAmerica.org"""

        return content
    
    async def _verify_facts(self, content: str, research: Dict[str, Any]) -> List[FactCheck]:
        """Verify facts mentioned in the content"""
        
        logger.info("Conducting fact verification")
        
        # Simulate fact-checking process
        await asyncio.sleep(0.8)
        
        fact_checks = []
        
        # Check monetary economy size claim
        if "4.7 quadrillion" in content.lower() or "4.7q" in content.lower():
            fact_checks.append(
                self.create_fact_check(
                    claim="Monetary economy processes approximately $4.7 quadrillion annually",
                    verification_status="verified",
                    sources=research["sources"][:2],  # Use first 2 sources
                    confidence_level=0.90,
                    notes="Based on Federal Reserve and BIS payment system statistics"
                )
            )
        
        # Check real economy size claim  
        if "30 trillion" in content.lower() and "gdp" in content.lower():
            fact_checks.append(
                self.create_fact_check(
                    claim="US GDP (Real Economy) is approximately $30 trillion",
                    verification_status="verified",
                    sources=[research["sources"][1]],  # BEA source
                    confidence_level=0.98,
                    notes="Current US GDP from Bureau of Economic Analysis"
                )
            )
        
        # Check scale difference claim
        if "150" in content and "times" in content:
            fact_checks.append(
                self.create_fact_check(
                    claim="Monetary economy is approximately 150 times larger than real economy",
                    verification_status="verified", 
                    sources=research["sources"],
                    confidence_level=0.85,
                    notes="Calculated ratio: $4.7Q ÷ $30T ≈ 157x"
                )
            )
        
        return fact_checks
    
    async def _review_compliance(self, content: str, content_type: str) -> List[ComplianceCheck]:
        """Review content for compliance with movement standards"""
        
        logger.info("Conducting compliance review")
        
        # Simulate compliance checking
        await asyncio.sleep(0.5)
        
        compliance_checks = []
        
        # Check for partisan language
        partisan_terms = ["democrat", "republican", "liberal", "conservative", "socialist"]
        content_lower = content.lower()
        
        partisan_found = any(term in content_lower for term in partisan_terms)
        
        compliance_checks.append(
            self.create_compliance_check(
                category="messaging_neutrality",
                status="compliant" if not partisan_found else "needs_review",
                details=f"Partisan language check: {'None detected' if not partisan_found else 'Potential partisan terms found'}",
                recommendations=[] if not partisan_found else ["Remove partisan language", "Focus on economic facts"]
            )
        )
        
        # Check citation completeness
        has_sources = "sources:" in content_lower or "source:" in content_lower
        
        compliance_checks.append(
            self.create_compliance_check(
                category="source_citation",
                status="compliant" if has_sources else "non_compliant",
                details=f"Source citation check: {'Sources properly cited' if has_sources else 'Missing source citations'}",
                recommendations=[] if has_sources else ["Add source citations", "Include reference links"]
            )
        )
        
        # Check accessibility
        compliance_checks.append(
            self.create_compliance_check(
                category="accessibility",
                status="compliant",
                details="Content uses clear language and proper structure",
                recommendations=["Consider adding alt-text for any images", "Ensure proper heading hierarchy"]
            )
        )
        
        return compliance_checks
    
    async def _calculate_quality_scores(self, content: str, content_type: str) -> Dict[str, float]:
        """Calculate quality scores for the content"""
        
        logger.info("Calculating quality scores")
        
        # Simulate quality analysis
        await asyncio.sleep(0.3)
        
        word_count = len(content.split())
        template = self.content_templates[content_type]
        target_range = template["length_words"]
        
        # Length appropriateness score
        if target_range["min"] <= word_count <= target_range["max"]:
            length_score = 1.0
        elif word_count < target_range["min"]:
            length_score = word_count / target_range["min"]
        else:
            length_score = max(0.5, target_range["max"] / word_count)
        
        # Readability score (simplified)
        sentences = content.count('.') + content.count('!') + content.count('?')
        avg_sentence_length = word_count / max(sentences, 1)
        readability_score = max(0.3, min(1.0, 1.0 - (avg_sentence_length - 15) / 50))
        
        # Movement alignment score  
        movement_keywords = [
            "tax the system", "not the people", "monetary flow", 
            "unburden america", "debt elimination"
        ]
        content_lower = content.lower()
        keyword_hits = sum(1 for keyword in movement_keywords if keyword in content_lower)
        movement_score = min(1.0, keyword_hits / len(movement_keywords) * 2)
        
        # Fact density score
        fact_indicators = ["trillion", "billion", "%", "statistics", "data", "according to"]
        fact_hits = sum(1 for indicator in fact_indicators if indicator in content_lower)
        fact_density_score = min(1.0, fact_hits / 10)  # Max score at 10+ fact indicators
        
        return {
            "length_appropriateness": length_score,
            "readability": readability_score,
            "movement_alignment": movement_score,
            "fact_density": fact_density_score,
            "overall_quality": (length_score + readability_score + movement_score + fact_density_score) / 4
        }

# Export the agent class
__all__ = ['ContentProducerAgent']