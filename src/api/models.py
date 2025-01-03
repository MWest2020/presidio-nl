"""API models for request and response data."""
from typing import List, Dict, Optional
from pydantic import BaseModel

class TextRequest(BaseModel):
    """Request model for text analysis and anonymization."""
    text: str
    entities: Optional[List[str]] = None

class Entity(BaseModel):
    """Found entity in text."""
    entity_type: str
    text: str
    score: float

class AnalysisResponse(BaseModel):
    """Response model for text analysis."""
    text: str
    entities_found: List[Entity]

class EntityFound(BaseModel):
    """Found entity in text."""
    entity_type: str
    text: str
    score: float

class EntityDetail(BaseModel):
    """Detail of found entity."""
    text: str
    score: float

class AnonymizeResponse(BaseModel):
    """Response model for text anonymization."""
    original_text: str
    anonymized_text: str
    entities_found: List[EntityFound]

class ProcessResponse(BaseModel):
    """Response model for PDF processing."""
    total_entities: int
    entities_by_type: Dict[str, List[EntityDetail]]
    input_file: str
    output_file: str
    download_link: str
    message: Optional[str] = None
    error: Optional[str] = None 