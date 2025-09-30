#!/usr/bin/env python3
"""
Test script to demonstrate actual content generation from agents
"""

import sys
import os
import asyncio

# Add project root to path
sys.path.insert(0, '/home/user/webapp')

from agents.implementations.agent_factory import agent_factory, AgentType

async def test_content_generation():
    """Test direct content generation"""
    
    print("🚀 Testing AI Agent Content Generation")
    print("=" * 50)
    
    try:
        # Test Content Producer Agent
        print("\n📝 Testing Content Producer Agent...")
        
        inputs = {
            "intent": "Create educational content about economic reform",
            "payload": {
                "topic": "Understanding the Monetary Flow Tax",
                "audience": "working families",
                "tone": "educational"
            }
        }
        
        result = await agent_factory.execute_agent_task(AgentType.CONTENT_PRODUCER, inputs)
        
        print(f"\n✅ Agent Status: {result.status}")
        print(f"📊 Quality Scores: {result.quality_scores}")
        print(f"🔍 Fact Checks: {len(result.fact_checks)}")
        print(f"✅ Compliance Checks: {len(result.compliance_checks)}")
        print(f"📚 Sources Used: {len(result.sources_used)}")
        
        print(f"\n📄 GENERATED CONTENT:")
        print("=" * 80)
        if isinstance(result.primary_output, dict):
            for key, value in result.primary_output.items():
                print(f"{key}: {value}")
        else:
            print(result.primary_output)
        print("=" * 80)
        
        # Test Fact Checker
        print(f"\n🔍 Testing Fact Checker Agent...")
        
        fact_inputs = {
            "content_to_verify": result.primary_output,
            "verification_level": "standard"
        }
        
        fact_result = await agent_factory.execute_agent_task(AgentType.FACT_CHECKER, fact_inputs)
        
        print(f"\n✅ Fact Check Status: {fact_result.status}")
        print(f"📊 Quality Scores: {fact_result.quality_scores}")
        
        print(f"\n📋 FACT CHECK RESULTS:")
        print("-" * 40)
        for i, check in enumerate(fact_result.fact_checks, 1):
            print(f"{i}. {check.claim}")
            print(f"   Status: {check.status}")
            print(f"   Sources: {len(check.sources)}")
        
        print(f"\n🎉 SUCCESS! Agents are generating real content!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_content_generation())