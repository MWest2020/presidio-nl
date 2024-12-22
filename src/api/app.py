"""FastAPI application for text analysis and anonymization."""
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from ..analyzer.engine import DutchTextAnalyzer
from ..anonymizer.engine import DutchTextAnonymizer

# Get configuration from environment variables
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_ROOT_PATH = os.getenv("API_ROOT_PATH", "/api/v1")

app = FastAPI(
    title="Presidio-NL API",
    description="API voor Nederlandse tekst analyse en anonimisatie",
    version="0.1.0",
    root_path=API_ROOT_PATH
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configureer dit in productie
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
analyzer = DutchTextAnalyzer()
anonymizer = DutchTextAnonymizer()

class TextRequest(BaseModel):
    """Request model for text analysis and anonymization."""
    text: str
    entities: Optional[List[str]] = None

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        """Validate that text is not empty."""
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()

    @field_validator("entities")
    @classmethod
    def validate_entities(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate that entities are supported."""
        if v is not None:
            supported_entities = {"PERSON", "LOCATION", "PHONE_NUMBER", "IBAN"}
            invalid_entities = [e for e in v if e not in supported_entities]
            if invalid_entities:
                raise ValueError(f"Unsupported entities: {', '.join(invalid_entities)}")
        return v

class AnalysisResult(BaseModel):
    """Response model for text analysis."""
    entity_type: str
    text: str
    start: int
    end: int
    score: float

class AnalysisResponse(BaseModel):
    """Response model containing all analysis results."""
    results: List[AnalysisResult]

class AnonymizationResponse(BaseModel):
    """Response model for text anonymization."""
    original_text: str
    anonymized_text: str
    entities_found: List[AnalysisResult]

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):
    """
    Analyze text for entities.
    
    Returns a list of found entities with their positions and scores.
    """
    try:
        results = analyzer.analyze_text(request.text, request.entities)
        
        analysis_results = [
            AnalysisResult(
                entity_type=result.entity_type,
                text=request.text[result.start:result.end],
                start=result.start,
                end=result.end,
                score=result.score
            )
            for result in results
        ]
        
        return AnalysisResponse(results=analysis_results)
    
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing text: {str(e)}"
        )

@app.post("/anonymize", response_model=AnonymizationResponse)
async def anonymize_text(request: TextRequest):
    """
    Analyze and anonymize text.
    
    Returns the anonymized text along with information about what was anonymized.
    """
    try:
        # First analyze
        results = analyzer.analyze_text(request.text, request.entities)
        
        # Then anonymize
        anonymized = anonymizer.anonymize_text(request.text, results)
        
        # Create response
        analysis_results = [
            AnalysisResult(
                entity_type=result.entity_type,
                text=request.text[result.start:result.end],
                start=result.start,
                end=result.end,
                score=result.score
            )
            for result in results
        ]
        
        return AnonymizationResponse(
            original_text=request.text,
            anonymized_text=anonymized,
            entities_found=analysis_results
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error anonymizing text: {str(e)}"
        ) 