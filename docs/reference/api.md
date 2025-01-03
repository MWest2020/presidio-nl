# API Reference

## Endpoints

### POST /api/v1/anonymize/text

Anonimiseer tekst.

**Request Body:**
```json
{
    "text": "string",
    "entities": ["PERSON", "LOCATION", ...]  // Optioneel
}
```

**Query Parameters:**
- `use_ocr` (boolean, optional): Of OCR gebruikt moet worden (default: false)

**Response:**
```json
{
    "original_text": "string",
    "anonymized_text": "string",
    "entities_found": [
        {
            "entity_type": "string",
            "text": "string",
            "score": 0.95
        }
    ]
}
```

### POST /api/v1/anonymize/pdf

Anonimiseer een PDF bestand.

**Request:**
- Multipart form data met PDF bestand

**Query Parameters:**
- `entities` (array[string], optional): Lijst van entiteiten om te detecteren
- `use_ocr` (boolean, optional): Of OCR gebruikt moet worden voor gescande PDFs (default: false)

**Response:**
```json
{
    "statistics": {
        "total_entities": 5,
        "entities_by_type": {
            "PERSON": [
                {
                    "text": "string",
                    "score": 0.95
                }
            ]
        }
    },
    "anonymized_content": "base64 encoded PDF"
}
```

## Voorbeelden

### Tekst Anonimisatie

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Jan de Vries woont in Amsterdam",
    "entities": ["PERSON", "LOCATION"]
  }'
```

### PDF Anonimisatie

Normale PDF:
```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/pdf" \
  -F "file=@document.pdf"
```

Gescande PDF met OCR:
```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/pdf?use_ocr=true" \
  -F "file=@scanned_document.pdf"
```

## Docker Deployment

Start de API server met Docker:

```bash
# Build de image
docker build -t presidio-nl .

# Start de container
docker run -p 8000:8000 presidio-nl
```

## Vereisten

Voor OCR functionaliteit:
- Tesseract OCR (automatisch geïnstalleerd in Docker)
- Poppler Utils (automatisch geïnstalleerd in Docker)

Bij lokaal gebruik:
- Tesseract OCR met Nederlandse taaldata
- Poppler Utils voor PDF verwerking

## Environment Variables

- `TESSERACT_CMD`: Pad naar Tesseract executable (default: `C:\Program Files\Tesseract-OCR\tesseract.exe`)
- `POPPLER_PATH`: Pad naar Poppler binaries (default: `C:\Program Files\poppler-24.02.0\Library\bin`) 