"""
Summarization Agent for generating executive summaries from analysis results.
"""

from typing import Dict
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


def generate_summary(analysis_results: dict) -> dict:
    """
    Generate an executive-level plain-text summary from analysis results.
    
    Args:
        analysis_results (dict): Output from AnalysisAgent containing keywords, topics, and summary notes
                               Expected keys: 'keywords', 'topics', 'summary_notes'
                               
    Returns:
        dict: Executive summary with status and summary text
    """
    if not analysis_results or not isinstance(analysis_results, dict):
        return {
            "status": "error",
            "error_message": "Invalid analysis results provided. Expected dictionary with analysis data."
        }
    
    # Check if analysis was successful
    if analysis_results.get('status') != 'success':
        error_msg = analysis_results.get('error_message', 'Unknown error in analysis')
        return {
            "status": "error",
            "error_message": f"Analysis results indicate failure: {error_msg}"
        }
    
    # Extract components from analysis results
    keywords = analysis_results.get('keywords', [])
    topics = analysis_results.get('topics', [])
    summary_notes = analysis_results.get('summary_notes', '')
    
    if not keywords and not topics:
        return {
            "status": "error",
            "error_message": "No meaningful keywords or topics found in analysis results."
        }
    
    # Generate executive summary
    summary_parts = []
    
    # Opening statement
    if topics:
        if len(topics) == 1:
            summary_parts.append(f"Executive Summary: Analysis reveals a primary focus on {topics[0].lower()}.")
        else:
            summary_parts.append(f"Executive Summary: Analysis reveals key themes across {len(topics)} major areas: {', '.join(topics).lower()}.")
    else:
        summary_parts.append("Executive Summary: Analysis of collected data reveals diverse content patterns.")
    
    # Key findings section
    if keywords:
        top_keywords = keywords[:5]  # Focus on top 5 keywords
        if len(top_keywords) >= 3:
            summary_parts.append(f"Key findings center around {top_keywords[0]}, {top_keywords[1]}, and {top_keywords[2]}, indicating strong market interest and activity in these areas.")
        else:
            summary_parts.append(f"Key findings highlight {', '.join(top_keywords)} as primary areas of focus.")
    
    # Topic-specific insights
    if topics:
        topic_insights = []
        
        if 'Technology & Innovation' in topics:
            topic_insights.append("significant technological advancement and innovation activity")
        if 'Finance & Investment' in topics:
            topic_insights.append("active financial markets and investment opportunities")
        if 'Healthcare & Medical' in topics:
            topic_insights.append("developments in healthcare and medical research")
        if 'Business & Industry' in topics:
            topic_insights.append("business growth and industrial development")
        if 'Research & Analysis' in topics:
            topic_insights.append("ongoing research initiatives and analytical studies")
        if 'Market Trends' in topics:
            topic_insights.append("emerging market trends and consumer behavior shifts")
        
        if topic_insights:
            if len(topic_insights) == 1:
                summary_parts.append(f"The analysis indicates {topic_insights[0]}.")
            else:
                summary_parts.append(f"The analysis indicates {', '.join(topic_insights[:-1])}, and {topic_insights[-1]}.")
    
    # Strategic implications
    strategic_implications = []
    
    if 'fintech' in [k.lower() for k in keywords[:5]] or 'Finance & Investment' in topics:
        strategic_implications.append("opportunities in financial technology and digital payment solutions")
    
    if any(tech_word in [k.lower() for k in keywords[:5]] for tech_word in ['technology', 'tech', 'ai', 'digital']):
        strategic_implications.append("potential for technology-driven transformation and automation")
    
    if 'healthcare' in [k.lower() for k in keywords[:5]] or 'Healthcare & Medical' in topics:
        strategic_implications.append("growth prospects in healthcare innovation and medical technology")
    
    if strategic_implications:
        summary_parts.append(f"Strategic implications suggest {', '.join(strategic_implications)}.")
    
    # Conclusion
    if summary_notes:
        summary_parts.append(f"Overall assessment: {summary_notes}")
    else:
        summary_parts.append("The combined analysis provides valuable insights for strategic decision-making and market positioning.")
    
    # Recommendations
    if len(keywords) >= 3:
        summary_parts.append(f"Recommendation: Continue monitoring developments in {keywords[0]} and {keywords[1]} for emerging opportunities and competitive intelligence.")
    
    # Join all parts into final summary
    final_summary = " ".join(summary_parts)
    
    return {
        "status": "success",
        "summary": final_summary
    }


# Define the Summarization agent
summarization_agent = LlmAgent(
    name="summarization_agent",
    model=LiteLlm(model="openai/gpt-4o"),
    description="Agent that synthesizes an executive summary of trends and insights.",
    instruction=(
        "Provide an insightful summary of the dominant trends, topics, and keywords found across news, research, and X.com posts. "
        "Generate executive-level summaries that highlight key findings, strategic implications, and actionable insights. "
        "Always use the generate_summary function to process analysis results."
    ),
    tools=[generate_summary],
)


if __name__ == "__main__":
    # Example for SummarizationAgent
    analysis_result = {
        "status": "success",
        "keywords": ["fintech", "blockchain", "payments", "innovation", "digital"],
        "topics": ["Finance & Investment", "Technology & Innovation"],
        "summary_notes": "Analysis reveals strong focus on financial technology innovation."
    }
    summary = generate_summary(analysis_result)
    print(summary)