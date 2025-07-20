import datetime
import os
import re
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import fitz  # PyMuPDF

# Import the new agents using absolute imports
try:
    from agents.analysis import analyze_collected_results
    from agents.summarization import generate_summary
except ImportError:
    # Fallback: try relative import from parent directory
    import sys
    import os
    # Add the project root to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        from agents.analysis import analyze_collected_results
        from agents.summarization import generate_summary
    except ImportError:
        # If still can't import, define the functions locally
        def analyze_collected_results(inputs: dict) -> dict:
            """Fallback analysis function when agents module is not available."""
            return {
                "status": "error",
                "error_message": "Analysis function not available - agents module not found."
            }
        
        def generate_summary(content: str) -> dict:
            """Fallback summary function when agents module is not available."""
            return {
                "status": "error", 
                "error_message": "Summary function not available - agents module not found."
            }


def analyze_local_pdfs() -> dict:
    """Analyzes all PDF files in the local docs/ folder.
    
    Scans the docs/ directory for PDF files, extracts text content,
    and preprocesses it by removing excessive whitespace and converting to lowercase.
    Limits text extraction to prevent token limit issues.
    
    Returns:
        dict: Status and documents data or error message.
    """
    # Get the directory where this agent file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docs_folder = os.path.join(current_dir, "docs")
    
    # Check if docs folder exists
    if not os.path.exists(docs_folder):
        return {
            "status": "error",
            "error_message": f"The '{docs_folder}' folder does not exist."
        }
    
    # Find all PDF files
    pdf_files = []
    for filename in os.listdir(docs_folder):
        if filename.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(docs_folder, filename))
    
    if not pdf_files:
        print(f"No PDF files found in {docs_folder}/ folder.")
        return {
            "status": "error",
            "error_message": f"No PDF files found in {docs_folder}/ folder."
        }
    
    print(f"Found {len(pdf_files)} PDF file(s) to analyze.")
    
    documents = []
    
    for file_path in pdf_files:
        try:
            print(f"Processing: {file_path}")
            
            # Extract text using PyMuPDF with size limits
            doc = fitz.open(file_path)
            text_content = ""
            max_pages = 10  # Limit to first 10 pages
            max_chars_per_page = 5000  # Limit characters per page
            total_pages = doc.page_count
            
            for page_num in range(min(total_pages, max_pages)):
                page = doc[page_num]
                page_text = page.get_text()
                
                # Limit characters per page
                if len(page_text) > max_chars_per_page:
                    page_text = page_text[:max_chars_per_page] + "... [truncated]"
                
                text_content += page_text + "\n"
            
            # Preprocess text
            # Remove excessive whitespace and newlines
            cleaned_text = re.sub(r'\s+', ' ', text_content.strip())
            
            # Limit total text size to prevent token limit issues
            max_total_chars = 15000  # Conservative limit
            if len(cleaned_text) > max_total_chars:
                cleaned_text = cleaned_text[:max_total_chars] + "... [content truncated due to size]"
            
            # Convert to lowercase
            cleaned_text = cleaned_text.lower()
            
            # Add file info
            file_info = {
                "file_path": file_path,
                "text": cleaned_text,
                "total_pages": total_pages,
                "pages_processed": min(total_pages, max_pages),
                "text_length": len(cleaned_text),
                "note": "Text was truncated to stay within token limits" if len(cleaned_text) >= max_total_chars else "Full content processed"
            }
            
            # Close the document after we've extracted all needed information
            doc.close()
            
            documents.append(file_info)
            
            print(f"Successfully processed: {file_path} ({len(cleaned_text)} characters)")
            
        except Exception as e:
            print(f"Failed to process {file_path}: {str(e)}")
            documents.append({
                "file_path": file_path,
                "text": f"Error processing file: {str(e)}",
                "error": str(e)
            })
    
    return {
        "status": "success",
        "documents": documents,
        "note": "Large PDFs were truncated to prevent token limit issues. Consider using smaller files or breaking them into chunks."
    }


def search_news_articles(domain: str) -> dict:
    """
    Search for news articles about a specific domain using the news scraper agent.
    
    Args:
        domain (str): The domain keyword to search for
        
    Returns:
        dict: Status and news articles data or error message
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


def search_x_com_posts(domain: str) -> dict:
    """
    Search for X.com (Twitter) posts about a specific domain using the X scraper agent.
    
    Args:
        domain (str): The domain keyword to search for
        
    Returns:
        dict: Status and X.com posts data or error message
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


def get_comprehensive_analysis(domain: str) -> dict:
    """
    Get comprehensive analysis by searching both news and social media for a domain.
    
    Args:
        domain (str): The domain keyword to analyze
        
    Returns:
        dict: Combined analysis from news and social media sources
    """
    if not domain or domain.strip() == "":
        return {
            "status": "error",
            "error_message": "Domain keyword required for analysis."
        }
    
    # Get news articles
    news_result = search_news_articles(domain)
    
    # Get X.com posts
    x_com_result = search_x_com_posts(domain)
    
    # Combine results
    analysis = {
        "status": "success",
        "domain": domain,
        "timestamp": datetime.datetime.now().isoformat(),
        "news_analysis": news_result,
        "social_media_analysis": x_com_result,
        "summary": {
            "total_news_articles": len(news_result.get("articles", [])) if news_result.get("status") == "success" else 0,
            "total_social_posts": len(x_com_result.get("posts", [])) if x_com_result.get("status") == "success" else 0,
            "sources_analyzed": ["NewsAPI", "X.com"]
        }
    }
    
    return analysis


def search_research_papers(domain: str) -> dict:
    """
    Search for research papers about a specific domain using the research scraper agent.
    
    Args:
        domain (str): The domain keyword to search for
        
    Returns:
        dict: Status and research papers data or error message
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


root_agent = LlmAgent(
    name="market_trend_coordinator_agent",
    model=LiteLlm(model="openai/gpt-4o"), # LiteLLM model string format
    description=(
        "Autonomous agentic system that monitors, collects, analyzes, and summarizes emerging trends across industries "
        "(fintech, healthcare, retail, etc.) by aggregating data from multiple sources including news articles, "
        "social media posts, research publications, and local documents. The system provides comprehensive trend analysis "
        "and executive summaries for strategic decision-making."
    ),
    instruction=(
        "You are an autonomous agentic system designed to monitor and analyze emerging trends across different industries. "
        "Your goal is to collect, analyze, and summarize trend data from multiple sources to provide actionable insights. "
        ""
        "Your workflow for trend analysis:"
        "1. COLLECT: Use data collection tools to gather information from multiple sources"
        "   - Use search_news_articles() to find relevant news articles about the domain"
        "   - Use search_x_com_posts() to find relevant social media posts and discussions"
        "   - Use search_research_papers() to find academic research and publications"
        "   - Use analyze_local_pdfs() to analyze local documents if available"
        "   - Use get_comprehensive_analysis() to get both news and social media analysis"
        ""
        "2. ANALYZE: Process collected data using the analysis function"
        "   - Use analyze_collected_results() to combine results from news, research, and social media sources"
        "   - Identify key keywords, topics, and patterns across all sources"
        "   - Extract meaningful insights and trends from the aggregated data"
        ""
        "3. SUMMARIZE: Generate executive summaries using the summarization function"
        "   - Use generate_summary() to create comprehensive executive-level summaries of findings"
        "   - Highlight strategic implications and actionable insights"
        "   - Provide recommendations based on trend analysis"
        ""
        "When users request trend analysis for specific domains or industries:"
        "- First collect comprehensive data from all available sources"
        "- Then analyze the collected data to identify patterns and insights"
        "- Finally generate an executive summary with strategic recommendations"
        ""
        "Focus on providing comprehensive, data-driven insights that help users understand:"
        "- Emerging technologies and innovations in the domain"
        "- Market trends and industry developments"
        "- Investment opportunities and strategic implications"
        "- Competitive intelligence and market positioning"
        ""
        "Be proactive in suggesting relevant domains to analyze and provide actionable insights "
        "that support strategic decision-making and market positioning."
    ),
    tools=[search_news_articles, search_x_com_posts, search_research_papers, get_comprehensive_analysis, analyze_local_pdfs, analyze_collected_results, generate_summary],
)
