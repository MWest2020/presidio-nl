"""Document processing functionality."""
import os
from pathlib import Path
from typing import List, Optional, Dict
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter

from .analyzer import DutchTextAnalyzer
from .anonymizer import DutchTextAnonymizer

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text content as string
    """
    text_content = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"
    return text_content

class DocumentProcessor:
    """Processor for handling various document types."""
    
    def __init__(self):
        """Initialize the document processor."""
        self.analyzer = DutchTextAnalyzer()
        self.anonymizer = DutchTextAnonymizer()
    
    def process_pdf(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        entities: Optional[List[str]] = None,
        keep_layout: bool = True
    ) -> Dict:
        """
        Process a PDF file, analyze and anonymize its content.
        
        Args:
            input_path: Path to input PDF
            output_path: Optional path for output PDF. If None, uses input_path with '_anon' suffix
            entities: Optional list of entities to detect
            keep_layout: Try to maintain original PDF layout
            
        Returns:
            Dict with statistics about found entities
        """
        if not input_path.exists():
            raise FileNotFoundError(f"PDF niet gevonden: {input_path}")
        
        if output_path is None:
            # Create verwerkt directory within the input file's directory if it doesn't exist
            verwerkt_dir = input_path.parent / "verwerkt"
            verwerkt_dir.mkdir(exist_ok=True)
            output_path = verwerkt_dir / f"{input_path.stem}_anon.pdf"
        
        # Extract text from PDF
        text_content = extract_text_from_pdf(str(input_path))
        
        # Analyze text
        results = self.analyzer.analyze_text(text_content, entities)
        
        # Anonymize text
        anonymized_text = self.anonymizer.anonymize_text(text_content, results)
        
        # Create a new PDF with anonymized content
        writer = PdfWriter()
        
        # Create a new page with anonymized text
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        
        # Create a temporary PDF with anonymized text
        temp_buffer = BytesIO()
        c = canvas.Canvas(temp_buffer, pagesize=letter)
        
        # Split text into lines and write to PDF
        y = 750  # Start from top
        for line in anonymized_text.split('\n'):
            if line.strip():  # Only write non-empty lines
                c.drawString(50, y, line)
                y -= 12  # Move down for next line
                if y < 50:  # If we're at the bottom, start a new page
                    c.showPage()
                    y = 750
        
        c.save()
        
        # Add the page to the output PDF
        temp_buffer.seek(0)
        new_pdf = PdfReader(temp_buffer)
        for page in new_pdf.pages:
            writer.add_page(page)
        
        # Save the anonymized PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Return statistics
        stats = {
            "total_entities": len(results),
            "entities_by_type": {},
            "input_file": str(input_path),
            "output_file": str(output_path)
        }
        
        for result in results:
            entity_type = result.entity_type
            if entity_type not in stats["entities_by_type"]:
                stats["entities_by_type"][entity_type] = []
            stats["entities_by_type"][entity_type].append({
                "text": text_content[result.start:result.end],
                "score": result.score
            })
        
        return stats 