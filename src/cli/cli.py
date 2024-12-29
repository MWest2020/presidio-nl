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
        help="Analyseer tekst voor entiteiten"
    )
    analyze_parser.add_argument(
        "text",
        help="Tekst om te analyseren (of pad naar bestand als --input-file is gebruikt)"
    )
    analyze_parser.add_argument(
        "--input-file",
        action="store_true",
        help="Behandel TEXT als een bestandspad"
    )
    analyze_parser.add_argument(
        "--output-file",
        type=Path,
        help="Schrijf output naar bestand"
    )
    
    # Anonymize command
    anonymize_parser = subparsers.add_parser(
        "anonymize",
        help="Anonimiseer tekst"
    )
    anonymize_parser.add_argument(
        "text",
        help="Tekst om te anonimiseren (of pad naar bestand als --input-file is gebruikt)"
    )
    anonymize_parser.add_argument(
        "--input-file",
        action="store_true",
        help="Behandel TEXT als een bestandspad"
    )
    anonymize_parser.add_argument(
        "--output-file",
        type=Path,
        help="Schrijf output naar bestand"
    )
    
    # PDF command
    pdf_parser = subparsers.add_parser(
        "pdf",
        help="Verwerk een PDF bestand"
    )
    pdf_parser.add_argument(
        "input_file",
        type=Path,
        help="Input PDF bestand"
    )
    pdf_parser.add_argument(
        "--output-file",
        type=Path,
        help="Output PDF bestand (standaard: input_anon.pdf)"
    )
    pdf_parser.add_argument(
        "--no-layout",
        action="store_true",
        help="Behoud geen PDF layout (sneller maar minder mooi)"
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
        if args.command == "pdf":
            handler.process_pdf(
                input_file=args.input_file,
                output_file=args.output_file,
                entities=entities,
                keep_layout=not args.no_layout,
                output_format=args.format
            )
        elif args.input_file:
            # Process text file
            input_file = Path(args.text)
            if not input_file.exists():
                raise FileNotFoundError(f"Bestand niet gevonden: {args.text}")
            
            handler.process_file(
                input_file=input_file,
                output_file=args.output_file,
                command=args.command,
                entities=entities,
                output_format=args.format
            )
        else:
            # Process text directly
            if args.command == "analyze":
                handler.analyze(
                    text=args.text,
                    entities=entities,
                    output_format=args.format
                )
            else:  # anonymize
                handler.anonymize(
                    text=args.text,
                    entities=entities,
                    output_format=args.format
                )
    
    except Exception as e:
        parser.error(str(e))

if __name__ == "__main__":
    main() 