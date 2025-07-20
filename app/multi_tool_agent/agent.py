import datetime
import os
import re
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import fitz  # PyMuPDF

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


root_agent = LlmAgent(
    name="document_analysis_agent",
    model=LiteLlm(model="openai/gpt-4o"), # LiteLLM model string format
    description=(
        "Agent to analyze text content from local PDF documents."
    ),
    instruction=(
        "You are an agent that can read and analyze local PDF documents from the docs/ folder. "
        "When analyzing PDFs, provide a summary of the content, key topics, and any important "
        "information found. If the content was truncated due to size limits, mention this and "
        "suggest what additional analysis might be possible with the full document. "
        "Be helpful and provide actionable insights from the document content."
    ),
    tools=[analyze_local_pdfs],
)
