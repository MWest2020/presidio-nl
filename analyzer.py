from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

# Configuratie voor SpaCy NLP Engine
configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "nl", "model_name": "nl_core_news_md"}
    ],
}

# Creëer een NLP-engine met de configuratie
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()

# Instantieer de Presidio Analyzer en Anonymizer
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["nl"])
anonymizer = AnonymizerEngine()

def analyze_text(text):
    """Analyseer een tekst voor entiteiten."""
    results = analyzer.analyze(text=text, entities=["PERSON", "LOCATION"], language="nl")
    return results

from presidio_anonymizer.entities import OperatorConfig

def anonymize_text(text):
    """Anonimiseer een tekst op basis van geanalyseerde entiteiten."""
    # Analyseer de tekst om entiteiten te detecteren
    analysis_results = analyze_text(text)

    # Stel operators in voor anonimisatie
    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "[REDACTED]"}),
        "LOCATION": OperatorConfig("replace", {"new_value": "[REDACTED]"})
    }

    # Voer de anonymization uit
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=analysis_results,
        operators=operators
    )

    return anonymized_result.text
