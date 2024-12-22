from typing import Dict, List, Optional
from presidio_analyzer import RecognizerResult
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
            analyzer_results: List of RecognizerResult objects from the analyzer
            operators: Optional custom operators for anonymization
            
        Returns:
            Anonymized text
            
        Raises:
            ValueError: If input is invalid
        """
        # Input validation
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        if not isinstance(analyzer_results, list):
            raise ValueError("Analyzer results must be a list")
        
        # Operator validation
        if operators is not None:
            if not isinstance(operators, dict):
                raise ValueError("Operators must be a dictionary")
            if not operators:
                raise ValueError("Operators dictionary cannot be empty")
            if not all(isinstance(v, OperatorConfig) for v in operators.values()):
                raise ValueError("All operators must be OperatorConfig objects")
            
            # Check if all required operators are present
            entity_types = {r.entity_type for r in analyzer_results}
            if not all(et in operators for et in entity_types):
                raise ValueError("Missing operators for some entity types")
        
        # Use default operators if none provided
        operators = operators or self.default_operators
        
        # Handle overlapping entities by sorting by score and length
        analyzer_results = sorted(
            analyzer_results,
            key=lambda x: (x.score or 0.0, len(x.entity_type)),
            reverse=True
        )
        
        # Filter out overlapping entities
        filtered_results = []
        used_ranges = []
        
        for result in analyzer_results:
            # Check if this range overlaps with any used range
            overlaps = False
            for start, end in used_ranges:
                if (result.start < end and result.end > start):
                    overlaps = True
                    break
            
            if not overlaps:
                filtered_results.append(result)
                used_ranges.append((result.start, result.end))
        
        # Anonymize text
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=filtered_results,
            operators=operators
        )
        
        return anonymized_result.text