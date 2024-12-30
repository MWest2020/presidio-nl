import pytest
from presidio_analyzer.recognizer_result import RecognizerResult
from src.core.anonymizer import DutchTextAnonymizer

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
        "IBAN"
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
            entity_type="IBAN",
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

def test_anonymize_text_with_overlapping_entities(anonymizer):
    """Test if anonymizer handles overlapping entities correctly."""
    text = "Jan de Vries Bank in Amsterdam"
    results = [
        RecognizerResult(
            entity_type="PERSON",
            start=0,
            end=12,
            score=0.85
        ),
        RecognizerResult(
            entity_type="ORGANIZATION",
            start=0,
            end=17,
            score=0.7
        ),
        RecognizerResult(
            entity_type="LOCATION",
            start=21,
            end=30,
            score=0.9
        )
    ]
    
    anonymized = anonymizer.anonymize_text(text, results)
    assert "[NAAM]" in anonymized
    assert "[LOCATIE]" in anonymized
    assert "Jan de Vries" not in anonymized
    assert "Amsterdam" not in anonymized

def test_anonymize_text_with_adjacent_entities(anonymizer):
    """Test if anonymizer handles adjacent entities correctly."""
    text = "ING Bank Amsterdam"
    results = [
        RecognizerResult(
            entity_type="ORGANIZATION",
            start=0,
            end=8,
            score=0.85
        ),
        RecognizerResult(
            entity_type="LOCATION",
            start=9,
            end=18,
            score=0.9
        )
    ]
    
    anonymized = anonymizer.anonymize_text(text, results)
    assert "[ORGANISATIE]" in anonymized
    assert "[LOCATIE]" in anonymized
    assert "ING Bank" not in anonymized
    assert "Amsterdam" not in anonymized

def test_anonymize_text_with_special_characters(anonymizer):
    """Test if anonymizer handles special characters correctly."""
    text = "Jan-Pieter van der Aa werkt bij 's-Hertogenbosch"
    results = [
        RecognizerResult(
            entity_type="PERSON",
            start=0,
            end=19,
            score=0.85
        ),
        RecognizerResult(
            entity_type="LOCATION",
            start=29,
            end=44,
            score=0.9
        )
    ]
    
    anonymized = anonymizer.anonymize_text(text, results)
    assert "[NAAM]" in anonymized
    assert "[LOCATIE]" in anonymized
    assert "Jan-Pieter" not in anonymized
    assert "'s-Hertogenbosch" not in anonymized

def test_anonymize_text_with_unicode(anonymizer):
    """Test if anonymizer handles Unicode characters correctly."""
    text = "André Çelik woont in Lëtzebuerg"
    results = [
        RecognizerResult(
            entity_type="PERSON",
            start=0,
            end=11,
            score=0.85
        ),
        RecognizerResult(
            entity_type="LOCATION",
            start=21,
            end=31,
            score=0.9
        )
    ]
    
    anonymized = anonymizer.anonymize_text(text, results)
    assert "[NAAM]" in anonymized
    assert "[LOCATIE]" in anonymized
    assert "André" not in anonymized
    assert "Lëtzebuerg" not in anonymized

def test_anonymize_text_with_multiple_occurrences(anonymizer):
    """Test if anonymizer handles multiple occurrences of the same entity correctly."""
    text = "Jan de Vries sprak met Jan de Vries over Amsterdam en Amsterdam"
    results = [
        RecognizerResult(
            entity_type="PERSON",
            start=0,
            end=12,
            score=0.85
        ),
        RecognizerResult(
            entity_type="PERSON",
            start=22,
            end=34,
            score=0.85
        ),
        RecognizerResult(
            entity_type="LOCATION",
            start=40,
            end=49,
            score=0.9
        ),
        RecognizerResult(
            entity_type="LOCATION",
            start=53,
            end=62,
            score=0.9
        )
    ]
    
    anonymized = anonymizer.anonymize_text(text, results)
    assert anonymized.count("[NAAM]") == 2
    assert anonymized.count("[LOCATIE]") == 2
    assert "Jan de Vries" not in anonymized
    assert "Amsterdam" not in anonymized

def test_anonymize_text_with_invalid_input(anonymizer):
    """Test if anonymizer handles invalid input gracefully."""
    with pytest.raises(ValueError):
        anonymizer.anonymize_text(None, [])
    
    with pytest.raises(ValueError):
        anonymizer.anonymize_text("", [])
    
    with pytest.raises(ValueError):
        anonymizer.anonymize_text("text", None)

def test_anonymize_text_with_invalid_operators(anonymizer):
    """Test if anonymizer handles invalid operators gracefully."""
    text = "Jan de Vries woont in Amsterdam"
    results = [
        RecognizerResult(
            entity_type="PERSON",
            start=0,
            end=12,
            score=0.85
        )
    ]
    
    # Test with empty operators dictionary
    with pytest.raises(ValueError, match="Operators dictionary cannot be empty"):
        anonymizer.anonymize_text(text, results, operators={})
    
    # Test with missing operator for entity type
    with pytest.raises(ValueError, match="Missing operators for some entity types"):
        anonymizer.anonymize_text(text, results, operators={"LOCATION": anonymizer.default_operators["LOCATION"]})
    
    # Test with invalid operator type
    with pytest.raises(ValueError, match="All operators must be OperatorConfig objects"):
        anonymizer.anonymize_text(text, results, operators={"PERSON": "invalid"})

if __name__ == "__main__":
    pytest.main([__file__, "-v"])