import pytest
from presidio_analyzer.recognizer_result import RecognizerResult
from src.anonymizer.engine import DutchTextAnonymizer

@pytest.fixture
def anonymizer():
    return DutchTextAnonymizer()

@pytest.fixture
def mock_analysis_results():
    """Create mock analysis results."""
    return [
        RecognizerResult(
            entity_type="PERSON",
            start=0,
            end=12,
            score=0.85
        ),
        RecognizerResult(
            entity_type="LOCATION",
            start=23,
            end=32,
            score=0.9
        )
    ]

def test_anonymizer_initialization(anonymizer):
    """Test if anonymizer initializes correctly."""
    assert anonymizer is not None
    assert all(key in anonymizer.default_operators for key in [
        "PERSON",
        "LOCATION",
        "PHONE_NUMBER",
        "IBAN_CODE"
    ])

def test_anonymize_text_with_person_and_location(anonymizer, mock_analysis_results):
    """Test if anonymizer replaces person and location correctly."""
    text = "Jan de Vries woont in Amsterdam."
    anonymized = anonymizer.anonymize_text(text, mock_analysis_results)
    
    assert "[NAAM]" in anonymized
    assert "[LOCATIE]" in anonymized
    assert "Jan de Vries" not in anonymized
    assert "Amsterdam" not in anonymized

def test_anonymize_text_with_phone_number():
    """Test if anonymizer replaces phone number correctly."""
    anonymizer = DutchTextAnonymizer()
    text = "Bel mij op 06-12345678"
    results = [
        RecognizerResult(
            entity_type="PHONE_NUMBER",
            start=10,
            end=21,
            score=0.9
        )
    ]
    
    anonymized = anonymizer.anonymize_text(text, results)
    assert "[TELEFOONNUMMER]" in anonymized
    assert "06-12345678" not in anonymized

def test_anonymize_text_with_iban():
    """Test if anonymizer replaces IBAN correctly."""
    anonymizer = DutchTextAnonymizer()
    text = "IBAN: NL91ABNA0417164300"
    results = [
        RecognizerResult(
            entity_type="IBAN_CODE",
            start=6,
            end=24,
            score=0.9
        )
    ]
    
    anonymized = anonymizer.anonymize_text(text, results)
    assert "[REKENINGNUMMER]" in anonymized
    assert "NL91ABNA0417164300" not in anonymized

def test_anonymize_text_with_custom_operators(anonymizer, mock_analysis_results):
    """Test if anonymizer works with custom operators."""
    from presidio_anonymizer.entities import OperatorConfig
    
    custom_operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "<PERSOON>"}),
        "LOCATION": OperatorConfig("replace", {"new_value": "<PLAATS>"})
    }
    
    text = "Jan de Vries woont in Amsterdam."
    anonymized = anonymizer.anonymize_text(
        text,
        mock_analysis_results,
        operators=custom_operators
    )
    
    assert "<PERSOON>" in anonymized
    assert "<PLAATS>" in anonymized
    assert "[NAAM]" not in anonymized
    assert "[LOCATIE]" not in anonymized 