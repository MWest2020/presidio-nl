# API Tutorial

### Basic Setup

The API server runs on `http://localhost:8000` by default. You can customize the host and port by setting the appropriate environment variables or command line arguments when starting the server.

### API Endpoints

#### 1. Health Check
```bash
GET /api/v1/health

# Example response:
{
    "status": "healthy"
}
```

#### 2. Analyze Text
```bash
POST /api/v1/analyze
Content-Type: application/json

{
    "text": "Jan de Vries woont in Amsterdam.",
    "entities": ["PERSON", "LOCATION"]  # Optional
}

# Example response:
{
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
```

#### 3. Anonymize Text
```bash
POST /api/v1/anonymize
Content-Type: application/json

{
    "text": "Jan de Vries woont in Amsterdam.",
    "entities": ["PERSON", "LOCATION"]  # Optional
}

# Example response:
{
    "original_text": "Jan de Vries woont in Amsterdam.",
    "anonymized_text": "<PERSON> woont in <LOCATION>.",
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
```

### Testing with cURL

Here are examples of how to test the API using cURL:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Analyze text
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Jan de Vries woont in Amsterdam.\"}"

# Anonymize text
curl -X POST http://localhost:8000/api/v1/anonymize \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Jan de Vries woont in Amsterdam.\"}"
```

Note: When using Windows Command Prompt, use `^` instead of `\` for line continuation.

### Interactive Documentation

You can also explore the API using the interactive Swagger documentation at `http://localhost:8000/docs`.