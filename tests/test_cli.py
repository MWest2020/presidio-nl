import pytest
from src.cli.main import CLI

@pytest.fixture
def cli():
    return CLI()

def test_cli_initialization(cli):
    """Test if CLI initializes correctly."""
    assert cli is not None

def test_cli_analyze_text(cli):
    """Test analyzing text through CLI."""
    text = "Jan de Vries woont in Amsterdam."
    results = cli.analyze_text(text)
    assert len(results) > 0
    
    # Check if we found person and location
    entity_types = {r.entity_type for r in results}
    assert "PERSON" in entity_types
    assert "LOCATION" in entity_types

def test_cli_anonymize_text(cli):
    """Test anonymizing text through CLI."""
    text = "Jan de Vries woont in Amsterdam."
    anonymized = cli.anonymize_text(text)
    
    assert "[NAAM]" in anonymized
    assert "[LOCATIE]" in anonymized
    assert "Jan de Vries" not in anonymized
    assert "Amsterdam" not in anonymized 