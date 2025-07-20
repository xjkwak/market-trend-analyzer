"""
Analysis Agent for processing and analyzing collected content from multiple sources.
"""

import re
from collections import Counter
from typing import Dict, List
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


def analyze_collected_results(inputs: dict) -> dict:
    """
    Analyze combined content from news, research, and social media sources.
    
    Args:
        inputs (dict): Dictionary containing lists of posts/articles/papers from different sources
                      Expected keys: 'news', 'research', 'social'
                      
    Returns:
        dict: Analysis results with keywords, topics, and summary notes
    """
    if not inputs or not isinstance(inputs, dict):
        return {
            "status": "error",
            "error_message": "Invalid inputs provided. Expected dictionary with content data."
        }
    
    # Check if inputs contain any content
    total_items = 0
    all_text = []
    
    # Process news content
    news_items = inputs.get('news', [])
    if isinstance(news_items, list):
        for item in news_items:
            if isinstance(item, dict) and 'content' in item:
                all_text.append(item['content'])
                total_items += 1
    
    # Process research content
    research_items = inputs.get('research', [])
    if isinstance(research_items, list):
        for item in research_items:
            if isinstance(item, dict):
                # Research items might have 'title' instead of 'content'
                content = item.get('content') or item.get('title', '')
                if content:
                    all_text.append(content)
                    total_items += 1
    
    # Process social media content
    social_items = inputs.get('social', [])
    if isinstance(social_items, list):
        for item in social_items:
            if isinstance(item, dict) and 'content' in item:
                all_text.append(item['content'])
                total_items += 1
    
    # Also handle the case where inputs might be a direct result from get_comprehensive_analysis
    if total_items == 0 and isinstance(inputs, dict):
        # Check if this is a comprehensive analysis result
        if 'news_analysis' in inputs and 'social_media_analysis' in inputs:
            news_analysis = inputs.get('news_analysis', {})
            social_analysis = inputs.get('social_media_analysis', {})
            
            # Extract news articles
            if news_analysis.get('status') == 'success':
                news_articles = news_analysis.get('articles', [])
                for article in news_articles:
                    if isinstance(article, dict) and 'content' in article:
                        all_text.append(article['content'])
                        total_items += 1
            
            # Extract social posts
            if social_analysis.get('status') == 'success':
                social_posts = social_analysis.get('posts', [])
                for post in social_posts:
                    if isinstance(post, dict) and 'content' in post:
                        all_text.append(post['content'])
                        total_items += 1
    
    if total_items == 0:
        return {
            "status": "error",
            "error_message": "No valid content found in inputs. Expected 'news', 'research', and 'social' keys with content arrays, or a comprehensive analysis result."
        }
    
    # Combine all text for analysis
    combined_text = ' '.join(all_text).lower()
    
    # Extract keywords (simple tokenization and filtering)
    # Remove punctuation and split into words
    words = re.findall(r'\b[a-zA-Z]+\b', combined_text)
    
    # Define common stopwords to filter out
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'among', 'this', 'that', 'these', 'those', 'i',
        'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
        'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
        'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is',
        'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
        'do', 'does', 'did', 'doing', 'will', 'would', 'should', 'could', 'can', 'may',
        'might', 'must', 'shall', 'sample', 'about', 'latest', 'new', 'today', 'news'
    }
    
    # Filter out stopwords and short words
    filtered_words = [word for word in words if len(word) > 2 and word not in stopwords]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    # Get top keywords (most frequent words)
    top_keywords = [word for word, count in word_counts.most_common(10)]
    
    # Identify dominant topics/themes (simplified approach)
    topics = []
    
    # Look for common business/technology themes
    theme_patterns = {
        'Technology & Innovation': ['technology', 'innovation', 'tech', 'ai', 'artificial', 'intelligence', 'machine', 'learning', 'digital', 'algorithm'],
        'Finance & Investment': ['finance', 'fintech', 'investment', 'money', 'financial', 'banking', 'payment', 'market', 'economic', 'economy'],
        'Healthcare & Medical': ['healthcare', 'health', 'medical', 'medicine', 'patient', 'treatment', 'clinical', 'pharmaceutical'],
        'Business & Industry': ['business', 'industry', 'company', 'corporate', 'startup', 'enterprise', 'commercial', 'growth', 'development'],
        'Research & Analysis': ['research', 'analysis', 'study', 'data', 'findings', 'report', 'paper', 'academic', 'scientific'],
        'Market Trends': ['trend', 'trending', 'market', 'growth', 'increase', 'sector', 'industry', 'demand', 'consumer']
    }
    
    for theme, keywords in theme_patterns.items():
        theme_score = sum(1 for keyword in keywords if keyword in filtered_words)
        if theme_score > 0:
            topics.append(theme)
    
    # Generate summary notes
    if topics:
        dominant_topics = topics[:3]  # Top 3 themes
        summary_notes = f"Analysis of {total_items} items reveals dominant themes in {', '.join(dominant_topics)}. "
        summary_notes += f"Key recurring terms include {', '.join(top_keywords[:5])}."
    else:
        summary_notes = f"Analysis of {total_items} items shows diverse content without clear dominant themes."
    
    return {
        "status": "success",
        "keywords": top_keywords,
        "topics": topics,
        "summary_notes": summary_notes
    }


# Define the Analysis agent
analysis_agent = LlmAgent(
    name="analysis_agent",
    model=LiteLlm(model="openai/gpt-4o"),
    description="Agent to analyze collected content from news, research, and X.com posts.",
    instruction=(
        "Analyze the combined results from multiple sources and identify key topics and keywords. "
        "Extract meaningful patterns from news articles, research papers, and social media posts. "
        "Always use the analyze_collected_results function to process the input data."
    ),
    tools=[analyze_collected_results],
)


if __name__ == "__main__":
    # Example for AnalysisAgent
    inputs = {
        "news": [{"source": "NewsAPI", "content": "Sample news about fintech innovation and digital payments."}],
        "research": [{"source": "arXiv", "title": "Research on blockchain technology and cryptocurrency applications."}],
        "social": [{"source": "X.com", "content": "Tweet about fintech payments and mobile banking trends."}]
    }
    result = analyze_collected_results(inputs)
    print(result)