# API Reference

Gedetailleerde documentatie van alle API endpoints.

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check

```http
GET /health
```

Response:
```json
{
    "status": "healthy"
}
```

### Analyze Text

```http
POST /analyze
```

Request body:
```json
{
    "text": "string",
    "entities": ["PERSON", "LOCATION"]  // Optional
}
```

Response:
```json
{
    "results": [
        {
            "entity_type": "PERSON",
            "text": "Jan de Vries",
            "start": 0,
            "end": 11,
            "score": 0.95
        }
    ]
}
```

### Anonymize Text

```http
POST /anonymize
```

Request body:
```json
{
    "text": "string",
    "entities": ["PERSON", "LOCATION"]  // Optional
}
```

Response:
```json
{
    "original_text": "Jan de Vries woont in Amsterdam",
    "anonymized_text": "[NAAM] woont in [LOCATIE]",
    "entities_found": [
        {
            "entity_type": "PERSON",
            "text": "Jan de Vries",
            "start": 0,
            "end": 11,
            "score": 0.95
        }
    ]
}
```

## Ondersteunde Entiteiten

- `PERSON`: Namen van personen
- `LOCATION`: Geografische locaties
- `PHONE_NUMBER`: Telefoonnummers
- `IBAN`: IBAN rekeningnummers

## Error Responses

```json
{
    "detail": "Error message"
}
```

HTTP Status Codes:
- 400: Invalid request
- 422: Validation error
- 500: Server error 