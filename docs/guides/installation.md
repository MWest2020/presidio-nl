# Installatie Guide

Deze guide beschrijft alle manieren om Presidio-NL te installeren en configureren.

## Docker Installatie (Aanbevolen)

De eenvoudigste manier om Presidio-NL te gebruiken is via Docker:

```bash
# Clone de repository
git clone https://github.com/your-org/presidio-nl.git
cd presidio-nl

# Start de services
docker compose up api    # Alleen API
# of
docker compose up       # API + CLI
```

### Docker Configuratie

Pas de configuratie aan in `docker-compose.yml`:

```yaml
services:
  api:
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - API_ROOT_PATH=/api/v1
```

## Pip Installatie

Voor lokale ontwikkeling of integratie in bestaande Python projecten:

```bash
# Basis installatie
pip install -r requirements/base.txt

# API dependencies
pip install -r requirements/api.txt

# Development dependencies
pip install -r requirements/dev.txt
```

### Python Configuratie

Configureer via environment variables:

```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export API_ROOT_PATH=/api/v1
```

## Kubernetes Installatie

Voor productie deployments, zie onze [Deployment Guide](deployment.md).

## Systeem Vereisten

- Python 3.9+
- Docker 20.10+ (voor Docker installatie)
- 4GB RAM minimum
- 2GB vrije schijfruimte

## Troubleshooting

### Veel voorkomende problemen

1. **Port already in use**
   ```bash
   # Controleer poort gebruik
   netstat -ano | findstr :8000
   ```

2. **Memory issues**
   - Verhoog Docker memory limit
   - Controleer systeem resources

3. **Model download fails**
   - Controleer internet connectie
   - Verifieer schrijfrechten in cache directory 