#!/usr/bin/env python3
"""
Test script for the Market Trend Coordinator Agent functionality.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from multi_tool_agent.agent import (
        root_agent, 
        search_news_articles, 
        search_x_com_posts, 
        get_comprehensive_analysis
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("Please install dependencies with: pip install -r requirements.txt")
    DEPENDENCIES_AVAILABLE = False

def test_news_search():
    """Test the news search functionality."""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot test - dependencies not installed")
        return None
    
    print("Testing news search functionality...")
    result = search_news_articles("Fintech")
    print(f"News search result: {result}")
    return result

def test_x_com_search():
    """Test the X.com search functionality."""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot test - dependencies not installed")
        return None
    
    print("Testing X.com search functionality...")
    result = search_x_com_posts("Healthcare")
    print(f"X.com search result: {result}")
    return result

def test_comprehensive_analysis():
    """Test the comprehensive analysis functionality."""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot test - dependencies not installed")
        return None
    
    print("Testing comprehensive analysis functionality...")
    result = get_comprehensive_analysis("AI")
    print(f"Comprehensive analysis result: {result}")
    return result

def test_coordinator_agent():
    """Test the coordinator agent tools directly."""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot test agent - dependencies not installed")
        return None
        
    print("\nTesting coordinator agent tools...")
    try:
        # Test that the agent has the expected tools
        tools = root_agent.tools if hasattr(root_agent, 'tools') else []
        print(f"Agent has {len(tools)} tools: {[tool.__name__ for tool in tools]}")
        
        # Test that the agent has the expected name and description
        print(f"Agent name: {root_agent.name}")
        print(f"Agent description: {root_agent.description}")
        
        return True
    except Exception as e:
        print(f"Error testing coordinator agent: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testing Market Trend Coordinator Agent implementation...")
    
    if DEPENDENCIES_AVAILABLE:
        # Test individual functions
        news_result = test_news_search()
        x_com_result = test_x_com_search()
        comprehensive_result = test_comprehensive_analysis()
        
        # Test the coordinator agent
        agent_result = test_coordinator_agent()
        
        print("\n✅ Testing completed!")
        print("\nSummary:")
        print(f"- News search: {'✅' if news_result and news_result.get('status') == 'success' else '❌'}")
        print(f"- X.com search: {'✅' if x_com_result and x_com_result.get('status') == 'success' else '❌'}")
        print(f"- Comprehensive analysis: {'✅' if comprehensive_result and comprehensive_result.get('status') == 'success' else '❌'}")
        print(f"- Coordinator agent tools: {'✅' if agent_result else '❌'}")
    else:
        print("\n📋 Implementation is ready but requires dependencies.")
        print("Run 'pip install -r requirements.txt' to install dependencies and test the functionality.") 