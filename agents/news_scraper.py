"""
NewsAPI Mock Scraper Agent for simulating news data collection.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict


def search_news(domain: str) -> dict:
    """
    Mock function to simulate searching NewsAPI.org for articles about a specific domain.
    
    Args:
        domain (str): The domain keyword to search for
        
    Returns:
        dict: Status and mocked articles data or error message
    """
    if not domain or domain.strip() == "":
        return {
            "status": "error",
            "error_message": "Domain keyword required."
        }
    
    # Generate mock news articles based on the domain
    mock_articles = [
        {"source": "NewsAPI", "content": f"Sample headline about {domain} #1"},
        {"source": "NewsAPI", "content": f"Sample headline about {domain} #2"},
        {"source": "NewsAPI", "content": f"Breaking: Major {domain} company announces breakthrough innovation"},
        {"source": "NewsAPI", "content": f"Industry experts predict significant growth in {domain} sector"},
        {"source": "NewsAPI", "content": f"New regulations could impact {domain} market dynamics"},
        {"source": "NewsAPI", "content": f"Global {domain} market reaches record high this quarter"},
        {"source": "NewsAPI", "content": f"Startup disrupts traditional {domain} industry with AI technology"},
        {"source": "NewsAPI", "content": f"Investment surge in {domain} companies signals market confidence"},
        {"source": "NewsAPI", "content": f"Research reveals consumer trends shifting toward {domain} solutions"},
        {"source": "NewsAPI", "content": f"International summit addresses future of {domain} innovation"}
    ]
    
    return {
        "status": "success",
        "articles": mock_articles
    }


# Define the NewsAPI search agent
news_scraper_agent = LlmAgent(
    name="news_scraper_agent",
    model=LiteLlm(model="openai/gpt-4o"),
    description="Agent to mock searching NewsAPI.org for articles about a specific domain.",
    instruction=(
        "When requested, return a mock list of news articles about the specified domain. "
        "The articles should be realistic news headlines and relevant to the requested domain. "
        "Always use the search_news function to generate mock news content."
    ),
    tools=[search_news],
)


if __name__ == "__main__":
    result = search_news("Healthcare")
    print(result)