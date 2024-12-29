"""Core anonymizer functionality."""
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
            "PERSON": OperatorConfig("replace", {"new_value": "[PERSOON]"}),
            "LOCATION": OperatorConfig("replace", {"new_value": "[LOCATIE]"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[TELEFOONNUMMER]"}),
            "EMAIL": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
            "ORGANIZATION": OperatorConfig("replace", {"new_value": "[ORGANISATIE]"}),
            "IBAN": OperatorConfig("replace", {"new_value": "[IBAN]"}),
            "ADDRESS": OperatorConfig("replace", {"new_value": "[ADRES]"})
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
        """
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
            # Skip if confidence score is too low
            if result.score < 0.4:
                continue
                
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
        return anonymized_result.text 