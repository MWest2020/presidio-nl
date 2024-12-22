# API Tutorial

Deze tutorial laat zien hoe je de Presidio-NL API kunt gebruiken voor tekstanalyse en anonimisatie.

## Inhoudsopgave
- [Basis Setup](#basis-setup)
- [Configuratie](#configuratie)
- [Tekst Analyseren](#tekst-analyseren)
- [Tekst Anonimiseren](#tekst-anonimiseren)
- [Geavanceerd Gebruik](#geavanceerd-gebruik)
- [Error Handling](#error-handling)
- [Voorbeelden](#voorbeelden)

## Basis Setup

De API is standaard beschikbaar op `http://localhost:8000/api/v1/`. Je kunt dit aanpassen via configuratie.

### Swagger Documentatie

De volledige API documentatie is beschikbaar op `/docs`:
```
http://localhost:8000/docs
```

## Configuratie

### Omgevingsvariabelen

Je kunt de API configureren met de volgende omgevingsvariabelen:

- `API_HOST`: Het host adres waarop de API draait (default: "0.0.0.0")
- `API_PORT`: De poort waarop de API draait (default: 8000)
- `API_ROOT_PATH`: Het basis pad voor alle endpoints (default: "/api/v1")

### Docker Compose

In `docker-compose.yml` kun je de configuratie aanpassen:

```yaml
services:
  api:
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - API_ROOT_PATH=/api/v1
    ports:
      - "8000:8000"  # Pas dit aan naar bijv. "9000:8000" voor een andere poort
```

### Kubernetes / Helm

In `values.yaml` kun je de API configureren:

```yaml
app:
  api:
    host: "0.0.0.0"
    port: 8000
    rootPath: "/api/v1"
    cors:
      enabled: true
      allowOrigins: ["*"]
```

### Authenticatie

*Nog niet geïmplementeerd*

## Tekst Analyseren

### Endpoint
```
POST /analyze
```

### Request Format
```json
{
    "text": "Jan de Vries woont in Amsterdam.",
    "entities": ["PERSON", "LOCATION"]  // Optioneel
}
```

### Voorbeeld met curl
```bash
# Vervang ENDPOINT met je eigen API endpoint
ENDPOINT="http://localhost:8000/api/v1"

curl -X POST "$ENDPOINT/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Jan de Vries woont in Amsterdam."}'
```

### Voorbeeld met Python
```python
import os
import requests

# Configureer het API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

response = requests.post(
    f"{API_URL}/analyze",
    json={
        "text": "Jan de Vries woont in Amsterdam."
    }
)

results = response.json()
print(results)
```

### Voorbeeld Response
```json
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
            "start": 23,
            "end": 32,
            "score": 0.90
        }
    ]
}
```

## Tekst Anonimiseren

### Endpoint
```
POST /anonymize
```

### Request Format
```json
{
    "text": "Jan de Vries woont in Amsterdam.",
    "entities": ["PERSON", "LOCATION"]  // Optioneel
}
```

### Voorbeeld met curl
```bash
# Vervang ENDPOINT met je eigen API endpoint
ENDPOINT="http://localhost:8000/api/v1"

curl -X POST "$ENDPOINT/anonymize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Jan de Vries woont in Amsterdam."}'
```

### Voorbeeld met Python
```python
import os
import requests

# Configureer het API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

response = requests.post(
    f"{API_URL}/anonymize",
    json={
        "text": "Jan de Vries woont in Amsterdam."
    }
)

result = response.json()
print(result["anonymized_text"])
```

### Voorbeeld Response
```json
{
    "original_text": "Jan de Vries woont in Amsterdam.",
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
            "start": 23,
            "end": 32,
            "score": 0.90
        }
    ]
}
```

## Geavanceerd Gebruik

### Specifieke Entiteiten Selecteren

Je kunt specifieke entiteiten selecteren om alleen die te analyseren/anonimiseren:

```python
import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

response = requests.post(
    f"{API_URL}/analyze",
    json={
        "text": "Jan de Vries woont in Amsterdam.",
        "entities": ["PERSON"]  # Alleen persoonsnamen
    }
)
```

### Beschikbare Entiteit Types

- `PERSON`: Persoonsnamen
- `LOCATION`: Locaties
- `PHONE_NUMBER`: Telefoonnummers
- `IBAN`: IBAN rekeningnummers

## Error Handling

De API gebruikt de volgende HTTP status codes:

- `200`: Succesvol
- `422`: Validatie error (bijv. lege tekst of ongeldige entiteiten)
- `500`: Server error

### Voorbeeld Error Handling

```python
import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

try:
    response = requests.post(
        f"{API_URL}/analyze",
        json={
            "text": "",  # Lege tekst geeft een 422 error
            "entities": ["INVALID"]  # Ongeldige entiteit geeft een 422 error
        }
    )
    response.raise_for_status()
    result = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 422:
        errors = e.response.json()
        print(f"Validatie error: {errors['detail']}")
    else:
        print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

## Health Check

Je kunt de status van de API controleren met het health endpoint:

```bash
# Vervang ENDPOINT met je eigen API endpoint
ENDPOINT="http://localhost:8000/api/v1"

curl $ENDPOINT/health
```

Response:
```json
{
    "status": "healthy"
}
``` 