#!/usr/bin/env python3
"""
Setup script for OpenAI model integration with ADK agent.
"""

import os
import sys

def setup_openai_key():
    """Set up OpenAI API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your-api-key-here":
        print("⚠️  OpenAI API key not found!")
        print("\nTo set up your OpenAI API key:")
        print("1. Get your API key from https://platform.openai.com/api-keys")
        print("2. Set the environment variable:")
        print("   export OPENAI_API_KEY='your-actual-api-key'")
        print("\nOr add it to your .env file:")
        print("   OPENAI_API_KEY=your-actual-api-key")
        return False
    
    print("✅ OpenAI API key found!")
    return True

def test_agent():
    """Test the agent with a simple query."""
    try:
        from app.multi_tool_agent.agent import root_agent
        
        print("\n🧪 Testing agent with OpenAI model...")
        
        # Test the agent
        response = root_agent.run("What's the weather in New York?")
        print(f"Agent response: {response}")
        
        print("✅ Agent test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing agent: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up OpenAI model for ADK agent...")
    
    if setup_openai_key():
        test_agent()
    else:
        print("\nPlease set up your OpenAI API key and try again.")
        sys.exit(1) 