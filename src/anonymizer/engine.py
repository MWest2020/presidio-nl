"""Dutch Text Anonymizer using Presidio."""

from typing import List, Dict, Optional
from presidio_analyzer.recognizer_result import RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

class DutchTextAnonymizer:
    """Anonymizer for Dutch text using Presidio."""
    
    def __init__(self):
        """Initialize the anonymizer with Dutch language support."""
        self.anonymizer = AnonymizerEngine()
        
        # Default operators for each entity type
        self.default_operators = {
            "PERSON": OperatorConfig("replace", {"new_value": "[NAAM]"}),
            "LOCATION": OperatorConfig("replace", {"new_value": "[LOCATIE]"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[TELEFOONNUMMER]"}),
            "IBAN_CODE": OperatorConfig("replace", {"new_value": "[REKENINGNUMMER]"}),
            "EMAIL": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
            "ORGANIZATION": OperatorConfig("replace", {"new_value": "[ORGANISATIE]"})
        }
    
    def anonymize_text(
        self,
        text: str,
        analyzer_results: List[RecognizerResult],
        operators: Optional[Dict[str, OperatorConfig]] = None
    ) -> str:
        """
        Anonymize text based on analyzer results.
        
        Args:
            text: Text to anonymize
            analyzer_results: List of RecognizerResult objects from analyzer
            operators: Dictionary of entity types to OperatorConfig objects
            
        Returns:
            Anonymized text
        """
        if not text:
            raise ValueError("Text cannot be empty")
            
        if analyzer_results is None:
            raise ValueError("Analyzer results cannot be None")
            
        if operators is None:
            operators = self.default_operators
        else:
            # Validate operators
            if not operators:
                raise ValueError("Operators dictionary cannot be empty")
                
            # Check if all required operators are present
            missing_operators = set(
                result.entity_type for result in analyzer_results
            ) - set(operators.keys())
            if missing_operators:
                raise ValueError("Missing operators for some entity types")
                
            # Check operator types
            if not all(isinstance(op, OperatorConfig) for op in operators.values()):
                raise ValueError("All operators must be OperatorConfig objects")
        
        anonymized = self.anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results,
            operators=operators
        )
        
        return anonymized.text 