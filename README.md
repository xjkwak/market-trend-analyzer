# Document Analysis Agent

A Python-based intelligent agent built with Google's Agent Development Kit (ADK) that analyzes PDF documents from a local directory. This project demonstrates how to create an agent that can process and analyze text content from PDF files using advanced AI capabilities.

## Features

- **PDF Document Analysis**: Automatically scans and processes PDF files from a local `docs/` directory
- **Text Extraction**: Extracts and preprocesses text content from PDF documents
- **Content Summarization**: Provides summaries and key insights from document content
- **Smart Processing**: Handles large documents with intelligent truncation to stay within token limits
- **Error Handling**: Graceful handling of file processing errors and edge cases
- **Extensible Design**: Easy to add new document processing capabilities

## Project Structure

```
adk1/
├── app/
│   └── multi_tool_agent/
│       ├── __init__.py
│       ├── agent.py
│       └── docs/
│           └── [PDF files to analyze]
├── agents/
│   └── social_scraper.py
├── requirements.txt
├── setup_openai.py
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

The agent is configured with one main tool:

- **Document Analysis Tool** (`analyze_local_pdfs`): Scans the `docs/` directory for PDF files and analyzes their content

### Setting Up Documents

1. Create a `docs/` folder in the `app/multi_tool_agent/` directory
2. Place PDF files you want to analyze in this folder
3. The agent will automatically detect and process all PDF files

### Example Queries

The agent can handle natural language queries such as:
- "Analyze the documents in the docs folder"
- "What are the main topics in the PDF files?"
- "Summarize the content of the documents"
- "What key information can you find in the PDFs?"

### Agent Configuration

The agent is configured with:
- **Model**: `openai/gpt-4o` (via LiteLLM)
- **Name**: `document_analysis_agent`
- **Description**: Agent to analyze text content from local PDF documents
- **Instruction**: Analyzes PDF documents and provides summaries and insights

## API Reference

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

Run the test file to verify the agent functionality:

```bash
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

- `agents/social_scraper.py`: Additional agent for social media scraping
- `setup_openai.py`: OpenAI API configuration
- `test_document_analyzer.py`: Test file for the document analyzer
- `CLAUDE.md`: Additional documentation
