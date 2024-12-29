"""CLI commands for text analysis and anonymization."""
import sys
import json
from typing import List, Optional
from pathlib import Path

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
                    print(f"Positie: {r.start}-{r.end}")
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
                            "start": r.start,
                            "end": r.end,
                            "score": r.score
                        }
                        for r in results
                    ]
                }
                print(json.dumps(output, indent=2))
            else:
                print("\nOriginele tekst:")
                print(text)
                print("\nGeanonimiseerde tekst:")
                print(anonymized)
                
                if results:
                    print("\nGevonden en vervangen entiteiten:")
                    print("-" * 40)
                    for r in results:
                        print(f"Type: {r.entity_type}")
                        print(f"Text: {text[r.start:r.end]}")
                        print(f"Positie: {r.start}-{r.end}")
                        print(f"Score: {r.score:.2f}")
                        print("-" * 40)
        
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    def process_file(
        self,
        input_file: Path,
        output_file: Optional[Path] = None,
        command: str = "anonymize",
        entities: Optional[List[str]] = None,
        output_format: str = "text"
    ) -> None:
        """
        Process a file or directory.
        
        Args:
            input_file: Input file or directory path
            output_file: Optional output file path
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
                
                # Process all files in directory
                for file_path in input_file.glob("*"):
                    if file_path.is_file():
                        # Skip files in 'verwerkt' directory
                        if "verwerkt" in str(file_path):
                            continue
                            
                        # Create output path in verwerkt directory
                        file_output = output_dir / f"{file_path.stem}_anon{file_path.suffix}"
                        
                        print(f"\nVerwerken van: {file_path}")
                        try:
                            self.process_file(
                                input_file=file_path,
                                output_file=file_output,
                                command=command,
                                entities=entities,
                                output_format=output_format
                            )
                        except Exception as e:
                            print(f"Error bij verwerken {file_path}: {str(e)}")
                            continue
                return
            
            # Check if it's a PDF
            if input_file.suffix.lower() == '.pdf':
                # For PDFs, always create output in verwerkt directory
                if output_file is None:
                    output_dir = input_file.parent / "verwerkt"
                    output_dir.mkdir(exist_ok=True)
                    output_file = output_dir / f"{input_file.stem}_anon.pdf"
                
                # Process PDF
                stats = self.document_processor.process_pdf(
                    input_path=input_file,
                    output_path=output_file,
                    entities=entities,
                    keep_layout=True  # Always try to keep layout for better results
                )
                
                if output_format == "json":
                    print(json.dumps(stats, indent=2))
                else:
                    print("\nPDF Verwerking voltooid!")
                    print(f"Input bestand: {stats['input_file']}")
                    print(f"Output bestand: {stats['output_file']}")
                    print(f"\nTotaal aantal gevonden entiteiten: {stats['total_entities']}")
                    
                    if stats['entities_by_type']:
                        print("\nGevonden entiteiten per type:")
                        for entity_type, entities in stats['entities_by_type'].items():
                            print(f"\n{entity_type}:")
                            for entity in entities:
                                print(f"- {entity['text']} (score: {entity['score']:.2f})")
                
                return

            # Regular text file processing
            text = input_file.read_text(encoding='utf-8')  # Added explicit encoding
            
            # Process based on command
            if command == "analyze":
                results = self.analyzer.analyze_text(text, entities)
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
            else:  # anonymize
                results = self.analyzer.analyze_text(text, entities)
                anonymized = self.anonymizer.anonymize_text(text, results)
                output = {
                    "original_text": text,
                    "anonymized_text": anonymized,
                    "entities_found": [
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
            
            # Write output
            if output_file:
                if output_format == "json":
                    output_file.write_text(json.dumps(output, indent=2), encoding='utf-8')
                else:
                    if command == "analyze":
                        output_text = "\n".join(
                            f"{r['entity_type']}: {r['text']} ({r['score']:.2f})"
                            for r in output["results"]
                        )
                    else:
                        output_text = output["anonymized_text"]
                    output_file.write_text(output_text, encoding='utf-8')
            else:
                if output_format == "json":
                    print(json.dumps(output, indent=2))
                else:
                    if command == "analyze":
                        for r in output["results"]:
                            print(f"{r['entity_type']}: {r['text']} ({r['score']:.2f})")
                    else:
                        print(output["anonymized_text"])
        
        except Exception as e:
            print(f"Error bij verwerken bestand: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    def process_pdf(
        self,
        input_file: Path,
        output_file: Optional[Path] = None,
        entities: Optional[List[str]] = None,
        keep_layout: bool = True,
        output_format: str = "text"
    ) -> None:
        """
        Process a PDF file.
        
        Args:
            input_file: Input PDF file
            output_file: Optional output PDF file
            entities: Optional list of entities to detect
            keep_layout: Whether to try to maintain PDF layout
            output_format: Output format for statistics (text/json)
        """
        try:
            stats = self.document_processor.process_pdf(
                input_path=input_file,
                output_path=output_file,
                entities=entities,
                keep_layout=keep_layout
            )
            
            if output_format == "json":
                print(json.dumps(stats, indent=2))
            else:
                print("\nVerwerking voltooid!")
                print(f"Input bestand: {stats['input_file']}")
                print(f"Output bestand: {stats['output_file']}")
                print(f"\nTotaal aantal gevonden entiteiten: {stats['total_entities']}")
                
                if stats['entities_by_type']:
                    print("\nGevonden entiteiten per type:")
                    for entity_type, entities in stats['entities_by_type'].items():
                        print(f"\n{entity_type}:")
                        for entity in entities:
                            print(f"- {entity['text']} (score: {entity['score']:.2f})")
        
        except Exception as e:
            print(f"Error bij verwerken PDF: {str(e)}", file=sys.stderr)
            sys.exit(1) 