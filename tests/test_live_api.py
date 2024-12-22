import pytest
import requests
import os

# Skip all tests if live API is not available
pytestmark = pytest.mark.live

def test_health_check(live_api):
    """Test if the API health check endpoint is working."""
    if not live_api:
        pytest.skip("Live API is not available")
    
    response = requests.get(f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_text(live_api, sample_text, sample_analysis_result):
    """Test analyzing text with valid input."""
    if not live_api:
        pytest.skip("Live API is not available")
    
    response = requests.post(
        f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/analyze",
        json={
            "text": sample_text
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert len(result["results"]) == len(sample_analysis_result["results"])
    for actual, expected in zip(result["results"], sample_analysis_result["results"]):
        assert actual["entity_type"] == expected["entity_type"]
        assert actual["text"] == expected["text"]

def test_analyze_empty_text(live_api):
    """Test error handling for empty text."""
    if not live_api:
        pytest.skip("Live API is not available")
    
    response = requests.post(
        f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/analyze",
        json={
            "text": ""
        }
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert any("empty" in str(err).lower() for err in error_detail)

def test_analyze_invalid_entities(live_api, sample_text):
    """Test error handling for invalid entities."""
    if not live_api:
        pytest.skip("Live API is not available")
    
    response = requests.post(
        f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/analyze",
        json={
            "text": sample_text,
            "entities": ["INVALID_ENTITY"]
        }
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert any("unsupported" in str(err).lower() for err in error_detail)

def test_anonymize_text(live_api, sample_text, sample_anonymized_result):
    """Test anonymizing text with valid input."""
    if not live_api:
        pytest.skip("Live API is not available")
    
    response = requests.post(
        f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/anonymize",
        json={
            "text": sample_text
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert result["original_text"] == sample_anonymized_result["original_text"]
    assert "[NAAM]" in result["anonymized_text"]
    assert "[LOCATIE]" in result["anonymized_text"]
    assert len(result["entities_found"]) == len(sample_anonymized_result["entities_found"])

def test_anonymize_specific_entities(live_api, sample_text):
    """Test anonymizing only specific entity types."""
    if not live_api:
        pytest.skip("Live API is not available")
    
    response = requests.post(
        f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/anonymize",
        json={
            "text": sample_text,
            "entities": ["PERSON"]
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "[NAAM]" in result["anonymized_text"]
    assert "Amsterdam" in result["anonymized_text"]  # Location should not be anonymized
    assert len(result["entities_found"]) == 1

def test_api_error_handling(live_api):
    """Test various error scenarios."""
    if not live_api:
        pytest.skip("Live API is not available")
    
    # Test invalid JSON
    response = requests.post(
        f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/analyze",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422

    # Test missing required field
    response = requests.post(
        f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/analyze",
        json={}
    )
    assert response.status_code == 422

    # Test invalid HTTP method
    response = requests.get(f"{os.getenv('API_URL', 'http://localhost:8000/api/v1')}/analyze")
    assert response.status_code == 405

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 