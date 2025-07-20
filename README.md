# Market Trend Coordinator Agent

A Python-based intelligent coordinator agent built with Google's Agent Development Kit (ADK) that analyzes market trends by searching news articles and social media posts. This project demonstrates how to create a coordinator agent that can interact with multiple sub-agents to provide comprehensive market insights.

## Features

- **Market Trend Analysis**: Searches news articles and social media posts for specific domains or industries
- **Multi-Source Data Collection**: Integrates data from NewsAPI and X.com (Twitter) sources
- **Coordinator Agent Architecture**: Uses sub-agents for specialized data collection tasks
- **Comprehensive Insights**: Combines information from multiple sources for holistic analysis
- **PDF Document Analysis**: Also capable of analyzing local PDF documents for additional context
- **Smart Processing**: Handles large documents with intelligent truncation to stay within token limits
- **Error Handling**: Graceful handling of API errors and edge cases
- **Extensible Design**: Easy to add new data sources and analysis capabilities

## Project Structure

```
adk1/
├── app/
│   └── multi_tool_agent/
│       ├── __init__.py
│       ├── agent.py          # Coordinator agent
│       └── docs/
│           └── [PDF files to analyze]
├── agents/
│   ├── news_scraper.py       # News API sub-agent
│   ├── x_scraper.py          # X.com (Twitter) sub-agent
│   └── social_scraper.py     # Reddit sub-agent
├── requirements.txt
├── setup_openai.py
├── test_coordinator_agent.py # Test file for coordinator agent
├── test_document_analyzer.py
├── CLAUDE.md
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd adk1
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

The coordinator agent is configured with multiple tools:

- **News Search Tool** (`search_news_articles`): Searches for news articles about specific domains or topics
- **Social Media Search Tool** (`search_x_com_posts`): Searches for X.com (Twitter) posts about specific domains or topics
- **Comprehensive Analysis Tool** (`get_comprehensive_analysis`): Combines news and social media analysis for a domain
- **Document Analysis Tool** (`analyze_local_pdfs`): Scans the `docs/` directory for PDF files and analyzes their content

### Setting Up Documents

1. Create a `docs/` folder in the `app/multi_tool_agent/` directory
2. Place PDF files you want to analyze in this folder
3. The agent will automatically detect and process all PDF files

### Example Queries

The coordinator agent can handle natural language queries such as:
- "Search for news articles about Fintech industry trends"
- "Find social media posts about AI developments"
- "Get comprehensive analysis of the healthcare sector"
- "What are the latest trends in renewable energy?"
- "Analyze the documents in the docs folder"
- "What are the main topics in the PDF files?"
- "Summarize the content of the documents"
- "What key information can you find in the PDFs?"

### Agent Configuration

The coordinator agent is configured with:
- **Model**: `openai/gpt-4o` (via LiteLLM)
- **Name**: `market_trend_coordinator_agent`
- **Description**: Coordinator agent that analyzes market trends by searching news articles and social media posts
- **Instruction**: Coordinates multiple data sources to provide comprehensive market insights and analysis

## API Reference

### `search_news_articles(domain: str) -> dict`

Searches for news articles about a specific domain using the news scraper agent.

**Args:**
- `domain` (str): The domain keyword to search for

**Returns:**
- `dict`: Status and news articles data or error message

**Example Response:**
```python
{
    "status": "success",
    "articles": [
        {"source": "NewsAPI", "content": "Breaking: Major Fintech company announces breakthrough innovation"},
        {"source": "NewsAPI", "content": "Industry experts predict significant growth in Fintech sector"}
    ]
}
```

### `search_x_com_posts(domain: str) -> dict`

Searches for X.com (Twitter) posts about a specific domain using the X scraper agent.

**Args:**
- `domain` (str): The domain keyword to search for

**Returns:**
- `dict`: Status and X.com posts data or error message

**Example Response:**
```python
{
    "status": "success",
    "posts": [
        {"source": "X.com", "content": "Breaking news in AI industry today! #innovation"},
        {"source": "X.com", "content": "New developments in AI are changing the game"}
    ]
}
```

### `get_comprehensive_analysis(domain: str) -> dict`

Gets comprehensive analysis by searching both news and social media for a domain.

**Args:**
- `domain` (str): The domain keyword to analyze

**Returns:**
- `dict`: Combined analysis from news and social media sources

**Example Response:**
```python
{
    "status": "success",
    "domain": "AI",
    "timestamp": "2025-01-27T10:30:00",
    "news_analysis": {...},
    "social_media_analysis": {...},
    "summary": {
        "total_news_articles": 10,
        "total_social_posts": 10,
        "sources_analyzed": ["NewsAPI", "X.com"]
    }
}
```

### `analyze_local_pdfs() -> dict`

Analyzes all PDF files in the local `docs/` folder.

**Returns:**
- `dict`: Status and documents data or error message

**Example Response:**
```python
{
    "status": "success",
    "documents": [
        {
            "file_path": "/path/to/document.pdf",
            "text": "extracted and processed text content...",
            "total_pages": 15,
            "pages_processed": 10,
            "text_length": 12500,
            "note": "Text was truncated to stay within token limits"
        }
    ],
    "note": "Large PDFs were truncated to prevent token limit issues."
}
```

## Processing Details

### Text Extraction Limits

The agent implements several safeguards to handle large documents:

- **Page Limit**: Processes maximum 10 pages per document
- **Character Limit**: Maximum 5,000 characters per page
- **Total Limit**: Maximum 15,000 characters per document
- **Preprocessing**: Removes excessive whitespace and converts to lowercase

### Error Handling

The agent includes comprehensive error handling:
- Missing `docs/` directory returns appropriate error messages
- File processing errors are captured and reported
- Invalid PDF files are handled gracefully
- All functions return consistent response formats

## Dependencies

- `google-adk`: Google's Agent Development Kit
- `litellm`: LiteLLM for model integration
- `openai`: OpenAI API integration
- `python-dotenv`: Environment variable management
- `PyMuPDF`: PDF text extraction and processing
- `datetime`: Python's datetime module
- `zoneinfo`: Timezone information handling

## Development

### Adding New Document Types

To add support for new document formats:

1. Update the `analyze_local_pdfs` function to handle new file types
2. Add appropriate text extraction libraries
3. Test the new functionality

### Adding New Analysis Tools

To add new analysis capabilities:

1. Create a new function with appropriate docstrings
2. Add the function to the `tools` list in the `root_agent` configuration
3. Update the agent's description and instruction if needed

### Configuration

The agent can be customized by modifying:
- Model selection in the `LiteLlm` configuration
- Processing limits in the `analyze_local_pdfs` function
- Agent instructions and descriptions

## How to run

```
cd market-trend-analyzer/app
adk web
```

## Testing

Run the test files to verify the agent functionality:

```bash
# Test the coordinator agent
python test_coordinator_agent.py

# Test the document analyzer
python test_document_analyzer.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please open an issue in the repository.

## Related Files

- `agents/news_scraper.py`: News API sub-agent for searching news articles
- `agents/x_scraper.py`: X.com (Twitter) sub-agent for searching social media posts
- `agents/social_scraper.py`: Reddit sub-agent for social media scraping
- `setup_openai.py`: OpenAI API configuration
- `test_coordinator_agent.py`: Test file for the coordinator agent
- `test_document_analyzer.py`: Test file for the document analyzer
- `CLAUDE.md`: Additional documentation
