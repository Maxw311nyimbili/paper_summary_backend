import os
from groq import Groq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Groq client
client = None
try:
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        logger.info(f"GROQ_API_KEY found (length: {len(api_key)})")
        client = Groq(api_key=api_key)
        logger.info("Groq client initialized successfully.")
    else:
        logger.error("GROQ_API_KEY not found in environment variables. Please check your .env file.")
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {e}")

def summarize_text(text: str) -> str:
    """
    Summarizes the given text using Groq's LLM API.
    """
    if not client:
        return "Groq API is not available. Please set GROQ_API_KEY environment variable."
    
    if not text or len(text.strip()) == 0:
        return ""
    
    # Truncate text if too long (Groq has token limits)
    # Roughly 8000 characters ~ 2000 tokens
    truncated_text = text[:8000]
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert research assistant. Summarize academic papers clearly and concisely, capturing the main research question, methodology, key findings, and implications. Keep summaries between 150-250 words."
                },
                {
                    "role": "user",
                    "content": f"Please provide a comprehensive summary of this research paper:\n\n{truncated_text}"
                }
            ],
            model="llama-3.3-70b-versatile",  # Fast and high-quality model
            temperature=0.3,  # Lower temperature for more focused summaries
            max_tokens=400,
        )
        
        return chat_completion.choices[0].message.content.strip()
    
    except Exception as e:
        logger.error(f"Error during Groq summarization: {e}")
        return f"Error generating summary: {str(e)}"
