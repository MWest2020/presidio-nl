"""Routes for text anonymization."""
import os
import time
import tempfile
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import List, Optional

from ..models import TextRequest, AnonymizationResponse, PDFProcessingResponse
from ...core.analyzer import DutchTextAnalyzer
from ...core.anonymizer import DutchTextAnonymizer
from ...core.document import DocumentProcessor

router = APIRouter()
analyzer = DutchTextAnalyzer()
anonymizer = DutchTextAnonymizer()
document_processor = DocumentProcessor()

# Configuratie voor bestandsopslag
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "storage"))
MAX_STORAGE_TIME = int(os.getenv("MAX_STORAGE_TIME", "3600"))  # 1 uur in seconden

def cleanup_old_files():
    """Verwijder bestanden ouder dan MAX_STORAGE_TIME."""
    if not STORAGE_DIR.exists():
        return
        
    current_time = time.time()
    for file in STORAGE_DIR.glob("*.pdf"):
        if current_time - file.stat().st_mtime > MAX_STORAGE_TIME:
            try:
                file.unlink()
            except Exception:
                pass

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

@router.post("/anonymize/pdf", response_model=PDFProcessingResponse)
async def anonymize_pdf(
    pdf_file: UploadFile = File(...),
    entities: Optional[List[str]] = None
):
    """
    Process and anonymize a PDF file.
    
    Returns statistics about found entities and a URL to download the anonymized PDF.
    """
    if not pdf_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be a PDF"
        )
    
    try:
        # Cleanup oude bestanden
        cleanup_old_files()
        
        # Create storage directory if it doesn't exist
        STORAGE_DIR.mkdir(exist_ok=True, parents=True)
        
        # Generate unique filename
        timestamp = int(time.time())
        output_filename = f"anon_{timestamp}_{pdf_file.filename}"
        output_file = STORAGE_DIR / output_filename
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            temp_input = Path(temp_dir) / "input.pdf"
            
            with open(temp_input, "wb") as buffer:
                content = await pdf_file.read()
                buffer.write(content)
            
            # Process PDF
            stats = document_processor.process_pdf(
                input_path=temp_input,
                output_path=output_file,
                entities=entities,
                keep_layout=True
            )
            
            # Create response
            return {
                "total_entities": stats["total_entities"],
                "entities_by_type": {
                    entity_type: [
                        {
                            "text": entity["text"],
                            "score": float(entity["score"])  # Convert numpy.float32 to Python float
                        }
                        for entity in entities
                    ]
                    for entity_type, entities in stats["entities_by_type"].items()
                },
                "anonymized_pdf_url": f"/download/{output_filename}"
            }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """Download an anonymized PDF file."""
    file_path = STORAGE_DIR / filename
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    ) 