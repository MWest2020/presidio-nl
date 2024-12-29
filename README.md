# Presidio-NL

Nederlandse versie van Microsoft Presidio voor het herkennen en anonimiseren van gevoelige informatie in tekst.

## Features

- 🔍 Herkenning van Nederlandse entiteiten (personen, locaties, etc.)
- 🔒 Anonimisatie van gevoelige informatie
- 🌐 REST API voor integratie
- 💻 CLI tool voor lokaal gebruik
- ☁️ Kubernetes/Helm deployment support

## Quick Start

```bash
# Start met Docker
docker compose up api

# Test de API
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Jan de Vries woont in Amsterdam"}'
```

## Documentatie

### 📚 Tutorials
- [Quickstart Guide](docs/tutorials/quickstart.md) - Begin hier!
- [API Tutorial](docs/tutorials/api.md) - Leer de API gebruiken
- [CLI Tutorial](docs/tutorials/cli.md) - Werk met de command line tool

### 📖 Guides
- [Installation Guide](docs/guides/installation.md) - Gedetailleerde installatie instructies
- [Deployment Guide](docs/guides/deployment.md) - Productie deployment handleiding

### 📑 Reference
- [API Reference](docs/reference/api.md) - API specificatie
- [CLI Reference](docs/reference/cli.md) - CLI commando's
- [Configuration](docs/reference/configuration.md) - Configuratie opties

## Development

```bash
# Installeer development dependencies
pip install -r requirements/dev.txt

# Run tests
python -m pytest
```

## License

[MIT License](LICENSE)

## Contact

Voor vragen en support:
- 📧 Email: [support@example.com](mailto:support@example.com)
- 🌐 Website: [https://example.com](https://example.com)
- 💬 GitHub Issues: [Report een probleem](https://github.com/your-org/presidio-nl/issues)