"""Command Line Interface for presidio-nl."""

import argparse
from pathlib import Path
from typing import List, Optional

from ..core.analyzer import DutchTextAnalyzer
from ..core.anonymizer import DutchTextAnonymizer

class CLI:
    """Command Line Interface for text analysis and anonymization."""
    
    def __init__(self):
        """Initialize CLI with analyzer and anonymizer."""
        self.analyzer = DutchTextAnalyzer()
        self.anonymizer = DutchTextAnonymizer()
    
    def analyze_text(self, text: str) -> List:
        """Analyze text and return results."""
        return self.analyzer.analyze_text(text)
    
    def anonymize_text(self, text: str) -> str:
        """Anonymize text and return result."""
        results = self.analyzer.analyze_text(text)
        return self.anonymizer.anonymize_text(text, results)

def run():
    """Run the CLI application."""
    cli = CLI()
    parser = argparse.ArgumentParser(description="Dutch text analysis and anonymization tool")
    
    parser.add_argument(
        "command",
        choices=["analyze", "anonymize"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "text",
        help="Text to process"
    )
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        results = cli.analyze_text(args.text)
        for result in results:
            print(f"{result.entity_type}: {args.text[result.start:result.end]}")
    else:
        anonymized = cli.anonymize_text(args.text)
        print(anonymized)

if __name__ == "__main__":
    run() 