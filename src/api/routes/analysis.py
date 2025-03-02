"""Routes for text analysis."""
from fastapi import APIRouter, HTTPException

from ..models import TextRequest, AnalysisResponse, Entity
from ...core.analyzer import DutchTextAnalyzer

router = APIRouter()
analyzer = DutchTextAnalyzer()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):
    """
    Analyze text for entities.
    
    Returns a list of found entities with their positions and scores.
    """
    try:
        results = analyzer.analyze_text(request.text, request.entities)
        
        entities_found = [
            Entity(
                entity_type=result.entity_type,
                text=request.text[result.start:result.end],
                score=result.score
            )
            for result in results
        ]
        
        return AnalysisResponse(
            text=request.text,
            entities_found=entities_found
        )
    
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