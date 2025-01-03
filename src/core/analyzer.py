"""Main analyzer module."""
from typing import List, Optional

from presidio_analyzer import (
    AnalyzerEngine,
    RecognizerRegistry
)
from presidio_analyzer.nlp_engine import NlpEngineProvider

from .recognizers.robbert import RobBERTRecognizer

class DutchTextAnalyzer:
    """Main analyzer class for Dutch text analysis."""

    def __init__(self):
        """Initialize the analyzer with Dutch language support."""
        # Configure SpaCy NLP Engine
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {"lang_code": "nl", "model_name": "nl_core_news_md"}
            ],
        }
        
        # Create NLP engine
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()

        # Create registry and initialize analyzer
        registry = RecognizerRegistry()
        registry.supported_languages = ["nl"]
        
        # Add RobBERT recognizer for enhanced NER
        robbert_recognizer = RobBERTRecognizer()
        robbert_recognizer.load()  # Explicitly load the model
        registry.add_recognizer(robbert_recognizer)

        # Initialize analyzer with Dutch support
        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine,
            supported_languages=["nl"],
            registry=registry
        )

        # Minimal set of false positives
        self.false_positives = {
            "Met vriendelijke groet"
        }

    def analyze_text(self, text: str, entities: Optional[List[str]] = None) -> List:
        """
        Analyze text for entities using SpaCy and RoBERTa.
        
        Args:
            text: Text to analyze
            entities: Optional list of entities to detect
            
        Returns:
            List of detected entities
        """
        if entities is None:
            entities = [
                "PERSON",
                "LOCATION",
                "PHONE_NUMBER",
                "EMAIL",
                "ORGANIZATION",
                "IBAN",
                "ADDRESS"
            ]
        
        # Analyze text with Presidio (using SpaCy and RoBERTa)
        results = self.analyzer.analyze(
            text=text,
            entities=entities,
            language="nl"
        )
        
        # Filter out false positives and fix entity types
        filtered_results = []
        used_ranges = []
        
        # Sort by score and length
        results.sort(key=lambda x: (-x.score, -(x.end - x.start)))

        for result in results:
            text_span = text[result.start:result.end]
            
            # Skip false positives
            if text_span in self.false_positives:
                continue
                
            # Fix entity types
            if result.entity_type == "IBAN_CODE":
                result.entity_type = "IBAN"
            elif result.entity_type == "ORG":
                result.entity_type = "ORGANIZATION"
                
            # Check for overlapping ranges
            overlaps = False
            for start, end in used_ranges:
                if result.start < end and result.end > start:
                    overlaps = True
                    break
                    
            if overlaps:
                continue
            
            filtered_results.append(result)
            used_ranges.append((result.start, result.end))
        
        return filtered_results 