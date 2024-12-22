import argparse
import os
from typing import Optional
from pathlib import Path

from ..analyzer.engine import DutchTextAnalyzer
from ..anonymizer.engine import DutchTextAnonymizer

class CLI:
    """Command Line Interface for Dutch text analysis and anonymization."""
    
    def __init__(self):
        """Initialize CLI with analyzer and anonymizer."""
        self.analyzer = DutchTextAnalyzer()
        self.anonymizer = DutchTextAnonymizer()
    
    def analyze_text(self, text: str) -> None:
        """Analyze text and print results."""
        print("\nAnalyseresultaten:")
        results = self.analyzer.analyze_text(text)
        for result in results:
            print(f"Entiteit: {result.entity_type}, "
                  f"Tekst: '{text[result.start:result.end]}', "
                  f"Score: {result.score:.2f}")
    
    def anonymize_text(self, text: str, output_path: Optional[Path] = None) -> None:
        """Analyze and anonymize text, optionally save to file."""
        # Analyze
        print("\nAnalyseresultaten:")
        results = self.analyzer.analyze_text(text)
        for result in results:
            print(f"Entiteit: {result.entity_type}, "
                  f"Tekst: '{text[result.start:result.end]}', "
                  f"Score: {result.score:.2f}")
        
        # Anonymize
        print("\nGeanonimiseerde tekst:")
        anonymized_text = self.anonymizer.anonymize_text(text, results)
        print(anonymized_text)
        
        # Save if output path is provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(anonymized_text, encoding='utf-8')
    
    def process_file(self, filepath: Path, command: str) -> None:
        """Process a single file."""
        text = filepath.read_text(encoding='utf-8')
        
        if command == "analyze":
            self.analyze_text(text)
        elif command == "anonymize":
            output_filename = f"{filepath.stem}_geanonimiseerd{filepath.suffix}"
            output_path = Path("verwerkt") / output_filename
            self.anonymize_text(text, output_path=output_path)
    
    def process_directory(self, directory: Path, command: str) -> None:
        """Process all .txt files in a directory."""
        txt_files = list(directory.glob("*.txt"))
        if not txt_files:
            print(f"Geen .txt-bestanden gevonden in {directory}")
            return
        
        for txt_file in txt_files:
            print(f"\nVerwerken van bestand: {txt_file}")
            self.process_file(txt_file, command)
    
    def process_text(self, input_text: str, command: str) -> None:
        """Process direct text input."""
        if command == "analyze":
            self.analyze_text(input_text)
        elif command == "anonymize":
            self.anonymize_text(input_text)
    
    def main(self) -> None:
        """Main entry point for the CLI."""
        parser = argparse.ArgumentParser(
            description="CLI-tool voor analyse en anonimisatie van Nederlandse tekst."
        )
        
        subparsers = parser.add_subparsers(
            dest="command",
            help="Beschikbare commando's"
        )
        
        # Analyze command
        analyze_parser = subparsers.add_parser(
            "analyze",
            help="Analyseer de tekst"
        )
        analyze_parser.add_argument(
            "path",
            type=str,
            help="Pad naar een bestand of directory, of directe tekst"
        )
        
        # Anonymize command
        anonymize_parser = subparsers.add_parser(
            "anonymize",
            help="Analyseer en anonimiseer de tekst"
        )
        anonymize_parser.add_argument(
            "path",
            type=str,
            help="Pad naar een bestand of directory, of directe tekst"
        )
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        path = Path(args.path)
        
        try:
            if path.is_file():
                self.process_file(path, args.command)
            elif path.is_dir():
                self.process_directory(path, args.command)
            else:
                # Not a file or directory? Treat as direct text input
                self.process_text(args.path, args.command)
        except Exception as e:
            print(f"Error: {str(e)}")
            return 1
        
        return 0

def run():
    """Entry point for the package."""
    cli = CLI()
    return cli.main() 