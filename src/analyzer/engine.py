from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from typing import List, Optional

class DutchTextAnalyzer:
    """Main analyzer class for Dutch text analysis."""

    def __init__(self):
        """Initialize the analyzer with Dutch language support."""
        # Configuratie voor SpaCy NLP Engine
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {"lang_code": "nl", "model_name": "nl_core_news_md"}
            ],
        }
        
        # Create NLP engine
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()
        
        # Initialize analyzer
        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine,
            supported_languages=["nl"]
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
        entities: Optional[List[str]] = None
    ) -> List:
        """
        Analyze text for entities.
        
        Args:
            text: The text to analyze
            entities: Optional list of entities to detect. If None, uses default entities.
            
        Returns:
            List of detected entities
        """
        if entities is None:
            entities = self.default_entities
            
        return self.analyzer.analyze(
            text=text,
            entities=entities,
            language="nl"
        )