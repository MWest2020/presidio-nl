"""Pydantic models for the API."""
from typing import List, Optional
from pydantic import BaseModel, validator

class TextRequest(BaseModel):
    """Request model for text analysis and anonymization."""
    text: str
    entities: Optional[List[str]] = None

    @validator("text")
    def text_must_not_be_empty(cls, v: str) -> str:
        """Validate that text is not empty."""
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()

    @validator("entities")
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