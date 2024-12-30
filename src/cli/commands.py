"""CLI commands for text analysis and anonymization."""
import sys
import json
import logging
import warnings
from typing import List, Optional
from pathlib import Path

# Configure logging
logging.getLogger("transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", message="Asking to truncate")

from ..core.analyzer import DutchTextAnalyzer
from ..core.anonymizer import DutchTextAnonymizer
from ..core.document import DocumentProcessor

class CommandHandler:
    """Handler for CLI commands."""
    
    def __init__(self):
        """Initialize the command handler."""
        self.analyzer = DutchTextAnalyzer()
        self.anonymizer = DutchTextAnonymizer()
        self.document_processor = DocumentProcessor()
    
    def analyze(
        self,
        text: str,
        entities: Optional[List[str]] = None,
        output_format: str = "text"
    ) -> None:
        """
        Analyze text for entities.
        
        Args:
            text: Text to analyze
            entities: Optional list of entities to detect
            output_format: Output format (text/json)
        """
        try:
            results = self.analyzer.analyze_text(text, entities)
            
            if output_format == "json":
                output = {
                    "results": [
                        {
                            "entity_type": r.entity_type,
                            "text": text[r.start:r.end],
                            "start": r.start,
                            "end": r.end,
                            "score": r.score
                        }
                        for r in results
                    ]
                }
                print(json.dumps(output, indent=2))
            else:
                if not results:
                    print("Geen entiteiten gevonden.")
                    return
                
                print("\nGevonden entiteiten:")
                print("-" * 40)
                for r in results:
                    print(f"Type: {r.entity_type}")
                    print(f"Text: {text[r.start:r.end]}")
                    print(f"Score: {r.score:.2f}")
                    print("-" * 40)
        
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    def anonymize(
        self,
        text: str,
        entities: Optional[List[str]] = None,
        output_format: str = "text"
    ) -> None:
        """
        Anonymize text.
        
        Args:
            text: Text to anonymize
            entities: Optional list of entities to anonymize
            output_format: Output format (text/json)
        """
        try:
            # First analyze
            results = self.analyzer.analyze_text(text, entities)
            
            # Then anonymize
            anonymized = self.anonymizer.anonymize_text(text, results)
            
            if output_format == "json":
                output = {
                    "original_text": text,
                    "anonymized_text": anonymized,
                    "entities_found": [
                        {
                            "entity_type": r.entity_type,
                            "text": text[r.start:r.end],
                            "score": r.score
                        }
                        for r in results
                    ]
                }
                print(json.dumps(output, indent=2))
            else:
                print("\nGeanonimiseerde tekst:")
                print(anonymized)
                
                if results:
                    print("\nGevonden en vervangen entiteiten:")
                    print("-" * 40)
                    for r in results:
                        print(f"Type: {r.entity_type}")
                        print(f"Text: {text[r.start:r.end]}")
                        print(f"Score: {r.score:.2f}")
                        print("-" * 40)
        
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    def process_file(
        self,
        input_file: Path,
        command: str = "anonymize",
        entities: Optional[List[str]] = None,
        output_format: str = "text"
    ) -> None:
        """
        Process a file or directory.
        
        Args:
            input_file: Input file or directory path
            command: Command to execute (analyze/anonymize)
            entities: Optional list of entities
            output_format: Output format (text/json)
        """
        try:
            # Check if input is a directory
            if input_file.is_dir():
                # Create verwerkt directory if it doesn't exist
                output_dir = input_file.parent / "verwerkt"
                output_dir.mkdir(exist_ok=True)
                
                print(f"\nVerwerken van directory: {input_file}")
                
                # Process all text and PDF files
                for pattern in ["*.txt", "*.pdf"]:
                    for file_path in input_file.glob(pattern):
                        # Skip files in 'verwerkt' directory
                        if "verwerkt" in str(file_path):
                            continue
                            
                        print(f"\nVerwerken van: {file_path}")
                        try:
                            self.process_file(
                                input_file=file_path,
                                command=command,
                                entities=entities,
                                output_format=output_format
                            )
                        except Exception as e:
                            print(f"Error bij verwerken {file_path}: {str(e)}")
                            continue
                return
            
            # Create output path in verwerkt directory
            output_dir = input_file.parent / "verwerkt"
            output_dir.mkdir(exist_ok=True)
            
            # Process based on file type
            if input_file.suffix.lower() == '.pdf':
                # For PDFs, use document processor
                output_file = output_dir / f"{input_file.stem}_anon.pdf"
                stats = self.document_processor.process_pdf(
                    input_path=input_file,
                    output_path=output_file,
                    entities=entities,
                    keep_layout=True
                )
                
                if output_format == "json":
                    print(json.dumps(stats, indent=2))
                else:
                    print("\nPDF Verwerking voltooid!")
                    print(f"Output bestand: {stats['output_file']}")
                    if stats['entities_by_type']:
                        print("\nGevonden entiteiten per type:")
                        for entity_type, entities in stats['entities_by_type'].items():
                            print(f"\n{entity_type}:")
                            for entity in entities:
                                print(f"- {entity['text']} (score: {entity['score']:.2f})")
            else:
                # Regular text file processing
                text = input_file.read_text(encoding='utf-8')
                
                if command == "analyze":
                    results = self.analyzer.analyze_text(text, entities)
                    if output_format == "json":
                        output = {
                            "results": [
                                {
                                    "entity_type": r.entity_type,
                                    "text": text[r.start:r.end],
                                    "score": r.score
                                }
                                for r in results
                            ]
                        }
                        print(json.dumps(output, indent=2))
                    else:
                        print("\nGevonden entiteiten:")
                        print("-" * 40)
                        for r in results:
                            print(f"Type: {r.entity_type}")
                            print(f"Text: {text[r.start:r.end]}")
                            print(f"Score: {r.score:.2f}")
                            print("-" * 40)
                else:  # anonymize
                    results = self.analyzer.analyze_text(text, entities)
                    anonymized = self.anonymizer.anonymize_text(text, results)
                    output_file = output_dir / f"{input_file.stem}_anon{input_file.suffix}"
                    output_file.write_text(anonymized, encoding='utf-8')
                    
                    print(f"\nGeanonimiseerd bestand opgeslagen als: {output_file}")
                    if results:
                        print("\nGevonden en vervangen entiteiten:")
                        print("-" * 40)
                        for r in results:
                            print(f"Type: {r.entity_type}")
                            print(f"Text: {text[r.start:r.end]}")
                            print(f"Score: {r.score:.2f}")
                            print("-" * 40)
        
        except Exception as e:
            print(f"Error bij verwerken bestand: {str(e)}", file=sys.stderr)
            sys.exit(1) 