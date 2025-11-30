from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from text_utils import extract_text_from_pdf, extract_keywords, extract_insights
from summarizer import summarize_text

app = FastAPI(title="Paper Summary API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeResponse(BaseModel):
    summary: str
    keywords: List[str]
    insights: List[str]

@app.get("/")
def read_root():
    return {"message": "Paper Summary API is running."}

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_endpoint(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Endpoint to summarize text. Accepts either a file upload (PDF/TXT) OR raw text.
    """
    content = ""

    # Handle File Upload
    if file:
        if file.content_type == "application/pdf":
            file_bytes = await file.read()
            content = extract_text_from_pdf(file_bytes)
        elif file.content_type == "text/plain":
            content = (await file.read()).decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF or TXT.")
    
    # Handle Raw Text
    elif text:
        content = text
    
    else:
        raise HTTPException(status_code=400, detail="No content provided. Upload a file or provide text.")

    if not content.strip():
         raise HTTPException(status_code=400, detail="Extracted content is empty.")

    # Process Content
    summary = summarize_text(content)
    keywords = extract_keywords(content)
    insights = extract_insights(content)

    return SummarizeResponse(
        summary=summary,
        keywords=keywords,
        insights=insights
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
