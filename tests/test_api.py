"""Tests for the FastAPI application."""
import pytest
from fastapi.testclient import TestClient
from src.api.app import app

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_text(client):
    """Test text analysis endpoint."""
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Jan de Vries woont in Amsterdam."
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "results" in data
    assert isinstance(data["results"], list)
    
    # Check if we found both person and location
    entities_found = {r["entity_type"] for r in data["results"]}
    assert "PERSON" in entities_found
    assert "LOCATION" in entities_found
    
    # Check result details
    for result in data["results"]:
        assert "entity_type" in result
        assert "text" in result
        assert "start" in result
        assert "end" in result
        assert "score" in result
        assert isinstance(result["score"], float)
        assert 0 <= result["score"] <= 1

def test_analyze_text_with_specific_entities(client):
    """Test text analysis with specific entities."""
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Jan de Vries woont in Amsterdam.",
            "entities": ["PERSON"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should only find person, not location
    entities_found = {r["entity_type"] for r in data["results"]}
    assert "PERSON" in entities_found
    assert "LOCATION" not in entities_found

def test_anonymize_text(client):
    """Test text anonymization endpoint."""
    response = client.post(
        "/api/v1/anonymize",
        json={
            "text": "Jan de Vries woont in Amsterdam."
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "original_text" in data
    assert "anonymized_text" in data
    assert "entities_found" in data
    
    # Check anonymization
    assert "[NAAM]" in data["anonymized_text"]
    assert "[LOCATIE]" in data["anonymized_text"]
    assert "Jan de Vries" not in data["anonymized_text"]
    assert "Amsterdam" not in data["anonymized_text"]

def test_anonymize_text_with_specific_entities(client):
    """Test text anonymization with specific entities."""
    response = client.post(
        "/api/v1/anonymize",
        json={
            "text": "Jan de Vries woont in Amsterdam.",
            "entities": ["PERSON"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should only anonymize person, not location
    assert "[NAAM]" in data["anonymized_text"]
    assert "Amsterdam" in data["anonymized_text"]
    assert "[LOCATIE]" not in data["anonymized_text"]

def test_analyze_empty_text(client):
    """Test error handling for empty text."""
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": ""
        }
    )
    
    assert response.status_code == 422
    errors = response.json()
    assert any("empty" in str(error).lower() for error in errors["detail"])

def test_analyze_invalid_entities(client):
    """Test error handling for invalid entities."""
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Jan de Vries woont in Amsterdam.",
            "entities": ["INVALID_ENTITY"]
        }
    )
    
    assert response.status_code == 422
    errors = response.json()
    assert any("unsupported" in str(error).lower() for error in errors["detail"])

def test_analyze_complex_text(client):
    """Test analysis of text with multiple entity types."""
    text = """
    Sophie van Dijk (tel: 06-12345678) woont in Rotterdam.
    Haar IBAN is NL91ABNA0417164300.
    """
    
    response = client.post(
        "/api/v1/analyze",
        json={"text": text}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should find all entity types
    entities_found = {r["entity_type"] for r in data["results"]}
    assert "PERSON" in entities_found
    assert "LOCATION" in entities_found
    assert "PHONE_NUMBER" in entities_found
    assert "IBAN_CODE" in entities_found 

def test_live_api():
    """Test the live API endpoints."""
    import requests
    
    # Test analyze endpoint
    response = requests.post(
        "http://localhost:8000/api/v1/analyze",
        json={
            "text": "Jan de Vries woont in Amsterdam."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2
    
    # Test anonymize endpoint
    response = requests.post(
        "http://localhost:8000/api/v1/anonymize",
        json={
            "text": "Jan de Vries woont in Amsterdam."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "[NAAM]" in data["anonymized_text"]
    assert "[LOCATIE]" in data["anonymized_text"]