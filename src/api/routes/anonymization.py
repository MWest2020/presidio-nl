"""Routes for text anonymization."""
from fastapi import APIRouter, HTTPException

from ..models import TextRequest, AnonymizationResponse
from ...core.analyzer import DutchTextAnalyzer
from ...core.anonymizer import DutchTextAnonymizer

router = APIRouter()
analyzer = DutchTextAnalyzer()
anonymizer = DutchTextAnonymizer()

@router.post("/anonymize", response_model=AnonymizationResponse)
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
            {
                "entity_type": result.entity_type,
                "text": request.text[result.start:result.end],
                "start": result.start,
                "end": result.end,
                "score": result.score
            }
            for result in results
        ]
        
        return {
            "original_text": request.text,
            "anonymized_text": anonymized,
            "entities_found": analysis_results
        }
    
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