import pytest
from src.analyzer.engine import DutchTextAnalyzer

@pytest.fixture
def analyzer():
    return DutchTextAnalyzer()

def test_analyzer_initialization(analyzer):
    """Test if analyzer initializes correctly."""
    assert analyzer is not None
    assert analyzer.default_entities == [
        "PERSON",
        "LOCATION",
        "PHONE_NUMBER",
        "IBAN_CODE"
    ]

def test_analyze_text_with_person(analyzer):
    """Test if analyzer can detect person names."""
    text = "Jan de Vries woont in Amsterdam."
    results = analyzer.analyze_text(text)
    
    # Check if we found at least one person
    person_results = [r for r in results if r.entity_type == "PERSON"]
    assert len(person_results) > 0
    assert "Jan de Vries" in text[person_results[0].start:person_results[0].end]

def test_analyze_text_with_location(analyzer):
    """Test if analyzer can detect locations."""
    text = "Jan de Vries woont in Amsterdam."
    results = analyzer.analyze_text(text)
    
    # Check if we found the location
    location_results = [r for r in results if r.entity_type == "LOCATION"]
    assert len(location_results) > 0
    assert "Amsterdam" in text[location_results[0].start:location_results[0].end]

def test_analyze_text_with_phone_number(analyzer):
    """Test if analyzer can detect phone numbers."""
    text = "Mijn telefoonnummer is 06-12345678"
    results = analyzer.analyze_text(text)
    
    # Check if we found the phone number
    phone_results = [r for r in results if r.entity_type == "PHONE_NUMBER"]
    assert len(phone_results) > 0
    assert "06-12345678" in text[phone_results[0].start:phone_results[0].end]

def test_analyze_text_with_iban(analyzer):
    """Test if analyzer can detect IBAN numbers."""
    text = "Mijn rekeningnummer is NL91ABNA0417164300"
    results = analyzer.analyze_text(text)
    
    # Check if we found the IBAN
    iban_results = [r for r in results if r.entity_type == "IBAN_CODE"]
    assert len(iban_results) > 0
    assert "NL91ABNA0417164300" in text[iban_results[0].start:iban_results[0].end]

def test_analyze_text_with_custom_entities(analyzer):
    """Test if analyzer works with custom entity list."""
    text = "Jan de Vries woont in Amsterdam."
    results = analyzer.analyze_text(text, entities=["PERSON"])
    
    # Should only find person, not location
    assert all(r.entity_type == "PERSON" for r in results)
    assert not any(r.entity_type == "LOCATION" for r in results) 