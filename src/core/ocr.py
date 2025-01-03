"""OCR module for processing scanned PDFs."""
import os
from typing import Optional
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

class OCRProcessor:
    """Handles OCR processing for scanned PDFs."""
    
    def __init__(self, tesseract_cmd: Optional[str] = None, poppler_path: Optional[str] = None):
        """Initialize OCR processor with optional paths to Tesseract and Poppler."""
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            
        self.poppler_path = poppler_path
        
    def process_pdf(self, pdf_path: str) -> str:
        """
        Process a PDF file using OCR.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text from the PDF
        """
        try:
            # Convert PDF to images
            images = convert_from_path(
                pdf_path,
                poppler_path=self.poppler_path
            )
            
            # Extract text from each image
            text_parts = []
            for image in images:
                # Perform OCR with Dutch language support
                text = pytesseract.image_to_string(
                    image,
                    lang='nld',
                    config='--psm 1'  # Automatic page segmentation with OSD
                )
                text_parts.append(text)
            
            return '\n\n'.join(text_parts)
            
        except Exception as e:
            raise Exception(f"Error processing PDF with OCR: {str(e)}")
            
    def is_scanned_pdf(self, pdf_path: str) -> bool:
        """
        Check if a PDF appears to be scanned (i.e., contains no extractable text).
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if the PDF appears to be scanned, False otherwise
        """
        try:
            # Convert first page to image
            images = convert_from_path(
                pdf_path,
                poppler_path=self.poppler_path,
                first_page=1,
                last_page=1
            )
            
            if not images:
                return False
                
            # Try to extract text from first page
            text = pytesseract.image_to_string(
                images[0],
                lang='nld',
                config='--psm 1'
            )
            
            # If we get text from OCR but not from normal extraction,
            # it's likely a scanned document
            return bool(text.strip())
            
        except Exception:
            return False 

    def process_image(self, image: Image) -> str:
        """
        Process a single image using OCR.
        
        Args:
            image: PIL Image object to process
            
        Returns:
            Extracted text from the image
        """
        try:
            # Perform OCR with Dutch language support
            text = pytesseract.image_to_string(
                image,
                lang='nld',
                config='--psm 1'  # Automatic page segmentation with OSD
            )
            return text
            
        except Exception as e:
            raise Exception(f"Error processing image with OCR: {str(e)}") 