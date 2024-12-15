# Presidio x SpacyNLPEngine(NL): Nederlandse Tekst Anonimisatie

Dit open source project combineert [Microsoft Presidio](https://github.com/microsoft/presidio) met SpaCy en andere tools om Nederlandse tekst te analyseren en te anonimiseren. Het project biedt een krachtige CLI-tool voor het identificeren van gevoelige informatie zoals namen en locaties, en deze te anonimiseren.

## **Features**
- **Entiteitsanalyse:** Identificeer gevoelige informatie zoals persoonlijke namen en locaties.
- **Anonimisatie:** Vervang gevoelige informatie met een standaardwaarde zoals `[REDACTED]`.
- **Nederlandstalige ondersteuning:** Geoptimaliseerd voor Nederlandse teksten met behulp van SpaCy.
- **Uitbreidbaar:** Voeg eenvoudig nieuwe entiteitstypen en anonimisatie-opties toe.

## **Installatie**
1. Clone de repository:
   ```bash
   git clone https://github.com/MWest2020/Presidio-x-RobBERT
   cd Presidio-x-RobBERT
    ```

2. Installeer de benodigde Python-pakketten:
    ```bash
    pip install -r requirements.txt
    ```

3. Download het Nederlandse SpaCy-model:
    ```bash
    python -m spacy download nl_core_news_md
    ``` 

## Gebruik

Start de CLI-tool om een tekst te analyseren of te anonimiseren.

### Analyseren
Identificeer entiteiten in een tekst:

```bash
python cli.py analyze "Ik ben Menno en ik woon in Amsterdam."
```
### Anonimiseren

Anonimiseer gevoelige informatie in een tekst:
```bash
python cli.py anonymize "Ik ben Menno en ik woon in Amsterdam."
```

### Analyseren en Anonimiseren
Combineer beide functies:

```bash
python cli.py "Ik ben Menno en ik woon in Amsterdam."
```

## Documentatie

Voor meer uitleg over de werking van dit project, zie de [documentatie]() op Gitbook(todo).

## Bijdragen
Bijdragen zijn welkom! Open een issue of maak een pull request om verbeteringen voor te stellen.

## Roadmap

- Containeralisatie
- Helm chart
- Training model
- Context-vervangende placeholders