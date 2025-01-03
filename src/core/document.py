"""Document processing module."""
import os
import logging
from pathlib import Path
from typing import List, Optional, Dict
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time
import re

from .analyzer import DutchTextAnalyzer
from .anonymizer import DutchTextAnonymizer
from .ocr import OCRProcessor

# Set up logging
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str, ocr_processor: Optional[OCRProcessor] = None) -> str:
    """
    Extract text from a PDF file, with optional OCR support for scanned documents.
    
    Args:
        pdf_path: Path to the PDF file
        ocr_processor: Optional OCRProcessor instance for handling scanned PDFs
        
    Returns:
        Extracted text from the PDF
    """
    logger.debug(f"Extracting text from PDF: {pdf_path}")
    
    # First try normal text extraction
    reader = PdfReader(pdf_path)
    text = ""
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        text += page_text
        logger.debug(f"Page {page_num + 1} extracted text: {page_text[:100]}...")
    
    logger.debug(f"Extracted {len(text.split())} words using normal extraction")
    logger.debug(f"Full extracted text: {text[:500]}...")
    
    # If no text was extracted and OCR is available, try OCR
    if not text.strip() and ocr_processor is not None:
        try:
            logger.debug("No text found, attempting OCR...")
            text = ocr_processor.process_pdf(pdf_path)
            logger.debug(f"OCR extracted {len(text.split())} words")
            logger.debug(f"OCR extracted text: {text[:500]}...")
        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            # Continue with empty text if OCR fails
            pass
    
    return text

class DocumentProcessor:
    """Process documents for anonymization."""
    
    def __init__(self):
        """Initialize the document processor."""
        self.analyzer = DutchTextAnalyzer()
        self.anonymizer = DutchTextAnonymizer()
        self.ocr_processor = None
    
    def process_pdf(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        entities: Optional[List[str]] = None,
        keep_layout: bool = True
    ) -> Dict:
        """
        Process a PDF file, analyze and anonymize its content.
        Simple version: just creates a new PDF with anonymized text.
        
        Args:
            input_path: Path to input PDF
            output_path: Optional path for output PDF
            entities: Optional list of entities to detect
            keep_layout: Ignored in this simple version
            
        Returns:
            Dict with statistics about found entities
        """
        logger.debug(f"Starting PDF processing: {input_path}")
        
        if not input_path.exists():
            raise FileNotFoundError(f"PDF niet gevonden: {input_path}")
        
        # Ensure output path is in verwerkt directory
        if output_path is None:
            verwerkt_dir = Path("verwerkt")
            verwerkt_dir.mkdir(exist_ok=True)
            output_path = verwerkt_dir / f"{input_path.stem}_geanonimiseerd.pdf"
        
        logger.debug(f"Output will be written to: {output_path}")
        
        # Extract text from PDF
        reader = PdfReader(str(input_path))
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n\n"
        
        if not text.strip():
            logger.warning("No text found in document")
            return {
                "total_entities": 0,
                "entities_by_type": {},
                "input_file": str(input_path),
                "output_file": str(output_path),
                "error": "Geen tekst gevonden"
            }
        
        # Analyze and anonymize text
        results = self.analyzer.analyze_text(text, entities)
        anonymized_text = self.anonymizer.anonymize_text(text, results) if results else text
        
        try:
            # Create a new PDF with anonymized content
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Helvetica", 11)
            
            # Write text
            y = 750  # Start near top
            for line in anonymized_text.split('\n'):
                if line.strip():
                    can.drawString(50, y, line.strip())
                    y -= 12
                    if y < 50:  # Start new page when near bottom
                        can.showPage()
                        y = 750
            
            can.save()
            packet.seek(0)
            
            # Save to output file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as output_file:
                output_file.write(packet.getvalue())
            
            # Return statistics
            stats = {
                "total_entities": len(results) if results else 0,
                "entities_by_type": {},
                "input_file": str(input_path),
                "output_file": str(output_path)
            }
            
            if results:
                for result in results:
                    entity_type = result.entity_type
                    if entity_type not in stats["entities_by_type"]:
                        stats["entities_by_type"][entity_type] = []
                    stats["entities_by_type"][entity_type].append({
                        "text": text[result.start:result.end],
                        "score": float(result.score)
                    })
            
            return stats
            
        except Exception as e:
            logger.error(f"Error creating PDF: {str(e)}", exc_info=True)
            raise Exception(f"Error creating PDF: {str(e)}")
    
    def _extract_text_segments(self, page):
        """Extract text segments and their positions from a PDF page."""
        segments = []
        content = page.get_contents()
        if content:
            for operands, operator in content.operations:
                if operator == b'Tj':
                    segments.append(operands[0])
        return segments
    
    def _replace_text_in_stream(self, stream, replacements):
        """Replace text in PDF content stream."""
        modified = stream
        for original, replacement in replacements.items():
            # Escape special characters in the original text
            escaped_original = re.escape(original.encode('utf-8'))
            # Replace the text while preserving PDF operators
            modified = re.sub(
                b'\\(' + escaped_original + b'\\)', 
                b'(' + replacement.encode('utf-8') + b')', 
                modified
            )
        return modified 