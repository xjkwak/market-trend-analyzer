"""
X.com (Twitter) Mock Scraper Agent for simulating social media data collection.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict


def search_x_com(domain: str) -> dict:
    """
    Mock function to simulate searching X.com (Twitter) for posts about a specific domain.
    
    Args:
        domain (str): The domain keyword to search for
        
    Returns:
        dict: Status and mocked posts data or error message
    """
    if not domain or domain.strip() == "":
        return {
            "status": "error",
            "error_message": "Domain keyword required."
        }
    
    # Generate mock posts based on the domain
    mock_posts = [
        {"source": "X.com", "content": f"Latest trending post about {domain} #1"},
        {"source": "X.com", "content": f"Latest trending post about {domain} #2"},
        {"source": "X.com", "content": f"Breaking news in {domain} industry today! #innovation"},
        {"source": "X.com", "content": f"New developments in {domain} are changing the game"},
        {"source": "X.com", "content": f"Just discovered an amazing {domain} startup 🚀"},
        {"source": "X.com", "content": f"Thread: Why {domain} is the future of technology (1/5)"},
        {"source": "X.com", "content": f"Market analysis shows {domain} growing 200% this year"},
        {"source": "X.com", "content": f"Investors are bullish on {domain} companies #investing"},
        {"source": "X.com", "content": f"Conference highlights: The state of {domain} in 2025"},
        {"source": "X.com", "content": f"Hot take: {domain} will dominate the next decade #prediction"}
    ]
    
    return {
        "status": "success",
        "posts": mock_posts
    }


# Define the X.com search agent
x_com_search_agent = LlmAgent(
    name="x_com_search_agent",
    model=LiteLlm(model="openai/gpt-4o"),
    description="Agent to mock searching X.com (Twitter) for posts about a specific domain.",
    instruction=(
        "When requested, return a mock list of posts as if fetched from X.com about the domain keyword. "
        "The posts should be realistic and relevant to the requested domain. "
        "Always use the search_x_com function to generate mock social media content."
    ),
    tools=[search_x_com],
)


if __name__ == "__main__":
    result = search_x_com("Fintech")
    print(result)