# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based multi-tool agent built with Google's Agent Development Kit (ADK) that provides weather and time information for cities. The agent supports both Google Gemini and OpenAI models via LiteLLM.

## Architecture

The project uses a modular architecture with:
- **ADK Framework**: Uses Google's Agent Development Kit for agent orchestration
- **LiteLLM Integration**: Supports multiple LLM providers (currently configured for OpenAI GPT-4)
- **Tool-based Architecture**: Functions are exposed as tools to the agent
- **Simple Function Tools**: `get_weather()` and `get_current_time()` provide core functionality

Key files:
- `app/multi_tool_agent/agent.py`: Main agent definition with tools and LLM configuration
- `setup_openai.py`: Setup script for testing OpenAI integration
- `.env.sample`: Environment variable template

## Development Commands

### Installation
```bash
pip install -r requirements.txt
```

### Environment Setup
```bash
# Copy environment template
cp app/multi_tool_agent/.env.sample app/multi_tool_agent/.env

# Set required API keys in .env:
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key  # If using Gemini
```

### Testing the Agent
```bash
python setup_openai.py
```

### Running the Agent
```python
from app.multi_tool_agent.agent import root_agent
response = root_agent.run("What's the weather in New York?")
```

## Agent Configuration

The agent can be configured with two different model backends:

1. **OpenAI (Current)**: Uses `LlmAgent` with `LiteLlm(model="openai/gpt-4o")`
2. **Google Gemini (Commented)**: Uses `Agent` with `model="gemini-2.0-flash"`

To switch models, uncomment the appropriate agent configuration in `agent.py:59-69` or `agent.py:71-81`.

## Tool Functions

Both tools return consistent response format:
```python
{
    "status": "success" | "error",
    "report": "response message",      # on success
    "error_message": "error details"  # on error
}
```

Current city support is limited to "New York" with hardcoded responses. To add new cities, update both `get_weather()` and `get_current_time()` functions with appropriate data sources and timezone mappings.

## Dependencies

- `google-adk`: Core agent framework
- `litellm`: Multi-provider LLM interface
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management

## Upcoming Features

- **Social Media Scraper Agent**: 
  * Implement Reddit scraping functionality using PRAW library
  * Create `SocialMediaScraperAgent` in `agents/social_scraper.py`
  * Support searching Reddit posts by domain keyword
  * Fetch up to 10 posts per query
  * Gracefully handle API and connection exceptions
  * Return structured post data with source and content