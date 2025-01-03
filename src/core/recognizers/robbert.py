"""RobBERT NER recognizer voor Nederlandse tekst."""
from typing import List, Optional
from presidio_analyzer import EntityRecognizer, RecognizerResult
from transformers import pipeline
import spacy

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
            supported_entities = [
                "PERSON",
                "LOCATION",
                "ORGANIZATION",
                "PHONE_NUMBER",
                "EMAIL",
                "IBAN",
                "ADDRESS"
            ]

        super().__init__(
            supported_entities=supported_entities,
            supported_language=supported_language,
            name="RobBERT Recognizer",
        )

        # Disable auto-loading
        self.is_loaded = False
        self.model = None
        self.nlp = None
        
    def load(self) -> None:
        """Laad het RobBERT model en SpaCy."""
        if not self.is_loaded:
            # Laad RobBERT voor algemene NER
            self.model = pipeline(
                "ner",
                model="pdelobelle/robbert-v2-dutch-ner",
                aggregation_strategy="simple"
            )
            
            # Laad SpaCy voor aanvullende entiteiten
            self.nlp = spacy.load("nl_core_news_md")
            
            self.is_loaded = True

    def analyze(self, text: str, entities: List[str], nlp_artifacts=None) -> List[RecognizerResult]:
        """
        Analyze text using RobBERT NER and SpaCy.
        
        Args:
            text: Text om te analyseren
            entities: Lijst van entiteiten om te detecteren
            nlp_artifacts: Niet gebruikt voor RobBERT
            
        Returns:
            List[RecognizerResult]: Gevonden entiteiten
        """
        if not text:
            return []

        # Lazy loading van models
        if not self.is_loaded:
            self.load()

        results = []
        
        # RobBERT NER analyse voor namen, locaties en organisaties
        robbert_results = self.model(text)
        for ent in robbert_results:
            # Converteer RobBERT labels naar Presidio formaat
            entity_type = self._convert_robbert_label(ent["entity_group"])
            
            # Skip als we deze entiteit niet zoeken
            if entity_type and (not entities or entity_type in entities):
                result = RecognizerResult(
                    entity_type=entity_type,
                    start=ent["start"],
                    end=ent["end"],
                    score=ent["score"]
                )
                results.append(result)
        
        # SpaCy analyse voor aanvullende entiteiten
        doc = self.nlp(text)
        for ent in doc.ents:
            # Converteer SpaCy labels naar Presidio formaat
            entity_type = self._convert_spacy_label(ent.label_)
            
            # Skip als we deze entiteit niet zoeken
            if entity_type and (not entities or entity_type in entities):
                result = RecognizerResult(
                    entity_type=entity_type,
                    start=ent.start_char,
                    end=ent.end_char,
                    score=0.85  # SpaCy geeft geen scores, gebruik default
                )
                results.append(result)

        return results

    def _convert_robbert_label(self, robbert_label: str) -> Optional[str]:
        """Converteer RobBERT labels naar Presidio formaat."""
        label_mapping = {
            "PER": "PERSON",
            "LOC": "LOCATION",
            "ORG": "ORGANIZATION",
            "MISC": "ORGANIZATION"  # MISC kan vaak een organisatie zijn
        }
        return label_mapping.get(robbert_label)
        
    def _convert_spacy_label(self, spacy_label: str) -> Optional[str]:
        """Converteer SpaCy labels naar Presidio formaat."""
        label_mapping = {
            "PERSON": "PERSON",
            "LOC": "LOCATION",
            "GPE": "LOCATION",
            "ORG": "ORGANIZATION",
            "FAC": "LOCATION",
            "PRODUCT": "ORGANIZATION",
            "EVENT": None,
            "WORK_OF_ART": None,
            "LAW": None,
            "LANGUAGE": None,
            "DATE": None,
            "TIME": None,
            "PERCENT": None,
            "MONEY": None,
            "QUANTITY": None,
            "ORDINAL": None,
            "CARDINAL": None
        }
        return label_mapping.get(spacy_label) 