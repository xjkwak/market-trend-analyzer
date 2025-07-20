"""
Research Scraper Mock Agent for simulating research database queries.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict


def search_research(domain: str) -> dict:
    """
    Mock function to simulate searching research databases like arXiv and SSRN for papers about a specific domain.
    
    Args:
        domain (str): The domain keyword to search for
        
    Returns:
        dict: Status and mocked research papers data or error message
    """
    if not domain or domain.strip() == "":
        return {
            "status": "error",
            "error_message": "Domain keyword required."
        }
    
    # Generate mock research papers based on the domain
    mock_papers = [
        {"source": "arXiv", "title": f"Sample research paper about {domain} #1"},
        {"source": "SSRN", "title": f"Sample research paper about {domain} #2"},
        {"source": "arXiv", "title": f"Deep Learning Applications in {domain}: A Comprehensive Review"},
        {"source": "SSRN", "title": f"Market Dynamics and Innovation Patterns in the {domain} Industry"},
        {"source": "arXiv", "title": f"Machine Learning Methods for {domain} Optimization and Analysis"},
        {"source": "SSRN", "title": f"Economic Impact of {domain} Technologies on Global Markets"},
        {"source": "arXiv", "title": f"Algorithmic Approaches to {domain} Problem Solving"},
        {"source": "SSRN", "title": f"Investment Trends and Risk Assessment in {domain} Sector"},
        {"source": "arXiv", "title": f"Statistical Models for {domain} Data Processing and Prediction"},
        {"source": "SSRN", "title": f"Regulatory Framework and Policy Implications for {domain} Development"}
    ]
    
    return {
        "status": "success",
        "papers": mock_papers
    }


# Define the Research Scraper agent
research_scraper_agent = LlmAgent(
    name="research_scraper_agent",
    model=LiteLlm(model="openai/gpt-4o"),
    description="Agent to mock searching arXiv and SSRN for research papers about a specific domain.",
    instruction=(
        "When requested, return a mock list of research papers related to the specified domain. "
        "The papers should be realistic academic titles from reputable sources like arXiv and SSRN. "
        "Always use the search_research function to generate mock research content."
    ),
    tools=[search_research],
)


if __name__ == "__main__":
    result = search_research("AI/Tech")
    print(result)