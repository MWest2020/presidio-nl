from typing import Dict, Optional
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

class DutchTextAnonymizer:
    """Anonymizer for Dutch text."""
    
    def __init__(self):
        """Initialize the anonymizer with default settings."""
        self.anonymizer = AnonymizerEngine()
        
        # Default operators for different entity types
        self.default_operators = {
            "PERSON": OperatorConfig("replace", {"new_value": "[NAAM]"}),
            "LOCATION": OperatorConfig("replace", {"new_value": "[LOCATIE]"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[TELEFOONNUMMER]"}),
            "IBAN_CODE": OperatorConfig("replace", {"new_value": "[REKENINGNUMMER]"})
        }
    
    def anonymize_text(
        self,
        text: str,
        analysis_results: list,
        operators: Optional[Dict[str, OperatorConfig]] = None
    ) -> str:
        """
        Anonymize text based on analysis results.
        
        Args:
            text: The text to anonymize
            analysis_results: Results from the analyzer
            operators: Optional custom operators for anonymization
            
        Returns:
            Anonymized text
        """
        if operators is None:
            operators = self.default_operators
            
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=analysis_results,
            operators=operators
        )
        
        return anonymized_result.text 