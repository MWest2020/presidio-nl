"""Dutch Text Analyzer using spaCy and Presidio."""

import spacy
from typing import List, Optional, Dict, Any
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_analyzer.nlp_engine import NlpEngine
from presidio_analyzer.recognizer_registry import RecognizerRegistry

from .recognizers.robbert import RobBERTRecognizer
from .recognizers.patterns import (
    DutchPhoneNumberRecognizer,
    DutchIBANRecognizer,
    DutchEmailRecognizer
)

class DutchTextAnalyzer:
    """Analyzer for Dutch text using spaCy and custom recognizers."""
    
    def __init__(self):
        """Initialize the analyzer with Dutch language support."""
        # Load Dutch language model
        self.nlp = spacy.load("nl_core_news_md")
        
        # Setup NLP engine with spaCy
        self.nlp_engine = NlpEngine(self.nlp)
        
        # Create registry with custom recognizers
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()
        
        # Add custom recognizers
        registry.add_recognizer(DutchPhoneNumberRecognizer())
        registry.add_recognizer(DutchIBANRecognizer())
        registry.add_recognizer(DutchEmailRecognizer())
        registry.add_recognizer(RobBERTRecognizer())
        
        # Initialize analyzer
        self.analyzer = AnalyzerEngine(
            nlp_engine=self.nlp_engine,
            registry=registry
        )
        
        # Default entities to detect
        self.default_entities = [
            "PERSON",
            "LOCATION",
            "PHONE_NUMBER",
            "IBAN_CODE"
        ]
    
    def analyze_text(
        self,
        text: str,
        entities: Optional[List[str]] = None,
        language: str = "nl"
    ) -> List[RecognizerResult]:
        """
        Analyze text for entities.
        
        Args:
            text: Text to analyze
            entities: List of entities to detect (default: self.default_entities)
            language: Language of text (default: "nl")
            
        Returns:
            List of RecognizerResult objects
        """
        if not text:
            raise ValueError("Text cannot be empty")
            
        if entities is None:
            entities = self.default_entities
            
        results = self.analyzer.analyze(
            text=text,
            language=language,
            entities=entities
        )
        
        return results 