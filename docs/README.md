# Presidio-NL Documentation

## Quick Start

### Container Registry Setup

To build and push the container image:
```bash
# Build the image
docker build -t ghcr.io/mwest2020/presidio-nl:latest .

# Login to GitHub Container Registry
docker login ghcr.io -u YOUR_GITHUB_USERNAME
# Use a GitHub Personal Access Token with these scopes:
# - write:packages
# - read:packages
# - delete:packages
# - repo (for private repositories)

# Push the image
docker push ghcr.io/mwest2020/presidio-nl:latest
```

### Met Docker

```bash
# Start de API server
docker-compose up api

# De API is nu beschikbaar op http://localhost:8000
# Swagger documentatie op http://localhost:8000/docs
```

### CLI Gebruik

De CLI ondersteunt twee hoofdcommando's:
```bash
# Analyseer tekst of bestand
python -m main analyze "Jan de Vries woont in Amsterdam"
python -m main analyze bestand.txt

# Anonimiseer tekst of bestand
python -m main anonymize "Jan de Vries woont in Amsterdam"
python -m main anonymize bestand.txt
```

## API Endpoints

### Tekst Verwerking

1. **Tekst Analyseren**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Jan de Vries woont in Amsterdam"}'
```

2. **Tekst Anonimiseren**
```bash
curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Jan de Vries woont in Amsterdam"}'
```

### PDF Verwerking

1. **PDF Anonimiseren**
```bash
# Upload en verwerk PDF
curl -X POST "http://localhost:8000/api/v1/anonymize/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "pdf_file=@document.pdf"

# Download resultaat (vervang TIMESTAMP)
curl -o output.pdf http://localhost:8000/download/anon_TIMESTAMP_document.pdf
```

## Docker Configuratie

### Environment Variables

```yaml
environment:
  - API_HOST=0.0.0.0
  - API_PORT=8000
  - STORAGE_DIR=/app/storage    # Locatie voor PDF opslag
  - MAX_STORAGE_TIME=3600      # Cleanup tijd in seconden
```

### Volumes

```yaml
volumes:
  - ./src:/app/src             # Code
  - pip-cache:/root/.cache/pip # Python packages
  - model-cache:/app/models    # AI modellen
  - pdf-storage:/app/storage   # PDF opslag
```

## Ondersteunde Entiteiten

- `PERSON`: Namen van personen
- `LOCATION`: Locaties, adressen, plaatsnamen
- `PHONE_NUMBER`: Telefoonnummers
- `IBAN`: Nederlandse bankrekeningnummers
- `EMAIL`: Email adressen
- `ORGANIZATION`: Organisaties en bedrijven

## Bestandsformaten

- Platte tekst (`.txt`)
- PDF documenten (`.pdf`)
  - Automatische layout behoud
  - Entiteiten worden vervangen door placeholders
  - Geanonimiseerde PDFs worden tijdelijk opgeslagen (1 uur)

## Ontwikkeling

### Setup Development Omgeving

```bash
# Clone repository
git clone [repository-url]
cd presidio-nl

# Start met Docker
docker-compose up api

# Of lokaal
python -m pip install -r requirements/dev.txt
python -m main analyze "Test tekst"
```

### API vs CLI

- **API**: Geschikt voor integratie in andere applicaties, webinterfaces
- **CLI**: Handig voor batch verwerking en command line gebruik

De API biedt meer functionaliteit (zoals PDF verwerking) en is de aanbevolen methode voor productie gebruik. 