import os
import pytest
import requests
from fastapi.testclient import TestClient
from src.api.app import app

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
TEST_TEXT = "Jan de Vries woont in Amsterdam."

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def live_api():
    """Check if the live API is available."""
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        pass
    return False

@pytest.fixture
def sample_text():
    """Return a sample text for testing."""
    return TEST_TEXT

@pytest.fixture
def sample_entities():
    """Return a list of valid entity types."""
    return ["PERSON", "LOCATION"]

@pytest.fixture
def sample_analysis_result():
    """Return a sample analysis result."""
    return {
        "results": [
            {
                "entity_type": "PERSON",
                "text": "Jan de Vries",
                "start": 0,
                "end": 12,
                "score": 0.85
            },
            {
                "entity_type": "LOCATION",
                "text": "Amsterdam",
                "start": 22,
                "end": 31,
                "score": 0.85
            }
        ]
    }

@pytest.fixture
def sample_anonymized_result():
    """Return a sample anonymized result."""
    return {
        "original_text": TEST_TEXT,
        "anonymized_text": "[NAAM] woont in [LOCATIE].",
        "entities_found": [
            {
                "entity_type": "PERSON",
                "text": "Jan de Vries",
                "start": 0,
                "end": 12,
                "score": 0.85
            },
            {
                "entity_type": "LOCATION",
                "text": "Amsterdam",
                "start": 22,
                "end": 31,
                "score": 0.85
            }
        ]
    } 