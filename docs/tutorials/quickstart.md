# Quickstart Guide

Deze quickstart guide helpt je om snel aan de slag te gaan met Presidio-NL.

## Installatie

```bash
# Met Docker (aanbevolen voor de API)
docker compose up api

# Of met pip (voor CLI gebruik)
pip install -r requirements/base.txt
```

## Eerste gebruik

### Via de CLI (Lokaal)

1. **Analyseer tekst:**
   ```bash
   python main.py analyze "Jan de Vries woont in Amsterdam"
   ```

2. **Anonimiseer tekst:**
   ```bash
   python main.py anonymize "Jan de Vries woont in Amsterdam"
   ```

3. **Verwerk een bestand:**
   ```bash
   python main.py anonymize --input-file input.txt --output-file output.txt
   ```

### Via de API (Server)

1. **Test de API:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "Jan de Vries woont in Amsterdam"}'
   ```

2. **Anonimiseer via API:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/anonymize \
     -H "Content-Type: application/json" \
     -d '{"text": "Jan de Vries woont in Amsterdam"}'
   ```

## Ondersteunde Entiteiten

- `PERSON`: Namen van personen
- `LOCATION`: Geografische locaties
- `PHONE_NUMBER`: Telefoonnummers
- `IBAN`: IBAN rekeningnummers

## Volgende stappen

### Voor CLI gebruik
- [CLI Tutorial](cli.md) - Uitgebreide CLI functionaliteit
- [CLI Reference](../reference/cli.md) - Alle CLI opties

### Voor API gebruik
- [API Tutorial](api.md) - Leer de API gebruiken
- [API Reference](../reference/api.md) - API specificatie

### Deployment
- [Installation Guide](../guides/installation.md) - Andere installatie methoden
- [Deployment Guide](../guides/deployment.md) - Productie deployment 