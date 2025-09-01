#!/usr/bin/env python3
"""
Simple test script for the Research Agent
"""

import sys
import os

def test_import():
    """Test if we can import the agent."""
    try:
        from research_agent import ResearchAgent
        print("✅ Import successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_agent_creation():
    """Test if we can create an agent instance."""
    try:
        from research_agent import ResearchAgent
        agent = ResearchAgent()
        print("✅ Agent creation successful")
        return agent
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return None

def test_simple_research(agent):
    """Test a simple research query."""
    try:
        print("🔍 Testing simple research...")
        results = agent.research_topic("test query")
        print("✅ Research test successful")
        print(f"Results: {results}")
        return True
    except Exception as e:
        print(f"❌ Research test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Research Agent...")
    print("=" * 30)
    
    # Test 1: Import
    if not test_import():
        return
    
    # Test 2: Agent creation
    agent = test_agent_creation()
    if not agent:
        return
    
    # Test 3: Simple research
    test_simple_research(agent)
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
