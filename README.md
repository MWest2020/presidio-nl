# Presidio-NL: Nederlandse Tekst Anonimisatie

Dit open source project combineert [Microsoft Presidio](https://github.com/microsoft/presidio) met SpaCy voor het analyseren en anonimiseren van Nederlandse tekst. Het project biedt zowel een CLI-tool als een REST API voor het identificeren en anonimiseren van gevoelige informatie zoals namen, locaties, telefoonnummers en IBAN-nummers.

## Features
- **Entiteitsanalyse:** Identificeer gevoelige informatie zoals:
  - Persoonlijke namen
  - Locaties
  - Telefoonnummers
  - IBAN-nummers
- **Anonimisatie:** Vervang gevoelige informatie met configureerbare placeholders
- **Nederlandstalige ondersteuning:** Geoptimaliseerd voor Nederlandse teksten met SpaCy
- **Flexibele interfaces:** Beschikbaar als CLI-tool en REST API
- **Uitbreidbaar:** Eenvoudig nieuwe entiteitstypen en anonimisatie-opties toevoegen
- **Type-safe:** Volledig voorzien van type hints
- **Goed getest:** Uitgebreide test suite met pytest

## Projectstructuur
```
presidio-nl/
├── src/
│   ├── analyzer/          # Tekstanalyse functionaliteit
│   ├── anonymizer/        # Anonimisatie functionaliteit
│   ��── api/              # REST API implementatie
│   └── cli/              # Command-line interface
├── tests/                # Test suite
├── requirements/         # Dependencies per omgeving
└── main.py              # Command-line entry point
```

## Installatie

1. Clone de repository:
   ```bash
   git clone https://github.com/MWest2020/Presidio-x-RobBERT
   cd Presidio-x-RobBERT
   ```

2. Maak een virtuele omgeving aan (optioneel maar aanbevolen):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # OF
   .\venv\Scripts\activate  # Windows
   ```

3. Installeer de dependencies:
   ```bash
   # Voor CLI gebruik:
   pip install -r requirements/base.txt

   # Voor API gebruik:
   pip install -r requirements/api.txt

   # Voor ontwikkeling (inclusief test dependencies):
   pip install -r requirements/dev.txt
   ```

4. Download het Nederlandse SpaCy model:
   ```bash
   python -m spacy download nl_core_news_md
   ```

## Gebruik

### Command Line Interface

1. **Analyseren van tekst:**
   ```bash
   python main.py analyze "Jan de Vries woont in Amsterdam."
   ```

2. **Anonimiseren van tekst:**
   ```bash
   python main.py anonymize "Jan de Vries woont in Amsterdam."
   ```

3. **Verwerken van een bestand:**
   ```bash
   python main.py analyze pad/naar/bestand.txt
   python main.py anonymize pad/naar/bestand.txt
   ```

4. **Verwerken van een directory:**
   ```bash
   python main.py analyze pad/naar/directory
   python main.py anonymize pad/naar/directory
   ```

### REST API

1. **Start de API server:**
   ```bash
   # Installeer eerst de API dependencies:
   pip install -r requirements/api.txt

   # Start de server:
   uvicorn src.api.app:app --reload
   ```

2. **Bekijk de API documentatie:**
   Open `http://localhost:8000/docs` in je browser voor de interactieve Swagger documentatie.

3. **Gebruik de API:**
   ```bash
   # Analyseren van tekst
   curl -X POST "http://localhost:8000/api/v1/analyze" \
        -H "Content-Type: application/json" \
        -d '{"text": "Jan de Vries woont in Amsterdam."}'

   # Anonimiseren van tekst
   curl -X POST "http://localhost:8000/api/v1/anonymize" \
        -H "Content-Type: application/json" \
        -d '{"text": "Jan de Vries woont in Amsterdam."}'
   ```

   Zie [API Tutorial](docs/api_tutorial.md) voor meer voorbeelden en details.

### Output

- **Analyse output:**
  ```
  Analyseresultaten:
  Entiteit: PERSON, Tekst: 'Jan de Vries', Score: 0.85
  Entiteit: LOCATION, Tekst: 'Amsterdam', Score: 0.90
  ```

- **Anonimisatie output:**
  ```
  [NAAM] woont in [LOCATIE].
  ```

## Ontwikkeling

### Installeren van ontwikkelingsafhankelijkheden

```bash
pip install -r requirements/dev.txt
```

### Tests uitvoeren

```bash
# Alle tests
python -m pytest tests/

# Specifieke tests
python -m pytest tests/test_api.py -v  # API tests
python -m pytest tests/test_cli.py -v  # CLI tests
```

### Code kwaliteit

1. **Code formatteren met black:**
   ```bash
   black src/ tests/ main.py
   ```

2. **Type checking met mypy:**
   ```bash
   mypy src/ main.py
   ```

3. **Linting met flake8:**
   ```bash
   flake8 src/ tests/ main.py
   ```

## Bijdragen

Bijdragen zijn welkom! Volg deze stappen:

1. Fork de repository
2. Maak een nieuwe branch: `git checkout -b feature/mijn-feature`
3. Commit je wijzigingen: `git commit -am 'Voeg nieuwe feature toe'`
4. Push naar de branch: `git push origin feature/mijn-feature`
5. Open een Pull Request

## Licentie

Dit project is gelicenseerd onder de MIT License - zie het [LICENSE](LICENSE) bestand voor details.

## Contact

- Auteur: Menno West
- Email: menno.west@gmail.com
- GitHub: [MWest2020](https://github.com/MWest2020)