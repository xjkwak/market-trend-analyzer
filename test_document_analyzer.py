#!/usr/bin/env python3
"""
Test script for DocumentAnalyzerAgent functionality.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from multi_tool_agent.agent import analyze_local_pdfs, document_analysis_agent
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("Please install dependencies with: pip install -r requirements.txt")
    DEPENDENCIES_AVAILABLE = False

def test_analyze_local_pdfs():
    """Test the analyze_local_pdfs function directly."""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot test - dependencies not installed")
        return None
    
    print("Testing analyze_local_pdfs function...")
    result = analyze_local_pdfs()
    print(f"Result: {result}")
    return result

def test_document_analyzer_agent():
    """Test the document analysis agent."""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot test agent - dependencies not installed")
        return None
        
    print("\nTesting document_analysis_agent...")
    try:
        response = document_analysis_agent.run("Please analyze all PDF documents in the docs folder.")
        print(f"Agent response: {response}")
        return response
    except Exception as e:
        print(f"Error testing agent: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testing DocumentAnalyzerAgent implementation...")
    
    if DEPENDENCIES_AVAILABLE:
        # Test the function directly
        function_result = test_analyze_local_pdfs()
        
        # Test the agent
        agent_result = test_document_analyzer_agent()
        
        print("\n✅ Testing completed!")
    else:
        print("\n📋 Implementation is ready but requires dependencies.")
        print("Run 'pip install -r requirements.txt' to install PyMuPDF and test the functionality.")