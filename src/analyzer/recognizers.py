from typing import List
from presidio_analyzer import PatternRecognizer

class DutchRecognizers:
    """Collection of custom recognizers for Dutch text analysis."""
    
    @staticmethod
    def get_custom_recognizers() -> List[PatternRecognizer]:
        """
        Get a list of custom recognizers.
        
        Returns:
            List of PatternRecognizer instances
        """
        recognizers = []
        
        # IBAN Recognizer
        iban_pattern = r'[A-Z]{2}\d{2}[A-Z0-9]{1,30}'
        iban_recognizer = PatternRecognizer(
            supported_entity="CUSTOM_IBAN",
            patterns=[{
                "name": "iban_pattern",
                "pattern": iban_pattern,
                "score": 1.0
            }]
        )
        recognizers.append(iban_recognizer)
        
        # Add more custom recognizers here as needed
        
        return recognizers 