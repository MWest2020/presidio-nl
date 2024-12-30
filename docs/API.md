# API Documentatie

## Endpoints

### 1. Tekst Analyse

**Endpoint:** `POST /api/v1/analyze`

Analyseert tekst en detecteert entiteiten.

**Request:**
```json
{
  "text": "Jan de Vries woont in Amsterdam",
  "entities": ["PERSON", "LOCATION"]  // Optioneel
}
```

**Response:**
```json
{
  "results": [
    {
      "entity_type": "PERSON",
      "text": "Jan de Vries",
      "start": 0,
      "end": 12,
      "score": 0.98
    },
    {
      "entity_type": "LOCATION",
      "text": "Amsterdam",
      "start": 22,
      "end": 31,
      "score": 0.95
    }
  ]
}
```

### 2. Tekst Anonimisatie

**Endpoint:** `POST /api/v1/anonymize`

Anonimiseert tekst door gevonden entiteiten te vervangen.

**Request:**
```json
{
  "text": "Jan de Vries woont in Amsterdam",
  "entities": ["PERSON", "LOCATION"]  // Optioneel
}
```

**Response:**
```json
{
  "original_text": "Jan de Vries woont in Amsterdam",
  "anonymized_text": "[NAAM] woont in [LOCATIE]",
  "entities_found": [
    {
      "entity_type": "PERSON",
      "text": "Jan de Vries",
      "start": 0,
      "end": 12,
      "score": 0.98
    },
    {
      "entity_type": "LOCATION",
      "text": "Amsterdam",
      "start": 22,
      "end": 31,
      "score": 0.95
    }
  ]
}
```

### 3. PDF Anonimisatie

**Endpoint:** `POST /api/v1/anonymize/pdf`

Upload en anonimiseer een PDF bestand.

**Request:**
```
Content-Type: multipart/form-data
pdf_file: <binary>
entities: ["PERSON", "LOCATION"]  // Optioneel
```

**Response:**
```json
{
  "total_entities": 28,
  "entities_by_type": {
    "PERSON": [
      {
        "text": "Jan de Vries",
        "score": 0.98
      }
    ],
    "LOCATION": [
      {
        "text": "Amsterdam",
        "score": 0.95
      }
    ]
  },
  "anonymized_pdf_url": "/download/anon_1234567890_document.pdf"
}
```

### 4. PDF Download

**Endpoint:** `GET /download/{filename}`

Download een geanonimiseerde PDF.

**Response:**
- Content-Type: application/pdf
- Binary PDF bestand

## Error Responses

Alle endpoints kunnen de volgende errors teruggeven:

- `400 Bad Request`: Ongeldige input
- `422 Unprocessable Entity`: Validatie error
- `500 Internal Server Error`: Server error

Voorbeeld error response:
```json
{
  "detail": "Error message here"
}
```

## Opmerkingen

1. **Bestandsopslag**
   - PDFs worden 1 uur bewaard
   - Automatische cleanup van oude bestanden
   - Unieke bestandsnamen met timestamp

2. **Rate Limiting**
   - Geen rate limiting geïmplementeerd
   - Overweeg voor productie gebruik

3. **Authenticatie**
   - Momenteel geen authenticatie
   - Overweeg voor productie gebruik

4. **CORS**
   - Alle origins toegestaan (`*`)
   - Pas aan voor productie gebruik 