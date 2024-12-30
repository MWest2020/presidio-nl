"""RobBERT NER recognizer voor Nederlandse tekst."""
from typing import List, Optional
from presidio_analyzer import EntityRecognizer, RecognizerResult
from transformers import pipeline

class RobBERTRecognizer(EntityRecognizer):
    """
    Recognizer die RobBERT gebruikt voor Nederlandse NER.
    Gebaseerd op pdelobelle/robbert-v2-dutch-ner.
    """

    def __init__(
        self,
        supported_entities: Optional[List[str]] = None,
        supported_language: str = "nl",
    ):
        """Initialize the RobBERT recognizer."""
        if supported_entities is None:
            supported_entities = ["PERSON", "LOCATION", "ORGANIZATION"]

        super().__init__(
            supported_entities=supported_entities,
            supported_language=supported_language,
            name="RobBERT Recognizer",
        )

        # Disable auto-loading
        self.is_loaded = False
        self.model = None
        
    def load(self) -> None:
        """Laad het RobBERT model."""
        if not self.is_loaded:
            self.model = pipeline(
                "ner",
                model="pdelobelle/robbert-v2-dutch-ner",
                aggregation_strategy="simple"
            )
            self.is_loaded = True

    def analyze(self, text: str, entities: List[str], nlp_artifacts=None) -> List[RecognizerResult]:
        """
        Analyze text using RobBERT NER.
        
        Args:
            text: Text om te analyseren
            entities: Lijst van entiteiten om te detecteren
            nlp_artifacts: Niet gebruikt voor RobBERT
            
        Returns:
            List[RecognizerResult]: Gevonden entiteiten
        """
        if not text:
            return []

        # Lazy loading van model
        if not self.is_loaded:
            self.load()

        # RobBERT NER analyse
        ner_results = self.model(text)
        
        results = []
        for ent in ner_results:
            # Converteer RobBERT labels naar Presidio formaat
            entity_type = self._convert_label(ent["entity_group"])
            
            # Skip als we deze entiteit niet zoeken
            if entities and entity_type not in entities:
                continue
                
            # Maak Presidio result
            result = RecognizerResult(
                entity_type=entity_type,
                start=ent["start"],
                end=ent["end"],
                score=ent["score"]
            )
            results.append(result)

        return results

    def _convert_label(self, robbert_label: str) -> str:
        """Converteer RobBERT labels naar Presidio formaat."""
        label_mapping = {
            "PER": "PERSON",
            "LOC": "LOCATION",
            "ORG": "ORGANIZATION",
            "MISC": None  # Skip misc labels
        }
        return label_mapping.get(robbert_label) 