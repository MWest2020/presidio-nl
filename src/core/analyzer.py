"""Core analyzer functionality."""
from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.recognizer_result import RecognizerResult
from presidio_analyzer.recognizer_registry import RecognizerRegistry
from typing import List, Optional
import re

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
        registry.supported_languages = ["nl"]  # Set supported languages explicitly
        
        # Initialize analyzer with Dutch support
        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine,
            supported_languages=["nl"],
            registry=registry
        )

        # Add Dutch recognizers
        self._add_dutch_recognizers()

        # Words to ignore
        self.false_positives = {
            "Klantgesprek",
            "Hypotheekaanvraag",
            "Vervolgafspraken",
            "Contactgegevens",
            "Aanwezigen gesprek",
            "Met vriendelijke groet",
            "Hypotheekadviseur",
            "Financieel specialist",
            "Verslag Klantgesprek",
            "Tijdens het gesprek",
            "Voor vragen",
            "Met vriendelijke",
            "Het echtpaar",
            "Voor woensdag",
            "Vervolgafspraak gepland"
        }

    def _add_dutch_recognizers(self):
        """Add Dutch-specific recognizers to the analyzer."""
        # Person patterns
        self.analyzer.registry.add_recognizer(
            PatternRecognizer(
                supported_entity="PERSON",
                supported_language="nl",
                patterns=[
                    Pattern(
                        "DUTCH_FORMAL_NAME",
                        r"\b(?:de\s+heer|mevrouw|mevr\.|dhr\.|dr\.|mr\.|prof\.)\s+(?:[A-Z]\.?\s+)?(?:van\s+(?:der|den|de|het)|de|den|ter|te|ten|het|'t)?\s*[A-Z][a-zÀ-ÿ]+(?:-[A-Z][a-zÀ-ÿ]+)?\b",
                        0.85
                    ),
                    Pattern(
                        "DUTCH_FAMILY",
                        r"\b(?:familie|gezin|echtpaar)\s+(?:van\s+(?:der|den|de|het)|de|den|ter|te|ten|het|'t)?\s*[A-Z][a-zÀ-ÿ]+\b",
                        0.85
                    ),
                    Pattern(
                        "DUTCH_NAME",
                        r"\b[A-Z][a-zÀ-ÿ]+\s+(?:van\s+(?:der|den|de|het)|de|den|ter|te|ten|het|'t)?\s*[A-Z][a-zÀ-ÿ]+(?:-[A-Z][a-zÀ-ÿ]+)?\b",
                        0.85
                    )
                ],
                context=["naam", "persoon", "klant", "adviseur", "specialist", "medewerker", "collega"]
            )
        )

        # Phone number patterns
        self.analyzer.registry.add_recognizer(
            PatternRecognizer(
                supported_entity="PHONE_NUMBER",
                supported_language="nl",
                patterns=[
                    Pattern(
                        "DUTCH_MOBILE",
                        r"\b(?:\+31|0031|0)6[-\s]?(?:[1-9][\s-]?[0-9][-\s]?){4}\b",
                        0.85
                    ),
                    Pattern(
                        "DUTCH_LANDLINE",
                        r"\b(?:\+31|0031|0)(?:[1-9][0-9][-\s]?)?(?:[0-9][-\s]?){6,8}\b",
                        0.85
                    )
                ],
                context=["telefoon", "tel", "mobiel", "gsm", "nummer", "contact", "kantoor"]
            )
        )

        # Email pattern
        self.analyzer.registry.add_recognizer(
            PatternRecognizer(
                supported_entity="EMAIL",
                supported_language="nl",
                patterns=[
                    Pattern(
                        "EMAIL_PATTERN",
                        r"(?i)\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                        0.85
                    )
                ],
                context=["email", "e-mail", "mail", "contact", "@"]
            )
        )

        # IBAN pattern
        self.analyzer.registry.add_recognizer(
            PatternRecognizer(
                supported_entity="IBAN",
                supported_language="nl",
                patterns=[
                    Pattern(
                        "DUTCH_IBAN",
                        r"(?i)(?:IBAN:?\s*)?(?:NL|BE|DE)\d{2}[A-Z]{4}\d{10}",
                        0.95
                    )
                ],
                context=["iban", "rekening", "bank", "betaling", "rekeningnummer"]
            )
        )

        # Address pattern
        self.analyzer.registry.add_recognizer(
            PatternRecognizer(
                supported_entity="ADDRESS",
                supported_language="nl",
                patterns=[
                    Pattern(
                        "DUTCH_ADDRESS",
                        r"\b[A-Z][a-z]+(?:straat|laan|weg|plein|gracht|kade|singel)\s+\d+(?:[a-zA-Z])?\b",
                        0.85
                    )
                ]
            )
        )

        # Organization pattern
        self.analyzer.registry.add_recognizer(
            PatternRecognizer(
                supported_entity="ORGANIZATION",
                supported_language="nl",
                patterns=[
                    Pattern(
                        "DUTCH_ORGANIZATIONS",
                        r"\b(?:ABN\s*AMRO|Rabobank|ING|SNS|Triodos|[A-Z][A-Za-z\s]+(?:Bank|Gymnasium|School|College|Universiteit|B\.V\.|N\.V\.|Holding|Groep|Stichting))\b",
                        0.85
                    )
                ]
            )
        )

    def analyze_text(self, text: str, entities: Optional[List[str]] = None) -> List:
        """
        Analyze text for entities.
        
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

        # Analyze text with Presidio
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
                
            # Prevent IBAN being detected as LOCATION
            if result.entity_type == "LOCATION" and any(
                text_span.upper().startswith(prefix) 
                for prefix in ["NL", "BE", "DE"]
            ) and any(c.isdigit() for c in text_span):
                continue
                
            # Additional filtering for person names
            if result.entity_type == "PERSON":
                # Skip if text contains common words or patterns that indicate non-person text
                if any(word in text_span.lower() for word in [
                    "aan de", "voor de", "met de", "in de", "op de", "bij de",
                    "wordt", "kunnen", "hebben", "moeten", "zullen", "ruimte",
                    "contact", "kantoor", "tijdens", "bleek", "sprak", "momenteel"
                ]):
                    continue
                    
                # Skip if text doesn't match typical name patterns
                if not any([
                    # Full name with prefix
                    re.match(r"\b(?:de\s+heer|mevrouw|mevr\.|dhr\.|dr\.|mr\.|prof\.)\s+(?:[A-Z]\.?\s+)?(?:van\s+(?:der|den|de|het)|de|den|ter|te|ten|het|'t)?\s*[A-Z][a-zÀ-ÿ]+\b", text_span),
                    # Family reference
                    re.match(r"\b(?:familie|gezin|echtpaar)\s+(?:van\s+(?:der|den|de|het)|de|den|ter|te|ten|het|'t)?\s*[A-Z][a-zÀ-ÿ]+\b", text_span),
                    # Full name
                    re.match(r"\b[A-Z][a-zÀ-ÿ]+\s+(?:van\s+(?:der|den|de|het)|de|den|ter|te|ten|het|'t)?\s*[A-Z][a-zÀ-ÿ]+\b", text_span)
                ]):
                    continue
                
            filtered_results.append(result)
            used_ranges.append((result.start, result.end))

        return filtered_results 