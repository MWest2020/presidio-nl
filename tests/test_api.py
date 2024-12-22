"""Tests for the FastAPI application."""
import pytest
from fastapi.testclient import TestClient
from src.api.app import app
import time
import concurrent.futures

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

def test_api_response_time(client):
    """Test API response time for various operations."""
    # Test analyze endpoint response time
    start_time = time.time()
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Jan de Vries woont in Amsterdam."
        }
    )
    analyze_time = time.time() - start_time
    assert response.status_code == 200
    assert analyze_time < 1.0  # Response should be under 1 second
    
    # Test anonymize endpoint response time
    start_time = time.time()
    response = client.post(
        "/api/v1/anonymize",
        json={
            "text": "Jan de Vries woont in Amsterdam."
        }
    )
    anonymize_time = time.time() - start_time
    assert response.status_code == 200
    assert anonymize_time < 1.0  # Response should be under 1 second

def test_api_concurrent_requests(client):
    """Test API performance under concurrent load."""
    num_requests = 10
    
    def make_request():
        return client.post(
            "/api/v1/analyze",
            json={
                "text": "Jan de Vries woont in Amsterdam."
            }
        )
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        responses = [f.result() for f in futures]
    
    total_time = time.time() - start_time
    
    # Check all responses were successful
    assert all(r.status_code == 200 for r in responses)
    
    # Check average response time
    avg_time = total_time / num_requests
    assert avg_time < 2.0  # Average response time should be under 2 seconds

def test_api_large_text_performance(client):
    """Test API performance with large text input."""
    # Generate a large text (approximately 100KB)
    large_text = "Jan de Vries woont in Amsterdam. " * 1000
    
    start_time = time.time()
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": large_text
        }
    )
    processing_time = time.time() - start_time
    
    assert response.status_code == 200
    assert processing_time < 5.0  # Should process large text under 5 seconds

def test_api_memory_usage(client):
    """Test API memory usage with repeated requests."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
    
    # Make 50 requests
    for _ in range(50):
        response = client.post(
            "/api/v1/analyze",
            json={
                "text": "Jan de Vries woont in Amsterdam."
            }
        )
        assert response.status_code == 200
    
    final_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
    memory_increase = final_memory - initial_memory
    
    # Memory usage should not increase significantly (less than 100MB)
    assert memory_increase < 100

@pytest.mark.slow
def test_api_long_running_stability(client):
    """Test API stability over a longer period."""
    start_time = time.time()
    request_count = 0
    error_count = 0
    
    # Run for 1 minute
    while time.time() - start_time < 60:
        try:
            response = client.post(
                "/api/v1/analyze",
                json={
                    "text": "Jan de Vries woont in Amsterdam."
                }
            )
            assert response.status_code == 200
            request_count += 1
        except Exception:
            error_count += 1
    
    # Check error rate
    error_rate = error_count / request_count if request_count > 0 else 1
    assert error_rate < 0.01  # Less than 1% errors
    assert request_count > 0  # Should handle multiple requests

if __name__ == "__main__":
    pytest.main([__file__, "-v"])