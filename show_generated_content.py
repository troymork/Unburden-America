#!/usr/bin/env python3
"""
Direct demonstration of content generation bypassing quality gates
"""

import sys
import os
import asyncio

# Add project root to path
sys.path.insert(0, '/home/user/webapp')

from agents.implementations.content_producer_agent import ContentProducerAgent

async def show_raw_content():
    """Show content generated directly from agent"""
    
    print("📄 DEMONSTRATING ACTUAL CONTENT GENERATION")
    print("=" * 60)
    
    # Create agent instance directly
    agent = ContentProducerAgent("demo-agent-001")
    
    # Create input for content generation
    inputs = {
        "intent": "Create educational content about economic reform",
        "payload": {
            "topic": "Understanding the Monetary Flow Tax",
            "audience": "working families",
            "tone": "educational"
        }
    }
    
    print("🎯 Topic: Understanding the Monetary Flow Tax")
    print("👥 Audience: Working families")
    print("📝 Format: Educational article")
    print("\n" + "=" * 60)
    
    try:
        # Call the content generation directly
        print("🔄 Generating content...")
        
        # This will call the agent's process method
        result = await agent.process(inputs)
        
        print(f"✅ Generation Status: {result.status}")
        print(f"🏷️  Agent Type: {result.agent_type}")
        print(f"🆔 Agent ID: {result.agent_id}")
        
        if result.primary_output:
            print(f"\n📄 GENERATED ARTICLE:")
            print("=" * 60)
            
            if isinstance(result.primary_output, dict):
                # If it's structured output, show nicely formatted
                for key, value in result.primary_output.items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"{key.upper()}:")
                        print(value)
                        print("\n" + "-" * 40 + "\n")
                    else:
                        print(f"{key}: {value}")
            else:
                # If it's a string, show directly
                print(result.primary_output)
            
            print("=" * 60)
        else:
            print("❌ No primary output generated")
        
        if result.metadata:
            print(f"\n📊 METADATA:")
            for key, value in result.metadata.items():
                print(f"  {key}: {value}")
        
        print(f"\n📈 QUALITY SCORES: {result.quality_scores}")
        print(f"🔍 FACT CHECKS: {len(result.fact_checks)}")
        print(f"✅ COMPLIANCE CHECKS: {len(result.compliance_checks)}")
        print(f"📚 SOURCES: {len(result.sources_used)}")
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(show_raw_content())