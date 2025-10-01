#!/usr/bin/env python3
"""
Compliance Reviewer Agent for IsThereEnoughMoney Movement
========================================================

This agent specializes in legal, platform, accessibility, and ethical compliance
review to ensure all movement content meets regulatory and platform standards.
"""

import asyncio
import logging
import re
from typing import Dict, List, Any, Optional, Set
import datetime
import json

from agents.implementations.base_agent import (
    BaseAgent, AgentOutput, AgentStatus, Source, FactCheck, 
    ComplianceCheck, MovementKnowledgeBase
)

logger = logging.getLogger(__name__)

class ComplianceReviewerAgent(BaseAgent):
    """Agent specialized in compliance review and legal validation"""
    
    def __init__(self, agent_id: str = None):
        super().__init__(agent_id)
        self.capabilities = [
            "legal_review", "platform_policy_check", "accessibility_audit",
            "privacy_compliance", "ethical_standards_review", "regulatory_compliance"
        ]
        self.quality_gates = [
            "legal_compliance", "platform_compliance", "accessibility_standards",
            "privacy_protection", "ethical_guidelines"
        ]
        self.compliance_frameworks = self._load_compliance_frameworks()
        self.platform_policies = self._load_platform_policies()
        self.legal_guidelines = self._load_legal_guidelines()
    
    def get_agent_type(self) -> str:
        return "compliance_reviewer"
    
    def get_capabilities(self) -> List[str]:
        return self.capabilities
    
    def get_quality_gates(self) -> List[str]:
        return self.quality_gates
    
    def _load_compliance_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """Load compliance frameworks and standards"""
        return {
            "accessibility": {
                "standards": ["WCAG_2.1_AA", "Section_508", "ADA_compliance"],
                "requirements": {
                    "alt_text": "Images must have descriptive alt text",
                    "heading_hierarchy": "Proper H1-H6 structure required",
                    "color_contrast": "Minimum 4.5:1 contrast ratio",
                    "keyboard_navigation": "All interactive elements accessible via keyboard"
                },
                "severity_levels": ["critical", "major", "minor", "advisory"]
            },
            "privacy": {
                "standards": ["GDPR", "CCPA", "COPPA", "PIPEDA"],
                "requirements": {
                    "data_collection": "Clear notice of what data is collected",
                    "consent": "Explicit consent for data processing",
                    "data_retention": "Clear retention and deletion policies",
                    "third_party_sharing": "Notice of any data sharing"
                }
            },
            "political": {
                "standards": ["FEC_compliance", "lobbying_disclosure", "campaign_finance"],
                "requirements": {
                    "political_advertising": "Proper disclaimers required",
                    "contribution_limits": "Comply with donation limits",
                    "disclosure_requirements": "Transparent funding sources",
                    "coordination_rules": "Avoid prohibited coordination"
                }
            },
            "content_ethics": {
                "standards": ["truthfulness", "non_discrimination", "harm_prevention"],
                "requirements": {
                    "factual_accuracy": "All claims must be verifiable",
                    "bias_avoidance": "Avoid targeting based on protected characteristics",
                    "inclusive_language": "Use respectful, inclusive terminology",
                    "harm_mitigation": "Avoid content that could cause harm"
                }
            }
        }
    
    def _load_platform_policies(self) -> Dict[str, Dict[str, Any]]:
        """Load platform-specific policies and requirements"""
        return {
            "facebook": {
                "political_content": {
                    "disclaimer_required": True,
                    "paid_content_disclosure": "Required for all paid political content",
                    "targeting_restrictions": "Limited targeting for political ads",
                    "prohibited_content": ["voter suppression", "false election info"]
                },
                "community_standards": {
                    "hate_speech": "Prohibited",
                    "harassment": "Prohibited", 
                    "spam": "Prohibited",
                    "misleading_content": "Fact-checked and labeled"
                }
            },
            "twitter": {
                "civic_integrity": {
                    "election_content": "Must not mislead about voting processes",
                    "disputed_claims": "May be labeled or restricted",
                    "premature_declarations": "Victory claims before official results prohibited"
                },
                "hateful_conduct": {
                    "targeted_harassment": "Prohibited",
                    "hate_speech": "Prohibited based on protected categories"
                }
            },
            "youtube": {
                "monetization": {
                    "advertiser_friendly": "Content must be suitable for most advertisers",
                    "controversial_topics": "Political content may have limited monetization"
                },
                "community_guidelines": {
                    "spam_deception": "Prohibited",
                    "harmful_content": "Content that could cause real-world harm"
                }
            },
            "instagram": {
                "content_policy": {
                    "political_content": "Same as Facebook policies",
                    "community_guidelines": "Aligned with Facebook standards"
                }
            },
            "linkedin": {
                "professional_standards": {
                    "political_content": "Allowed but must be professional",
                    "misleading_content": "Fact-checked",
                    "spam": "Prohibited"
                }
            }
        }
    
    def _load_legal_guidelines(self) -> Dict[str, Dict[str, Any]]:
        """Load legal guidelines and regulatory requirements"""
        return {
            "campaign_finance": {
                "fec_requirements": {
                    "contribution_limits": "Individual: $2,900 per candidate per election",
                    "disclosure_thresholds": "$200+ contributions must be disclosed",
                    "prohibited_sources": "No foreign nationals, corporations (direct)",
                    "coordination_limits": "Limited coordination with campaigns"
                }
            },
            "lobbying": {
                "lda_requirements": {
                    "registration_threshold": "$3,000+ in lobbying activities per quarter",
                    "disclosure_requirements": "Quarterly disclosure reports required",
                    "contact_logging": "Must log contacts with covered officials"
                }
            },
            "tax_exempt": {
                "501c3_rules": {
                    "political_activity": "No campaign intervention allowed",
                    "lobbying_limits": "Insubstantial lobbying only",
                    "educational_focus": "Must be primarily educational"
                },
                "501c4_rules": {
                    "primary_purpose": "Social welfare must be primary purpose",
                    "political_activity": "Some political activity allowed",
                    "donor_disclosure": "Limited disclosure requirements"
                }
            },
            "advertising": {
                "ftc_requirements": {
                    "truthfulness": "No deceptive or unfair practices",
                    "substantiation": "Must have evidence for claims",
                    "endorsements": "Clear disclosure of material connections",
                    "native_advertising": "Must be clearly identified as advertising"
                }
            }
        }
    
    async def process(self, inputs: Dict[str, Any]) -> AgentOutput:
        """Process compliance review for content, campaigns, or activities"""
        
        # Extract inputs
        content_to_review = inputs.get("content", "")
        content_type = inputs.get("content_type", "general")
        target_platforms = inputs.get("platforms", ["web"])
        review_scope = inputs.get("scope", ["legal", "platform", "accessibility", "ethics"])
        organization_type = inputs.get("organization_type", "advocacy_group")
        
        logger.info(f"Conducting {', '.join(review_scope)} compliance review for {content_type}")
        
        # Simulate processing time
        await self.simulate_processing_delay(2.0, 5.0)
        
        # Perform compliance checks by category
        compliance_results = {}
        all_compliance_checks = []
        
        if "legal" in review_scope:
            legal_results = await self._review_legal_compliance(content_to_review, content_type, organization_type)
            compliance_results["legal"] = legal_results
            all_compliance_checks.extend(legal_results["checks"])
        
        if "platform" in review_scope:
            platform_results = await self._review_platform_compliance(content_to_review, target_platforms)
            compliance_results["platform"] = platform_results  
            all_compliance_checks.extend(platform_results["checks"])
        
        if "accessibility" in review_scope:
            accessibility_results = await self._review_accessibility_compliance(content_to_review, content_type)
            compliance_results["accessibility"] = accessibility_results
            all_compliance_checks.extend(accessibility_results["checks"])
        
        if "ethics" in review_scope:
            ethics_results = await self._review_ethical_compliance(content_to_review, content_type)
            compliance_results["ethics"] = ethics_results
            all_compliance_checks.extend(ethics_results["checks"])
        
        # Generate overall compliance assessment
        overall_assessment = await self._generate_overall_assessment(all_compliance_checks)
        
        # Generate recommendations
        recommendations = await self._generate_compliance_recommendations(all_compliance_checks, compliance_results)
        
        # Calculate risk scores
        risk_assessment = await self._calculate_risk_assessment(all_compliance_checks, content_type)
        
        return AgentOutput(
            agent_id=self.agent_id,
            agent_type=self.get_agent_type(),
            status=AgentStatus.PROCESSING,
            primary_output={
                "compliance_summary": {
                    "overall_status": overall_assessment["status"],
                    "critical_issues": overall_assessment["critical_count"],
                    "total_issues": len(all_compliance_checks),
                    "compliance_score": overall_assessment["compliance_score"],
                    "review_scope": review_scope
                },
                "detailed_results": compliance_results,
                "risk_assessment": risk_assessment,
                "recommendations": recommendations,
                "action_items": await self._generate_action_items(all_compliance_checks)
            },
            metadata={
                "compliance_frameworks_used": list(self.compliance_frameworks.keys()),
                "platforms_reviewed": target_platforms,
                "organization_type": organization_type,
                "review_methodology": "Multi-framework compliance analysis"
            },
            quality_scores={
                "legal_compliance_score": compliance_results.get("legal", {}).get("score", 1.0),
                "platform_compliance_score": compliance_results.get("platform", {}).get("score", 1.0),
                "accessibility_score": compliance_results.get("accessibility", {}).get("score", 1.0),
                "ethics_score": compliance_results.get("ethics", {}).get("score", 1.0),
                "overall_compliance_score": overall_assessment["compliance_score"]
            },
            fact_checks=[],  # Compliance agent doesn't generate fact checks
            compliance_checks=all_compliance_checks,
            sources_used=[
                self.create_source("https://www.fec.gov/", "Federal Election Commission", "government", 0.98),
                self.create_source("https://www.w3.org/WAI/WCAG21/quickref/", "WCAG 2.1 Guidelines", "standards", 0.95),
                self.create_source("https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings", "FTC Advertising Guidelines", "government", 0.96)
            ],
            execution_time_ms=0,
            created_at=datetime.datetime.utcnow().isoformat()
        )
    
    async def _review_legal_compliance(self, content: str, content_type: str, org_type: str) -> Dict[str, Any]:
        """Review legal compliance including campaign finance, lobbying, and advertising law"""
        
        logger.info("Conducting legal compliance review")
        await asyncio.sleep(0.8)
        
        checks = []
        legal_framework = self.legal_guidelines
        
        # Campaign finance compliance
        if self._contains_political_content(content):
            # Check for proper disclaimers
            has_disclaimer = self._check_political_disclaimer(content)
            checks.append(
                self.create_compliance_check(
                    category="campaign_finance",
                    status="compliant" if has_disclaimer else "non_compliant",
                    details=f"Political disclaimer: {'Present' if has_disclaimer else 'Missing'}",
                    recommendations=[] if has_disclaimer else ["Add 'Paid for by...' disclaimer to political content"]
                )
            )
            
            # Check for prohibited content
            prohibited_content = self._check_prohibited_political_content(content)
            if prohibited_content:
                checks.append(
                    self.create_compliance_check(
                        category="campaign_finance",
                        status="non_compliant", 
                        details=f"Prohibited content detected: {', '.join(prohibited_content)}",
                        recommendations=["Remove or modify prohibited political content"]
                    )
                )
        
        # Advertising law compliance (FTC)
        ftc_issues = await self._check_ftc_compliance(content)
        for issue in ftc_issues:
            checks.append(issue)
        
        # Tax-exempt organization compliance
        if org_type in ["501c3", "501c4"]:
            tax_exempt_issues = await self._check_tax_exempt_compliance(content, org_type)
            checks.extend(tax_exempt_issues)
        
        # Calculate legal compliance score
        compliant_checks = [c for c in checks if c.status == "compliant"]
        score = len(compliant_checks) / max(len(checks), 1)
        
        return {
            "checks": checks,
            "score": score,
            "framework_used": "FEC, FTC, IRS guidelines",
            "critical_issues": [c for c in checks if c.status == "non_compliant"]
        }
    
    async def _review_platform_compliance(self, content: str, platforms: List[str]) -> Dict[str, Any]:
        """Review compliance with platform-specific policies"""
        
        logger.info(f"Reviewing platform compliance for: {', '.join(platforms)}")
        await asyncio.sleep(0.6)
        
        checks = []
        
        for platform in platforms:
            if platform in self.platform_policies:
                platform_policy = self.platform_policies[platform]
                platform_checks = await self._check_platform_specific_compliance(content, platform, platform_policy)
                checks.extend(platform_checks)
        
        # Universal platform checks
        universal_checks = await self._check_universal_platform_compliance(content)
        checks.extend(universal_checks)
        
        # Calculate platform compliance score
        compliant_checks = [c for c in checks if c.status == "compliant"]
        score = len(compliant_checks) / max(len(checks), 1)
        
        return {
            "checks": checks,
            "score": score,
            "platforms_reviewed": platforms,
            "policy_violations": [c for c in checks if c.status == "non_compliant"]
        }
    
    async def _review_accessibility_compliance(self, content: str, content_type: str) -> Dict[str, Any]:
        """Review accessibility compliance (WCAG, ADA, Section 508)"""
        
        logger.info("Conducting accessibility compliance review")
        await asyncio.sleep(0.4)
        
        checks = []
        accessibility_framework = self.compliance_frameworks["accessibility"]
        
        # Check heading structure
        heading_check = self._check_heading_structure(content)
        checks.append(heading_check)
        
        # Check for images needing alt text
        image_check = self._check_image_accessibility(content)
        if image_check:
            checks.append(image_check)
        
        # Check color contrast (if HTML content)
        if content_type in ["html", "web_content"]:
            color_check = self._check_color_contrast(content)
            checks.append(color_check)
        
        # Check link accessibility
        link_check = self._check_link_accessibility(content)
        if link_check:
            checks.append(link_check)
        
        # Check language and readability
        readability_check = self._check_content_readability(content)
        checks.append(readability_check)
        
        # Calculate accessibility score
        compliant_checks = [c for c in checks if c.status == "compliant"]
        score = len(compliant_checks) / max(len(checks), 1)
        
        return {
            "checks": checks,
            "score": score,
            "standards_used": accessibility_framework["standards"],
            "accessibility_issues": [c for c in checks if c.status != "compliant"]
        }
    
    async def _review_ethical_compliance(self, content: str, content_type: str) -> Dict[str, Any]:
        """Review ethical compliance and content standards"""
        
        logger.info("Conducting ethical compliance review")
        await asyncio.sleep(0.5)
        
        checks = []
        ethics_framework = self.compliance_frameworks["content_ethics"]
        
        # Check for bias and discrimination
        bias_check = await self._check_bias_and_discrimination(content)
        checks.append(bias_check)
        
        # Check for inclusive language
        inclusive_check = self._check_inclusive_language(content)
        checks.append(inclusive_check)
        
        # Check for harmful content
        harm_check = self._check_harmful_content(content)
        checks.append(harm_check)
        
        # Check truthfulness alignment
        truth_check = self._check_truthfulness_standards(content)
        checks.append(truth_check)
        
        # Movement-specific ethical standards
        movement_ethics_check = await self._check_movement_ethics(content)
        checks.append(movement_ethics_check)
        
        # Calculate ethics score
        compliant_checks = [c for c in checks if c.status == "compliant"]
        score = len(compliant_checks) / max(len(checks), 1)
        
        return {
            "checks": checks,
            "score": score,
            "ethical_frameworks": ethics_framework["standards"],
            "ethical_concerns": [c for c in checks if c.status != "compliant"]
        }
    
    def _contains_political_content(self, content: str) -> bool:
        """Check if content contains political elements"""
        political_keywords = [
            "vote", "election", "candidate", "politician", "congress", "senate",
            "democrat", "republican", "campaign", "political", "policy", "legislation"
        ]
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in political_keywords)
    
    def _check_political_disclaimer(self, content: str) -> bool:
        """Check for required political disclaimers"""
        disclaimer_patterns = [
            r"paid for by",
            r"authorized by", 
            r"sponsored by",
            r"funded by"
        ]
        content_lower = content.lower()
        return any(re.search(pattern, content_lower) for pattern in disclaimer_patterns)
    
    def _check_prohibited_political_content(self, content: str) -> List[str]:
        """Check for prohibited political content"""
        prohibited_items = []
        content_lower = content.lower()
        
        # Check for voter suppression language
        suppression_terms = ["don't vote", "avoid voting", "skip election"]
        if any(term in content_lower for term in suppression_terms):
            prohibited_items.append("potential_voter_suppression")
        
        # Check for election misinformation
        misinfo_terms = ["wrong date", "fake poll", "rigged election"]
        if any(term in content_lower for term in misinfo_terms):
            prohibited_items.append("election_misinformation")
        
        return prohibited_items
    
    async def _check_ftc_compliance(self, content: str) -> List[ComplianceCheck]:
        """Check FTC advertising compliance"""
        checks = []
        
        # Check for unsubstantiated claims
        if self._contains_unverified_claims(content):
            checks.append(
                self.create_compliance_check(
                    category="advertising_law",
                    status="needs_review",
                    details="Content contains claims that may need substantiation",
                    recommendations=["Ensure all claims have supporting evidence", "Add disclaimers for projections"]
                )
            )
        
        # Check for clear advertising disclosure
        if self._appears_to_be_advertisement(content) and not self._has_ad_disclosure(content):
            checks.append(
                self.create_compliance_check(
                    category="advertising_law", 
                    status="non_compliant",
                    details="Advertisement lacks proper disclosure",
                    recommendations=["Add clear 'Advertisement' or 'Sponsored' disclosure"]
                )
            )
        
        return checks
    
    async def _check_tax_exempt_compliance(self, content: str, org_type: str) -> List[ComplianceCheck]:
        """Check tax-exempt organization compliance"""
        checks = []
        
        if org_type == "501c3":
            # 501(c)(3) cannot engage in campaign intervention
            if self._contains_campaign_intervention(content):
                checks.append(
                    self.create_compliance_check(
                        category="tax_exempt_compliance",
                        status="non_compliant",
                        details="501(c)(3) content appears to intervene in political campaign",
                        recommendations=["Remove campaign intervention language", "Focus on educational content"]
                    )
                )
        
        return checks
    
    async def _check_platform_specific_compliance(self, content: str, platform: str, policy: Dict) -> List[ComplianceCheck]:
        """Check compliance with specific platform policies"""
        checks = []
        
        # Facebook/Meta specific checks
        if platform == "facebook":
            if "political_content" in policy and self._contains_political_content(content):
                if not self._has_political_disclaimer(content):
                    checks.append(
                        self.create_compliance_check(
                            category="platform_policy",
                            status="non_compliant",
                            details="Facebook political content requires disclaimer",
                            recommendations=["Add Facebook-compliant political disclaimer"]
                        )
                    )
        
        # Twitter specific checks
        elif platform == "twitter":
            if len(content) > 280:
                checks.append(
                    self.create_compliance_check(
                        category="platform_policy",
                        status="non_compliant", 
                        details=f"Content exceeds Twitter character limit ({len(content)}/280)",
                        recommendations=["Shorten content to fit Twitter limit"]
                    )
                )
        
        return checks
    
    async def _check_universal_platform_compliance(self, content: str) -> List[ComplianceCheck]:
        """Check universal platform compliance issues"""
        checks = []
        
        # Check for spam-like content
        if self._appears_spammy(content):
            checks.append(
                self.create_compliance_check(
                    category="platform_policy",
                    status="non_compliant",
                    details="Content may be flagged as spam",
                    recommendations=["Reduce repetitive language", "Add meaningful content"]
                )
            )
        
        # Check for hate speech indicators
        if self._contains_hate_speech_indicators(content):
            checks.append(
                self.create_compliance_check(
                    category="platform_policy",
                    status="non_compliant",
                    details="Content may violate hate speech policies",
                    recommendations=["Review and remove potentially offensive language"]
                )
            )
        
        return checks
    
    def _check_heading_structure(self, content: str) -> ComplianceCheck:
        """Check proper heading hierarchy"""
        
        # Simple check for markdown headings
        headings = re.findall(r'^#+\s', content, re.MULTILINE)
        
        if not headings:
            return self.create_compliance_check(
                category="accessibility",
                status="needs_review",
                details="No headings found - consider adding structure",
                recommendations=["Add proper heading hierarchy (H1, H2, etc.)"]
            )
        
        return self.create_compliance_check(
            category="accessibility",
            status="compliant",
            details=f"Document has {len(headings)} headings",
            recommendations=[]
        )
    
    def _check_image_accessibility(self, content: str) -> Optional[ComplianceCheck]:
        """Check image accessibility requirements"""
        
        # Look for image references
        image_patterns = [r'!\[.*?\]\(.*?\)', r'<img.*?>', r'image:', r'photo:']
        has_images = any(re.search(pattern, content, re.IGNORECASE) for pattern in image_patterns)
        
        if has_images:
            # Check for alt text
            alt_text_patterns = [r'alt\s*=\s*["\'][^"\']*["\']', r'!\[.+?\]']
            has_alt_text = any(re.search(pattern, content, re.IGNORECASE) for pattern in alt_text_patterns)
            
            return self.create_compliance_check(
                category="accessibility",
                status="compliant" if has_alt_text else "non_compliant",
                details=f"Images found: {'Alt text present' if has_alt_text else 'Missing alt text'}",
                recommendations=[] if has_alt_text else ["Add descriptive alt text for all images"]
            )
        
        return None
    
    def _check_color_contrast(self, content: str) -> ComplianceCheck:
        """Check color contrast requirements"""
        
        # Simplified check - would need actual color analysis in real implementation
        return self.create_compliance_check(
            category="accessibility",
            status="needs_review",
            details="Color contrast requires manual verification",
            recommendations=["Verify 4.5:1 contrast ratio for text", "Test with accessibility tools"]
        )
    
    def _check_link_accessibility(self, content: str) -> Optional[ComplianceCheck]:
        """Check link accessibility"""
        
        links = re.findall(r'\[.*?\]\(.*?\)|https?://\S+', content)
        
        if links:
            # Check for descriptive link text
            descriptive_links = [link for link in links if len(link) > 10 and not re.match(r'https?://', link)]
            
            return self.create_compliance_check(
                category="accessibility",
                status="compliant" if descriptive_links else "needs_review",
                details=f"Links found: {len(links)}, descriptive: {len(descriptive_links)}",
                recommendations=["Use descriptive link text instead of URLs"] if not descriptive_links else []
            )
        
        return None
    
    def _check_content_readability(self, content: str) -> ComplianceCheck:
        """Check content readability"""
        
        # Simple readability metrics
        words = len(content.split())
        sentences = content.count('.') + content.count('!') + content.count('?')
        avg_sentence_length = words / max(sentences, 1)
        
        # Grade level approximation (simplified Flesch)
        grade_level = 0.39 * avg_sentence_length + 11.8  # Simplified calculation
        
        status = "compliant" if grade_level <= 12 else "needs_review"
        
        return self.create_compliance_check(
            category="accessibility",
            status=status,
            details=f"Estimated reading level: Grade {grade_level:.1f}",
            recommendations=["Simplify language for broader accessibility"] if status != "compliant" else []
        )
    
    async def _check_bias_and_discrimination(self, content: str) -> ComplianceCheck:
        """Check for bias and discriminatory language"""
        
        # Check for potentially biased terms
        bias_indicators = [
            "those people", "you people", "illegal aliens", 
            "welfare queens", "urban thugs"
        ]
        
        content_lower = content.lower()
        bias_found = any(term in content_lower for term in bias_indicators)
        
        return self.create_compliance_check(
            category="ethics",
            status="compliant" if not bias_found else "non_compliant",
            details=f"Bias check: {'No issues detected' if not bias_found else 'Potentially biased language found'}",
            recommendations=[] if not bias_found else ["Remove or replace biased language", "Use neutral terminology"]
        )
    
    def _check_inclusive_language(self, content: str) -> ComplianceCheck:
        """Check for inclusive language usage"""
        
        # Check for gender-inclusive language
        inclusive_score = 0
        
        # Positive indicators
        inclusive_terms = ["people", "individuals", "Americans", "families", "workers"]
        content_lower = content.lower()
        
        inclusive_count = sum(1 for term in inclusive_terms if term in content_lower)
        
        # Check for potentially exclusive terms
        exclusive_terms = ["guys", "mankind", "he/she"]
        exclusive_count = sum(1 for term in exclusive_terms if term in content_lower)
        
        status = "compliant" if exclusive_count == 0 else "needs_review"
        
        return self.create_compliance_check(
            category="ethics",
            status=status,
            details=f"Inclusive language: {inclusive_count} positive terms, {exclusive_count} exclusionary terms",
            recommendations=["Replace exclusionary terms with inclusive alternatives"] if exclusive_count > 0 else []
        )
    
    def _check_harmful_content(self, content: str) -> ComplianceCheck:
        """Check for potentially harmful content"""
        
        harmful_indicators = [
            "violence", "threat", "harm", "dangerous", "illegal activity"
        ]
        
        content_lower = content.lower()
        
        # Context-aware check - these terms might be acceptable in policy discussions
        policy_context = any(term in content_lower for term in ["policy", "legislation", "economic", "analysis"])
        
        harmful_count = sum(1 for term in harmful_indicators if term in content_lower)
        
        status = "compliant" if harmful_count == 0 or policy_context else "needs_review"
        
        return self.create_compliance_check(
            category="ethics",
            status=status,
            details=f"Harm assessment: {harmful_count} potential indicators, policy context: {policy_context}",
            recommendations=["Review content for potential harm"] if status != "compliant" else []
        )
    
    def _check_truthfulness_standards(self, content: str) -> ComplianceCheck:
        """Check adherence to truthfulness standards"""
        
        # Check for claim qualifiers
        qualifiers = ["approximately", "about", "estimated", "according to", "based on"]
        content_lower = content.lower()
        
        qualifier_count = sum(1 for qualifier in qualifiers if qualifier in content_lower)
        
        # Check for absolute statements that might need qualification
        absolute_terms = ["always", "never", "all", "none", "definitely", "certainly"]
        absolute_count = sum(1 for term in absolute_terms if term in content_lower)
        
        status = "compliant" if absolute_count <= qualifier_count else "needs_review"
        
        return self.create_compliance_check(
            category="ethics",
            status=status,
            details=f"Truthfulness: {qualifier_count} qualifiers, {absolute_count} absolute statements",
            recommendations=["Add qualifiers to absolute statements", "Ensure claims are verifiable"] if status != "compliant" else []
        )
    
    async def _check_movement_ethics(self, content: str) -> ComplianceCheck:
        """Check alignment with movement ethical standards"""
        
        movement_principles = self.movement_principles
        content_lower = content.lower()
        
        # Check for alignment with core message
        core_message_present = "tax the system" in content_lower and "not the people" in content_lower
        
        # Check for partisan language avoidance
        partisan_terms = ["democrat", "republican", "liberal", "conservative"]
        partisan_count = sum(1 for term in partisan_terms if term in content_lower)
        
        # Check for focus on economic facts
        economic_terms = ["economic", "economy", "financial", "monetary", "fiscal"]
        economic_count = sum(1 for term in economic_terms if term in content_lower)
        
        alignment_score = 0
        if core_message_present:
            alignment_score += 0.4
        if partisan_count == 0:
            alignment_score += 0.3
        if economic_count >= 2:
            alignment_score += 0.3
        
        status = "compliant" if alignment_score >= 0.6 else "needs_review"
        
        return self.create_compliance_check(
            category="movement_ethics",
            status=status,
            details=f"Movement alignment: {alignment_score:.1f} (core message: {core_message_present}, partisan terms: {partisan_count})",
            recommendations=["Strengthen alignment with movement messaging", "Focus on economic facts"] if status != "compliant" else []
        )
    
    # Helper methods for various checks
    def _contains_unverified_claims(self, content: str) -> bool:
        """Check if content contains claims that might need verification"""
        claim_indicators = ["will", "guarantees", "proven to", "definitely", "always results in"]
        return any(indicator in content.lower() for indicator in claim_indicators)
    
    def _appears_to_be_advertisement(self, content: str) -> bool:
        """Check if content appears to be advertising"""
        ad_indicators = ["buy", "purchase", "order now", "special offer", "limited time"]
        return any(indicator in content.lower() for indicator in ad_indicators)
    
    def _has_ad_disclosure(self, content: str) -> bool:
        """Check for advertising disclosure"""
        disclosure_terms = ["advertisement", "sponsored", "paid promotion", "ad"]
        return any(term in content.lower() for term in disclosure_terms)
    
    def _contains_campaign_intervention(self, content: str) -> bool:
        """Check for campaign intervention (prohibited for 501c3)"""
        intervention_terms = ["vote for", "support candidate", "elect", "defeat"]
        return any(term in content.lower() for term in intervention_terms)
    
    def _has_political_disclaimer(self, content: str) -> bool:
        """Check for political disclaimer"""
        return self._check_political_disclaimer(content)
    
    def _appears_spammy(self, content: str) -> bool:
        """Check if content appears spam-like"""
        # Simple spam indicators
        excessive_caps = len(re.findall(r'[A-Z]{3,}', content)) > 3
        excessive_exclamation = content.count('!') > 5
        repetitive_words = len(set(content.lower().split())) < len(content.split()) * 0.5
        
        return excessive_caps or excessive_exclamation or repetitive_words
    
    def _contains_hate_speech_indicators(self, content: str) -> bool:
        """Check for hate speech indicators"""
        # This would be more sophisticated in a real implementation
        hate_indicators = ["hate", "destroy", "eliminate", "inferior"]
        content_lower = content.lower()
        
        # Context matters - these terms might be acceptable in policy discussions
        policy_context = any(term in content_lower for term in ["policy", "economic", "system"])
        
        hate_count = sum(1 for indicator in hate_indicators if indicator in content_lower)
        
        return hate_count > 0 and not policy_context
    
    async def _generate_overall_assessment(self, all_checks: List[ComplianceCheck]) -> Dict[str, Any]:
        """Generate overall compliance assessment"""
        
        if not all_checks:
            return {"status": "compliant", "compliance_score": 1.0, "critical_count": 0}
        
        compliant_count = len([c for c in all_checks if c.status == "compliant"])
        non_compliant_count = len([c for c in all_checks if c.status == "non_compliant"])
        needs_review_count = len([c for c in all_checks if c.status == "needs_review"])
        
        compliance_score = (compliant_count + (needs_review_count * 0.5)) / len(all_checks)
        
        if non_compliant_count > 0:
            status = "non_compliant"
        elif needs_review_count > compliant_count:
            status = "needs_review"
        else:
            status = "compliant"
        
        return {
            "status": status,
            "compliance_score": compliance_score,
            "critical_count": non_compliant_count,
            "review_count": needs_review_count,
            "compliant_count": compliant_count
        }
    
    async def _generate_compliance_recommendations(self, checks: List[ComplianceCheck], 
                                                 results: Dict[str, Any]) -> List[str]:
        """Generate prioritized compliance recommendations"""
        
        recommendations = []
        
        # Critical issues first
        critical_checks = [c for c in checks if c.status == "non_compliant"]
        for check in critical_checks:
            recommendations.extend(check.recommendations)
        
        # Review items
        review_checks = [c for c in checks if c.status == "needs_review"]
        for check in review_checks:
            recommendations.extend(check.recommendations)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return unique_recommendations[:10]  # Top 10 recommendations
    
    async def _calculate_risk_assessment(self, checks: List[ComplianceCheck], content_type: str) -> Dict[str, Any]:
        """Calculate risk assessment for compliance issues"""
        
        risk_scores = {
            "legal": 0.0,
            "platform": 0.0,
            "accessibility": 0.0,
            "reputation": 0.0
        }
        
        for check in checks:
            if check.status == "non_compliant":
                if check.category in ["campaign_finance", "advertising_law", "tax_exempt_compliance"]:
                    risk_scores["legal"] += 0.3
                elif check.category == "platform_policy":
                    risk_scores["platform"] += 0.2
                elif check.category == "accessibility":
                    risk_scores["accessibility"] += 0.15
                elif check.category in ["ethics", "movement_ethics"]:
                    risk_scores["reputation"] += 0.1
        
        # Cap scores at 1.0
        for key in risk_scores:
            risk_scores[key] = min(1.0, risk_scores[key])
        
        overall_risk = max(risk_scores.values())
        
        return {
            "overall_risk_level": "high" if overall_risk > 0.7 else "medium" if overall_risk > 0.3 else "low",
            "risk_breakdown": risk_scores,
            "overall_risk_score": overall_risk
        }
    
    async def _generate_action_items(self, checks: List[ComplianceCheck]) -> List[Dict[str, Any]]:
        """Generate prioritized action items"""
        
        action_items = []
        
        # Critical items
        critical_checks = [c for c in checks if c.status == "non_compliant"]
        for check in critical_checks:
            for rec in check.recommendations:
                action_items.append({
                    "priority": "high",
                    "category": check.category,
                    "action": rec,
                    "deadline": "immediate"
                })
        
        # Review items
        review_checks = [c for c in checks if c.status == "needs_review"]
        for check in review_checks:
            for rec in check.recommendations:
                action_items.append({
                    "priority": "medium",
                    "category": check.category,
                    "action": rec,
                    "deadline": "before_publication"
                })
        
        return action_items[:15]  # Top 15 action items

# Export the agent class
__all__ = ['ComplianceReviewerAgent']