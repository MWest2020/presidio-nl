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

**Endpoint:** `POST /api/v1/anonymize/text`

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
file: <binary>  // PDF bestand
entities: ["PERSON", "LOCATION"]  // Optioneel
use_ocr: false  // Optioneel, gebruik OCR voor gescande PDFs
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
  "input_file": "/tmp/temp123.pdf",
  "output_file": "/app/storage/1234567890_document_geanonimiseerd.pdf",
  "download_link": "/api/v1/download/1234567890_document_geanonimiseerd.pdf"
}
```

### 4. PDF Download

**Endpoint:** `GET /api/v1/download/{filename}`

Download een geanonimiseerde PDF. De `filename` moet exact overeenkomen met wat je in de `download_link` van de PDF anonimisatie response hebt ontvangen.

**Response:**
- Content-Type: application/pdf
- Binary PDF bestand

**Voorbeeld:**
```bash
# Upload en verwerk PDF
curl -X POST "http://localhost:8000/api/v1/anonymize/pdf" \
  -F "file=@document.pdf"

# Download resultaat (gebruik filename uit download_link)
curl -o output.pdf "http://localhost:8000/api/v1/download/1234567890_document_geanonimiseerd.pdf"
```

## Error Responses

Alle endpoints kunnen de volgende errors teruggeven:

- `400 Bad Request`: Ongeldige input (bijv. geen PDF bestand)
- `404 Not Found`: Bestand niet gevonden bij download
- `422 Unprocessable Entity`: Validatie error
- `500 Internal Server Error`: Server error

Voorbeeld error response:
```json
{
  "detail": "Bestand niet gevonden. Mogelijk is de verwerking nog bezig of is het bestand verlopen (na 3600 seconden)."
}
```

## Opmerkingen

1. **Bestandsopslag**
   - PDFs worden 1 uur bewaard in de container
   - Automatische cleanup van oude bestanden
   - Unieke bestandsnamen met timestamp
   - Download direct na verwerking om verlopen te voorkomen

2. **Rate Limiting**
   - Geen rate limiting geïmplementeerd
   - Overweeg voor productie gebruik

3. **Authenticatie**
   - Momenteel geen authenticatie
   - Overweeg voor productie gebruik

4. **CORS**
   - Alle origins toegestaan (`*`)
   - Pas aan voor productie gebruik

5. **OCR Support**
   - Optionele OCR voor gescande PDFs
   - Vereist Tesseract installatie in container
   - Kan langzamer zijn dan normale PDF verwerking

## Kubernetes/Cluster Deployment

### 1. Deployment in Cluster

De API kan worden gedeployed in een Kubernetes cluster in de `conduction` namespace:

```bash
# Deploy in conduction namespace
kubectl apply -f k8s/ -n conduction
```

### 2. Service Discovery

De service is beschikbaar binnen het cluster via:
- Service naam: `presidio-nl-api`
- Namespace: `conduction`
- Intern endpoint: `http://presidio-nl-api.conduction.svc.cluster.local`

### 3. Externe Toegang

#### Via Ingress
De API is bereikbaar via de ingress controller op:
```
https://api.presidio-nl.conduction.nl
```

Alle API endpoints zijn beschikbaar onder dit base path:
```bash
# Voorbeeld text analyse
curl -X POST "https://api.presidio-nl.conduction.nl/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'

# Voorbeeld PDF verwerking
curl -X POST "https://api.presidio-nl.conduction.nl/api/v1/anonymize/pdf" \
  -F "file=@document.pdf"
```

#### Vanuit Nextcloud App

Voor integratie met een Nextcloud app:

1. **Directe Service Communicatie**
Als de Nextcloud app in hetzelfde cluster draait:
```php
$apiUrl = 'http://presidio-nl-api.conduction.svc.cluster.local';
```

2. **Via Ingress**
Als de Nextcloud app extern draait:
```php
$apiUrl = 'https://api.presidio-nl.conduction.nl';
```

3. **API Gebruik Voorbeeld (PHP)**
```php
// PDF Verwerking
$file = '/path/to/file.pdf';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $apiUrl . '/api/v1/anonymize/pdf');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, [
    'file' => new CURLFile($file)
]);
$response = curl_exec($ch);
$result = json_decode($response, true);

// Download verwerkt bestand
$downloadUrl = $apiUrl . $result['download_link'];
```

### 4. Security Overwegingen

1. **Netwerk Policies**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: presidio-nl-api
  namespace: conduction
spec:
  podSelector:
    matchLabels:
      app: presidio-nl-api
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: nextcloud
```

2. **Resource Limieten**
De API heeft de volgende resource limieten:
```yaml
resources:
  limits:
    memory: "1Gi"
    cpu: "1"
  requests:
    memory: "512Mi"
    cpu: "200m"
```

3. **Storage**
- Verwerkte PDFs worden 1 uur bewaard
- Storage wordt automatisch opgeruimd
- PVC wordt gebruikt voor persistente opslag

### 5. Monitoring

De API exposed metrics voor Prometheus op:
```
http://presidio-nl-api.conduction.svc.cluster.local:8000/metrics
```

Health check endpoint:
```
http://presidio-nl-api.conduction.svc.cluster.local:8000/health
```

### 6. Logging

Logs zijn beschikbaar via:
```bash
kubectl logs -f deployment/presidio-nl-api -n conduction
```

Of via Kibana als logging stack is geïnstalleerd. 