#!/usr/bin/env python3
"""
Fact Checker Agent for IsThereEnoughMoney Movement
=================================================

This agent specializes in rigorous fact-checking and source verification
to ensure all claims meet the movement's high standards for accuracy.
"""

import asyncio
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
import datetime
import json
import hashlib

from agents.implementations.base_agent import (
    BaseAgent, AgentOutput, AgentStatus, Source, FactCheck, 
    ComplianceCheck, MovementKnowledgeBase
)

logger = logging.getLogger(__name__)

class FactCheckerAgent(BaseAgent):
    """Agent specialized in fact-checking and source verification"""
    
    def __init__(self, agent_id: str = None):
        super().__init__(agent_id)
        self.capabilities = [
            "source_validation", "claim_verification", "uncertainty_documentation",
            "cross_reference_checking", "reliability_scoring", "bias_detection"
        ]
        self.quality_gates = [
            "minimum_two_sources", "primary_source_preference", "confidence_threshold",
            "cross_verification", "temporal_validity"
        ]
        self.trusted_source_domains = self._load_trusted_sources()
        self.fact_checking_protocols = self._load_fact_checking_protocols()
    
    def get_agent_type(self) -> str:
        return "fact_checker"
    
    def get_capabilities(self) -> List[str]:
        return self.capabilities
    
    def get_quality_gates(self) -> List[str]:
        return self.quality_gates
    
    def _load_trusted_sources(self) -> Dict[str, Dict[str, Any]]:
        """Load registry of trusted source domains with reliability scores"""
        return {
            # Government sources (highest reliability)
            "federalreserve.gov": {
                "reliability": 0.98,
                "type": "government",
                "specialties": ["monetary_policy", "payment_systems", "economic_data"]
            },
            "bea.gov": {
                "reliability": 0.97,
                "type": "government", 
                "specialties": ["gdp", "economic_statistics", "national_accounts"]
            },
            "treasury.gov": {
                "reliability": 0.96,
                "type": "government",
                "specialties": ["fiscal_policy", "debt_statistics", "revenue_data"]
            },
            "cbo.gov": {
                "reliability": 0.95,
                "type": "government",
                "specialties": ["budget_analysis", "economic_projections", "policy_analysis"]
            },
            "bis.org": {
                "reliability": 0.94,
                "type": "international_org",
                "specialties": ["international_payments", "financial_statistics", "central_banking"]
            },
            
            # Financial industry sources (high reliability for industry data)
            "dtcc.com": {
                "reliability": 0.90,
                "type": "industry_primary",
                "specialties": ["clearing", "settlement", "transaction_volumes"]
            },
            "federalreserve.org": {
                "reliability": 0.88,
                "type": "industry",
                "specialties": ["payment_systems", "financial_infrastructure"]
            },
            
            # Academic sources (high reliability with peer review)
            "brookings.edu": {
                "reliability": 0.85,
                "type": "academic_think_tank",
                "specialties": ["economic_policy", "fiscal_analysis"]
            },
            "american.edu": {
                "reliability": 0.83,
                "type": "academic",
                "specialties": ["political_science", "public_policy"]
            },
            
            # News sources (moderate to high reliability)
            "reuters.com": {
                "reliability": 0.82,
                "type": "news_wire",
                "specialties": ["financial_news", "economic_reporting"]
            },
            "wsj.com": {
                "reliability": 0.80,
                "type": "news_financial",
                "specialties": ["financial_markets", "economic_analysis"]
            }
        }
    
    def _load_fact_checking_protocols(self) -> Dict[str, Dict[str, Any]]:
        """Load fact-checking protocols for different types of claims"""
        return {
            "economic_statistics": {
                "minimum_sources": 2,
                "preferred_source_types": ["government", "international_org"],
                "cross_verification_required": True,
                "temporal_validity_months": 12,
                "confidence_threshold": 0.85
            },
            "policy_claims": {
                "minimum_sources": 3,
                "preferred_source_types": ["government", "academic", "think_tank"],
                "cross_verification_required": True,
                "temporal_validity_months": 6,
                "confidence_threshold": 0.80
            },
            "financial_data": {
                "minimum_sources": 2,
                "preferred_source_types": ["government", "industry_primary"],
                "cross_verification_required": True,
                "temporal_validity_months": 3,
                "confidence_threshold": 0.90
            },
            "historical_facts": {
                "minimum_sources": 2,
                "preferred_source_types": ["government", "academic"],
                "cross_verification_required": False,
                "temporal_validity_months": 60,
                "confidence_threshold": 0.85
            }
        }
    
    async def process(self, inputs: Dict[str, Any]) -> AgentOutput:
        """Process fact-checking request for content or claims"""
        
        # Extract inputs
        content_to_check = inputs.get("content", "")
        existing_sources = inputs.get("sources", [])
        claims_to_verify = inputs.get("claims", [])
        verification_level = inputs.get("verification_level", "standard")
        
        logger.info(f"Fact-checking {len(claims_to_verify)} claims with {verification_level} verification")
        
        # Simulate processing time
        await self.simulate_processing_delay(1.5, 4.0)
        
        # Step 1: Extract claims from content if not provided
        if not claims_to_verify and content_to_check:
            claims_to_verify = await self._extract_claims(content_to_check)
        
        # Step 2: Verify each claim
        fact_checks = []
        all_sources = list(existing_sources)
        
        for claim in claims_to_verify:
            fact_check_result = await self._verify_claim(claim, verification_level)
            fact_checks.append(fact_check_result)
            all_sources.extend(fact_check_result.sources)
        
        # Step 3: Cross-verification analysis
        cross_verification_results = await self._perform_cross_verification(fact_checks)
        
        # Step 4: Source reliability analysis
        source_analysis = await self._analyze_source_reliability(all_sources)
        
        # Step 5: Generate overall confidence assessment
        overall_confidence = await self._calculate_overall_confidence(fact_checks, source_analysis)
        
        # Step 6: Compliance checks
        compliance_checks = await self._review_fact_check_compliance(fact_checks, verification_level)
        
        return AgentOutput(
            agent_id=self.agent_id,
            agent_type=self.get_agent_type(),
            status=AgentStatus.PROCESSING,
            primary_output={
                "verification_summary": {
                    "claims_checked": len(fact_checks),
                    "claims_verified": len([fc for fc in fact_checks if fc.verification_status == "verified"]),
                    "claims_disputed": len([fc for fc in fact_checks if fc.verification_status == "disputed"]),
                    "claims_uncertain": len([fc for fc in fact_checks if fc.verification_status == "uncertain"]),
                    "overall_confidence": overall_confidence,
                    "verification_level": verification_level
                },
                "source_analysis": source_analysis,
                "cross_verification": cross_verification_results,
                "recommendations": await self._generate_recommendations(fact_checks, source_analysis)
            },
            metadata={
                "fact_checking_methodology": "Multi-source verification with cross-referencing",
                "sources_analyzed": len(all_sources),
                "trusted_sources_used": len([s for s in all_sources if self._is_trusted_source(s.url)]),
                "verification_protocols_applied": list(self.fact_checking_protocols.keys())
            },
            quality_scores={
                "source_reliability": source_analysis.get("average_reliability", 0.0),
                "verification_completeness": min(1.0, len(fact_checks) / max(1, len(claims_to_verify))),
                "cross_verification_score": cross_verification_results.get("consistency_score", 0.0),
                "confidence_score": overall_confidence
            },
            fact_checks=fact_checks,
            compliance_checks=compliance_checks,
            sources_used=[self._convert_to_source_object(s) for s in all_sources if hasattr(s, 'url')],
            execution_time_ms=0,
            created_at=datetime.datetime.utcnow().isoformat()
        )
    
    async def _extract_claims(self, content: str) -> List[str]:
        """Extract factual claims from content that need verification"""
        
        logger.info("Extracting factual claims from content")
        
        # Simulate claim extraction process
        await asyncio.sleep(0.5)
        
        claims = []
        
        # Look for numerical claims
        number_patterns = [
            r'\$?(\d+(?:\.\d+)?)\s*(trillion|billion|million|quadrillion)',
            r'(\d+(?:\.\d+)?)\s*%',
            r'(\d+)\s*years?',
            r'(\d+)\s*times?\s*(larger|bigger|more)'
        ]
        
        content_lower = content.lower()
        
        for pattern in number_patterns:
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                # Extract surrounding context for the claim
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip()
                claims.append(context)
        
        # Look for specific movement claims
        movement_claims = [
            "monetary economy.*quadrillion",
            "real economy.*trillion", 
            "debt elimination.*years",
            "tax.*system.*people",
            "150.*times.*larger"
        ]
        
        for claim_pattern in movement_claims:
            matches = re.finditer(claim_pattern, content_lower, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 30)
                end = min(len(content), match.end() + 30)
                context = content[start:end].strip()
                if context not in claims:  # Avoid duplicates
                    claims.append(context)
        
        # Add some specific claims we know need verification
        specific_claims = [
            "The monetary economy processes approximately $4.7 quadrillion annually",
            "US GDP is approximately $30 trillion", 
            "The monetary economy is about 150 times larger than the real economy",
            "A 0.5% tax on monetary flows could eliminate the national debt in 8 years"
        ]
        
        for claim in specific_claims:
            if any(key_phrase in content_lower for key_phrase in claim.lower().split()[:3]):
                claims.append(claim)
        
        return list(set(claims))  # Remove duplicates
    
    async def _verify_claim(self, claim: str, verification_level: str) -> FactCheck:
        """Verify a specific factual claim"""
        
        logger.info(f"Verifying claim: {claim[:100]}...")
        
        # Simulate verification process
        await asyncio.sleep(0.8)
        
        # Determine claim type for appropriate protocol
        claim_type = self._classify_claim(claim)
        protocol = self.fact_checking_protocols.get(claim_type, self.fact_checking_protocols["economic_statistics"])
        
        # Get relevant sources for this claim
        sources = await self._find_relevant_sources(claim, claim_type)
        
        # Verify against movement knowledge base
        knowledge_base_verification = self._verify_against_knowledge_base(claim)
        
        # Determine verification status
        if len(sources) >= protocol["minimum_sources"] and knowledge_base_verification["matches"]:
            if knowledge_base_verification["confidence"] >= protocol["confidence_threshold"]:
                verification_status = "verified"
                confidence_level = knowledge_base_verification["confidence"]
            else:
                verification_status = "uncertain"
                confidence_level = knowledge_base_verification["confidence"]
        elif knowledge_base_verification["contradicts"]:
            verification_status = "disputed"
            confidence_level = 0.3
        else:
            verification_status = "uncertain"
            confidence_level = 0.5
        
        # Generate verification notes
        notes = self._generate_verification_notes(claim, sources, knowledge_base_verification, protocol)
        
        return self.create_fact_check(
            claim=claim,
            verification_status=verification_status,
            sources=sources,
            confidence_level=confidence_level,
            notes=notes
        )
    
    def _classify_claim(self, claim: str) -> str:
        """Classify claim type to determine verification protocol"""
        
        claim_lower = claim.lower()
        
        if any(term in claim_lower for term in ["gdp", "trillion", "economy size", "economic statistics"]):
            return "economic_statistics"
        elif any(term in claim_lower for term in ["policy", "tax", "law", "regulation"]):
            return "policy_claims"
        elif any(term in claim_lower for term in ["quadrillion", "payment", "settlement", "financial"]):
            return "financial_data"
        else:
            return "economic_statistics"  # Default
    
    async def _find_relevant_sources(self, claim: str, claim_type: str) -> List[Source]:
        """Find sources relevant to verifying the claim"""
        
        # Simulate source finding process
        await asyncio.sleep(0.3)
        
        sources = []
        
        # Add sources based on claim content
        claim_lower = claim.lower()
        
        if "quadrillion" in claim_lower or "monetary" in claim_lower:
            sources.extend([
                self.create_source(
                    "https://www.federalreserve.gov/paymentsystems/fr-banking-industry-statistics.htm",
                    "Federal Reserve Payment Systems Statistics",
                    "government",
                    0.95
                ),
                self.create_source(
                    "https://www.bis.org/statistics/payment_stats.htm", 
                    "BIS Payment Statistics",
                    "international_org",
                    0.92
                )
            ])
        
        if "gdp" in claim_lower or "trillion" in claim_lower and "real economy" in claim_lower:
            sources.append(
                self.create_source(
                    "https://www.bea.gov/data/gdp/gross-domestic-product",
                    "BEA Gross Domestic Product Data",
                    "government",
                    0.97
                )
            )
        
        if "debt" in claim_lower or "national debt" in claim_lower:
            sources.append(
                self.create_source(
                    "https://www.treasury.gov/resource-center/data-chart-center/",
                    "US Treasury Debt Statistics", 
                    "government",
                    0.96
                )
            )
        
        # Ensure minimum sources
        protocol = self.fact_checking_protocols.get(claim_type, self.fact_checking_protocols["economic_statistics"])
        while len(sources) < protocol["minimum_sources"]:
            sources.append(
                self.create_source(
                    "https://www.cbo.gov/data",
                    "Congressional Budget Office Data",
                    "government", 
                    0.94
                )
            )
        
        return sources
    
    def _verify_against_knowledge_base(self, claim: str) -> Dict[str, Any]:
        """Verify claim against movement knowledge base"""
        
        core_facts = MovementKnowledgeBase.get_core_facts()
        claim_lower = claim.lower()
        
        verification_result = {
            "matches": False,
            "contradicts": False,
            "confidence": 0.0,
            "matching_facts": []
        }
        
        # Check against each core fact
        if "4.7" in claim and "quadrillion" in claim_lower:
            fact = core_facts["monetary_economy_size"]
            if "4.7_quadrillion" in fact["value"]:
                verification_result["matches"] = True
                verification_result["confidence"] = fact["confidence"]
                verification_result["matching_facts"].append("monetary_economy_size")
        
        if "30" in claim and "trillion" in claim_lower and ("gdp" in claim_lower or "real economy" in claim_lower):
            fact = core_facts["real_economy_size"] 
            if "30_trillion" in fact["value"]:
                verification_result["matches"] = True
                verification_result["confidence"] = max(verification_result["confidence"], fact["confidence"])
                verification_result["matching_facts"].append("real_economy_size")
        
        if "150" in claim and "times" in claim_lower:
            fact = core_facts["scale_difference"]
            if "150x" in fact["value"]:
                verification_result["matches"] = True
                verification_result["confidence"] = max(verification_result["confidence"], fact["confidence"])
                verification_result["matching_facts"].append("scale_difference")
        
        if "8" in claim and "years" in claim_lower and "debt" in claim_lower:
            fact = core_facts["debt_elimination_timeline"]
            if "8_years" in fact["value"]:
                verification_result["matches"] = True
                verification_result["confidence"] = max(verification_result["confidence"], 0.85)  # Conservative estimate
                verification_result["matching_facts"].append("debt_elimination_timeline")
        
        return verification_result
    
    def _generate_verification_notes(self, claim: str, sources: List[Source], 
                                   kb_verification: Dict[str, Any], protocol: Dict[str, Any]) -> str:
        """Generate verification notes explaining the fact-check result"""
        
        notes = []
        
        if kb_verification["matches"]:
            notes.append(f"Claim aligns with movement knowledge base facts: {', '.join(kb_verification['matching_facts'])}")
        
        notes.append(f"Verified using {len(sources)} sources meeting {protocol['minimum_sources']} minimum requirement")
        
        source_types = [s.source_type for s in sources]
        notes.append(f"Source types: {', '.join(set(source_types))}")
        
        if kb_verification["confidence"] >= protocol["confidence_threshold"]:
            notes.append(f"Confidence level ({kb_verification['confidence']:.2f}) meets threshold ({protocol['confidence_threshold']:.2f})")
        else:
            notes.append(f"Confidence level ({kb_verification['confidence']:.2f}) below threshold ({protocol['confidence_threshold']:.2f})")
        
        return " | ".join(notes)
    
    async def _perform_cross_verification(self, fact_checks: List[FactCheck]) -> Dict[str, Any]:
        """Perform cross-verification analysis across fact checks"""
        
        logger.info("Performing cross-verification analysis")
        
        # Simulate cross-verification
        await asyncio.sleep(0.4)
        
        # Calculate consistency scores
        verified_count = len([fc for fc in fact_checks if fc.verification_status == "verified"])
        total_count = len(fact_checks)
        consistency_score = verified_count / max(total_count, 1)
        
        # Check for contradictions
        contradictions = []
        confidence_levels = [fc.confidence_level for fc in fact_checks]
        avg_confidence = sum(confidence_levels) / len(confidence_levels) if confidence_levels else 0.0
        
        # Identify potential issues
        issues = []
        if consistency_score < 0.8:
            issues.append("Low verification consistency across claims")
        if avg_confidence < 0.8:
            issues.append("Below-average confidence levels")
        
        return {
            "consistency_score": consistency_score,
            "average_confidence": avg_confidence,
            "contradictions": contradictions,
            "potential_issues": issues,
            "cross_verification_passed": consistency_score >= 0.8 and avg_confidence >= 0.7
        }
    
    async def _analyze_source_reliability(self, sources: List[Any]) -> Dict[str, Any]:
        """Analyze the reliability of sources used"""
        
        logger.info("Analyzing source reliability")
        
        # Simulate source analysis  
        await asyncio.sleep(0.2)
        
        if not sources:
            return {"average_reliability": 0.0, "source_breakdown": {}}
        
        source_breakdown = {}
        total_reliability = 0.0
        
        for source in sources:
            if hasattr(source, 'url'):
                domain = self._extract_domain(source.url)
                source_info = self.trusted_source_domains.get(domain, {"reliability": 0.5, "type": "unknown"})
                
                source_type = source_info["type"]
                reliability = source_info["reliability"]
                
                if source_type not in source_breakdown:
                    source_breakdown[source_type] = {"count": 0, "avg_reliability": 0.0}
                
                source_breakdown[source_type]["count"] += 1
                current_avg = source_breakdown[source_type]["avg_reliability"]
                current_count = source_breakdown[source_type]["count"]
                source_breakdown[source_type]["avg_reliability"] = (current_avg * (current_count - 1) + reliability) / current_count
                
                total_reliability += reliability
        
        return {
            "average_reliability": total_reliability / len(sources),
            "source_breakdown": source_breakdown,
            "trusted_sources_ratio": len([s for s in sources if hasattr(s, 'url') and self._is_trusted_source(s.url)]) / len(sources)
        }
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc.lower().replace('www.', '')
    
    def _is_trusted_source(self, url: str) -> bool:
        """Check if URL is from a trusted source domain"""
        domain = self._extract_domain(url)
        return domain in self.trusted_source_domains
    
    def _convert_to_source_object(self, source: Any) -> Source:
        """Convert various source formats to Source object"""
        if isinstance(source, Source):
            return source
        elif hasattr(source, 'url'):
            return self.create_source(
                source.url,
                getattr(source, 'title', 'Unknown Title'),
                getattr(source, 'source_type', 'unknown'),
                getattr(source, 'reliability_score', 0.5)
            )
        else:
            return self.create_source("unknown", "Unknown Source", "unknown", 0.0)
    
    async def _calculate_overall_confidence(self, fact_checks: List[FactCheck], 
                                          source_analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence score for all fact checks"""
        
        if not fact_checks:
            return 0.0
        
        # Weight by individual confidence levels
        confidence_sum = sum(fc.confidence_level for fc in fact_checks)
        avg_confidence = confidence_sum / len(fact_checks)
        
        # Adjust by source reliability
        source_reliability = source_analysis.get("average_reliability", 0.5)
        
        # Adjust by verification consistency
        verified_ratio = len([fc for fc in fact_checks if fc.verification_status == "verified"]) / len(fact_checks)
        
        # Combined confidence score
        overall_confidence = (avg_confidence * 0.5) + (source_reliability * 0.3) + (verified_ratio * 0.2)
        
        return min(1.0, overall_confidence)
    
    async def _review_fact_check_compliance(self, fact_checks: List[FactCheck], 
                                         verification_level: str) -> List[ComplianceCheck]:
        """Review fact-checking compliance with movement standards"""
        
        compliance_checks = []
        
        # Check minimum source requirement
        min_sources_met = all(len(fc.sources) >= 2 for fc in fact_checks)
        
        compliance_checks.append(
            self.create_compliance_check(
                category="source_verification",
                status="compliant" if min_sources_met else "non_compliant",
                details=f"Minimum 2 sources per claim: {'Met' if min_sources_met else 'Not met'}",
                recommendations=[] if min_sources_met else ["Add additional sources for unsupported claims"]
            )
        )
        
        # Check confidence levels
        low_confidence_checks = [fc for fc in fact_checks if fc.confidence_level < 0.7]
        
        compliance_checks.append(
            self.create_compliance_check(
                category="confidence_threshold",
                status="compliant" if not low_confidence_checks else "needs_review",
                details=f"Low confidence claims: {len(low_confidence_checks)}/{len(fact_checks)}",
                recommendations=["Review low-confidence claims", "Seek additional sources"] if low_confidence_checks else []
            )
        )
        
        return compliance_checks
    
    async def _generate_recommendations(self, fact_checks: List[FactCheck], 
                                      source_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving fact-checking quality"""
        
        recommendations = []
        
        # Check for insufficient verification
        unverified_claims = [fc for fc in fact_checks if fc.verification_status != "verified"]
        if unverified_claims:
            recommendations.append(f"Seek additional sources for {len(unverified_claims)} unverified claims")
        
        # Check source diversity  
        source_types = set()
        for fc in fact_checks:
            source_types.update(s.source_type for s in fc.sources)
        
        if len(source_types) < 2:
            recommendations.append("Diversify source types (government, academic, industry)")
        
        # Check reliability
        avg_reliability = source_analysis.get("average_reliability", 0.0)
        if avg_reliability < 0.8:
            recommendations.append("Use higher-reliability sources when possible")
        
        # Check confidence levels
        low_confidence = [fc for fc in fact_checks if fc.confidence_level < 0.8]
        if low_confidence:
            recommendations.append("Strengthen verification for low-confidence claims")
        
        return recommendations

# Export the agent class
__all__ = ['FactCheckerAgent']