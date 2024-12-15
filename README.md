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


## Roadmap

- Containeralisaite
- Helm chart
- Training model
- Context-vervangende placeholders