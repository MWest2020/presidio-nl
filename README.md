# Presidio-NL

Een Nederlandse versie van Microsoft Presidio voor het herkennen en anonimiseren van gevoelige informatie in tekst.

## Features

- Herkenning van Nederlandse entiteiten (personen, locaties, etc.)
- Anonimisatie van gevoelige informatie
- REST API voor integratie
- CLI tool voor lokaal gebruik
- Kubernetes/Helm deployment support

## Installatie

### Met pip

```bash
pip install -r requirements/base.txt  # Basis functionaliteit
pip install -r requirements/api.txt   # Voor de REST API
```

### Met Docker

```bash
docker-compose up api  # Start alleen de API
# of
docker-compose up     # Start zowel API als CLI
```

## API Gebruik

De API draait standaard op `http://localhost:8000/api/v1/`. Je kunt dit aanpassen via:

1. Omgevingsvariabelen:
   ```bash
   export API_HOST=0.0.0.0
   export API_PORT=8000
   export API_ROOT_PATH=/api/v1
   ```

2. Docker Compose:
   ```yaml
   services:
     api:
       environment:
         - API_HOST=0.0.0.0
         - API_PORT=8000
         - API_ROOT_PATH=/api/v1
   ```

3. Helm Values:
   ```yaml
   app:
     api:
       host: "0.0.0.0"
       port: 8000
       rootPath: "/api/v1"
   ```

### API Endpoints

- Health Check: `GET /api/v1/health`
- Analyze: `POST /api/v1/analyze`
- Anonymize: `POST /api/v1/anonymize`

Zie de [API Tutorial](docs/api_tutorial.md) voor meer details en voorbeelden.

## CLI Gebruik

De CLI ondersteunt twee hoofdcommando's:

```bash
# Analyseer tekst
python main.py analyze "Jan de Vries woont in Amsterdam."

# Anonimiseer tekst
python main.py anonymize "Jan de Vries woont in Amsterdam."
```

Zie de [CLI Tutorial](docs/cli_tutorial.md) voor meer details en voorbeelden.

## Development

1. Clone de repository
2. Installeer development dependencies:
   ```bash
   pip install -r requirements/dev.txt
   ```
3. Run de tests:
   ```bash
   python -m pytest
   ```

## Deployment

Zie de [Helm Installatie Guide](docs/helm_installation.md) voor instructies over het deployen naar Kubernetes.