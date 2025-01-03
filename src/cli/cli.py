"""Command line interface for text analysis and anonymization."""
import argparse
from pathlib import Path
from typing import List, Optional

from .commands import CommandHandler

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="Nederlandse tekst analyse en anonimisatie tool"
    )
    
    # Algemene argumenten
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output formaat (standaard: text)"
    )
    
    parser.add_argument(
        "--entities",
        nargs="+",
        help="Specifieke entiteiten om te detecteren (bijv. PERSON LOCATION)"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyseer tekst of bestand(en)"
    )
    analyze_parser.add_argument(
        "input",
        help="Tekst om te analyseren, of pad naar bestand/directory"
    )
    analyze_parser.add_argument(
        "--ocr",
        action="store_true",
        help="Gebruik OCR voor gescande PDFs"
    )
    
    # Anonymize command
    anonymize_parser = subparsers.add_parser(
        "anonymize",
        help="Anonimiseer tekst of bestand(en)"
    )
    anonymize_parser.add_argument(
        "input",
        help="Tekst om te anonimiseren, of pad naar bestand/directory"
    )
    anonymize_parser.add_argument(
        "--ocr",
        action="store_true",
        help="Gebruik OCR voor gescande PDFs"
    )
    
    return parser

def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    handler = CommandHandler()
    
    # Convert entities to list if provided
    entities: Optional[List[str]] = None
    if args.entities:
        entities = [e.upper() for e in args.entities]
    
    try:
        # Check if input is a path
        input_path = Path(args.input)
        if input_path.exists():
            handler.process_file(
                input_file=input_path,
                command=args.command,
                entities=entities,
                output_format=args.format,
                use_ocr=args.ocr
            )
        else:
            # Process text directly
            if args.command == "analyze":
                handler.analyze(
                    text=args.input,
                    entities=entities,
                    output_format=args.format
                )
            else:  # anonymize
                handler.anonymize(
                    text=args.input,
                    entities=entities,
                    output_format=args.format
                )
    
    except Exception as e:
        parser.error(str(e))

if __name__ == "__main__":
    main() 