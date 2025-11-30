import io
import yake
from pypdf import PdfReader
from typing import List

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file byte stream."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def extract_keywords(text: str, max_ngram_size: int = 2, num_keywords: int = 10) -> List[str]:
    """Extracts keywords from text using YAKE."""
    try:
        kw_extractor = yake.KeywordExtractor(lan="en", n=max_ngram_size, dedupLim=0.9, top=num_keywords, features=None)
        keywords = kw_extractor.extract_keywords(text)
        # keywords is a list of tuples (keyword, score) - lower score is better
        # We just return the keyword strings
        return [kw[0] for kw in keywords]
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

def extract_insights(text: str, num_insights: int = 5) -> List[str]:
    """
    Extracts key insights (sentences) from the text.
    This is a simple extractive summary approach based on sentence length and position for now,
    as a full extractive model might be too heavy alongside the abstractive one.
    """
    sentences = text.split('. ')
    # Filter sentences that are too short or too long
    valid_sentences = [s.strip() for s in sentences if 20 < len(s) < 300]
    
    # Simple heuristic: take unique sentences from the beginning and middle
    # In a real app, we'd use a ranking algorithm (TextRank)
    seen = set()
    insights = []
    for s in valid_sentences:
        if s not in seen:
            insights.append(s)
            seen.add(s)
            if len(insights) >= num_insights:
                break
    return insights
