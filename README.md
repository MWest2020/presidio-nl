# Presidio-NL: Nederlandse Tekst Anonimisatie

Dit open source project combineert [Microsoft Presidio](https://github.com/microsoft/presidio) met SpaCy voor het analyseren en anonimiseren van Nederlandse tekst. Het project biedt een krachtige CLI-tool voor het identificeren en anonimiseren van gevoelige informatie zoals namen, locaties, telefoonnummers en IBAN-nummers.

## Features
- **Entiteitsanalyse:** Identificeer gevoelige informatie zoals:
  - Persoonlijke namen
  - Locaties
  - Telefoonnummers
  - IBAN-nummers
- **Anonimisatie:** Vervang gevoelige informatie met configureerbare placeholders
- **Nederlandstalige ondersteuning:** Geoptimaliseerd voor Nederlandse teksten met SpaCy
- **Uitbreidbaar:** Eenvoudig nieuwe entiteitstypen en anonimisatie-opties toevoegen
- **Type-safe:** Volledig voorzien van type hints
- **Goed getest:** Uitgebreide test suite met pytest

## Projectstructuur
```
presidio-nl/
├── src/
│   ├── analyzer/          # Tekstanalyse functionaliteit
│   ├── anonymizer/        # Anonimisatie functionaliteit
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
   pip install -r requirements/base.txt
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
python -m pytest tests/
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