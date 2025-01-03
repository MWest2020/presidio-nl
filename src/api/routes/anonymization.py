"""API routes for text anonymization."""
import os
import logging
import tempfile
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Query, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from PyPDF2 import PdfReader
import time

from ...core.document import DocumentProcessor
from ...core.ocr import OCRProcessor
from ..models import AnonymizeResponse, ProcessResponse

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define storage directory for processed files (container storage)
STORAGE_DIR = Path(os.environ.get('STORAGE_DIR', '/app/storage'))
if not STORAGE_DIR.exists():
    logger.info(f"Creating container storage directory: {STORAGE_DIR}")
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

logger.info(f"Container storage directory: {STORAGE_DIR}")

# Define cleanup time (in seconds)
MAX_STORAGE_TIME = int(os.environ.get('MAX_STORAGE_TIME', 3600))  # Default 1 hour

# Cleanup old files
def cleanup_old_files():
    """Remove files older than MAX_STORAGE_TIME from container storage."""
    current_time = time.time()
    try:
        for file_path in STORAGE_DIR.glob('*.pdf'):
            if current_time - file_path.stat().st_mtime > MAX_STORAGE_TIME:
                logger.info(f"Removing old file from container: {file_path}")
                file_path.unlink()
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

# Run cleanup on startup
cleanup_old_files()

# Create two routers: one for anonymization and one for downloads
anonymize_router = APIRouter(prefix="/anonymize", tags=["anonymization"])
download_router = APIRouter(tags=["downloads"])

# Initialize processors
document_processor = DocumentProcessor()

# Initialize OCR processor with system paths if available
tesseract_cmd = os.environ.get('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
poppler_path = os.environ.get('POPPLER_PATH', r'C:\Program Files\poppler-24.02.0\Library\bin')

try:
    ocr_processor = OCRProcessor(
        tesseract_cmd=tesseract_cmd,
        poppler_path=poppler_path
    )
except Exception as e:
    logger.warning(f"Could not initialize OCR: {str(e)}")
    ocr_processor = None

class AnonymizeRequest(BaseModel):
    """Request model for text anonymization."""
    text: str
    entities: Optional[List[str]] = None

@anonymize_router.post("/text", response_model=AnonymizeResponse)
async def anonymize_text(
    request: AnonymizeRequest,
    use_ocr: bool = Query(False, description="Of OCR gebruikt moet worden (alleen relevant voor PDF bestanden)")
) -> AnonymizeResponse:
    """
    Anonimiseer tekst.
    
    Args:
        request: AnonymizeRequest met text en optionele entities
        use_ocr: Of OCR gebruikt moet worden (alleen relevant voor PDF bestanden)
        
    Returns:
        Geanonimiseerde tekst en statistieken
    """
    # Analyze text
    results = document_processor.analyzer.analyze_text(request.text, request.entities)
    
    # Anonymize text
    anonymized = document_processor.anonymizer.anonymize_text(request.text, results)
    
    # Return response
    return AnonymizeResponse(
        original_text=request.text,
        anonymized_text=anonymized,
        entities_found=[{
            "entity_type": r.entity_type,
            "text": request.text[r.start:r.end],
            "score": r.score
        } for r in results]
    )

@anonymize_router.post("/pdf", response_model=ProcessResponse)
async def anonymize_pdf(
    file: UploadFile = File(...),
    entities: Optional[List[str]] = Query(None, description="Optionele lijst van entiteiten om te detecteren"),
    use_ocr: bool = Query(False, description="Of OCR gebruikt moet worden voor gescande PDFs")
) -> ProcessResponse:
    """
    Anonimiseer een PDF bestand via de API.
    
    Args:
        file: PDF bestand
        entities: Optionele lijst van entiteiten om te detecteren
        use_ocr: Of OCR gebruikt moet worden voor gescande PDFs
        
    Returns:
        ProcessResponse met statistieken en download link
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Alleen PDF bestanden worden ondersteund")

    logger.debug(f"Starting PDF anonymization for file: {file.filename}")
    
    # Create temporary file for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_in:
        content = await file.read()
        temp_in.write(content)
        temp_path = Path(temp_in.name)
        
        try:
            # Configure OCR if requested
            if use_ocr and ocr_processor:
                logger.debug("OCR requested and available, configuring processor")
                document_processor.ocr_processor = ocr_processor
            elif use_ocr:
                logger.warning("OCR requested but not available")
            
            # Process PDF
            timestamp = int(time.time())
            output_filename = f"{timestamp}_{Path(file.filename).stem}_geanonimiseerd.pdf"
            output_path = STORAGE_DIR / output_filename
            
            stats = document_processor.process_pdf(
                input_path=temp_path,
                output_path=output_path,
                entities=entities
            )
            
            logger.debug(f"PDF processing completed with stats: {stats}")
            
            # Verify file exists before returning response
            if not output_path.exists():
                logger.error(f"Output file not found after processing: {output_path}")
                raise HTTPException(
                    status_code=500,
                    detail="PDF verwerking mislukt: output bestand niet gevonden"
                )
            
            # Add download link to stats with the exact filename including timestamp
            stats["download_link"] = f"/download/{output_filename}"  # Use the same filename with timestamp
            
            return ProcessResponse(**stats)
            
        except Exception as e:
            logger.error(f"Error during PDF processing: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF: {str(e)}"
            )
        finally:
            # Cleanup temporary file
            if temp_path.exists():
                os.unlink(temp_path)

@download_router.get("/download/{filename}")
async def download_file(filename: str):
    """Download a processed PDF file from container storage."""
    file_path = STORAGE_DIR / filename
    
    logger.debug(f"Download requested for file: {filename}")
    logger.debug(f"Looking for file in container storage: {file_path}")
    
    if not file_path.exists():
        logger.error(f"File not found in container storage: {file_path}")
        raise HTTPException(
            status_code=404, 
            detail=f"Bestand niet gevonden. Mogelijk is de verwerking nog bezig of is het bestand verlopen (na {MAX_STORAGE_TIME} seconden)."
        )
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/pdf"
    )

# Export both routers
router = anonymize_router
download_router = download_router 