# TODO List

## Refactoring Prioriteiten
- [ ] Verwijder ongebruikte code en endpoints
- [ ] Consolideer PDF verwerking logica
- [ ] Vereenvoudig CLI interface
- [ ] Verbeter error handling en logging
- [ ] Optimaliseer model loading en caching

## Entiteit Verfijning
- [ ] Locatie opsplitsen in specifiekere entiteiten:
  - [ ] Plaatsnaam
  - [ ] Straatnaam
  - [ ] Huisnummer
  - [ ] Postcode
  - [ ] Land
  - Onderzoek:
    - SpaCy NER training voor Nederlandse adressen
    - Mogelijk gebruik van postcode/adres databases
    - Integratie met OpenStreetMap data

## Document Formaat Ondersteuning
- [x] PDF ondersteuning:
  - [x] PDF tekst extractie
  - [x] Behoud van layout en formatting
  - [x] Genereren van geanonimiseerde PDF
  - [ ] OCR ondersteuning voor gescande documenten

- [ ] DOCX ondersteuning:
  - [ ] DOCX tekst extractie
  - [ ] Behoud van formatting
  - [ ] Genereren van geanonimiseerde DOCX

## API & CLI Verbeteringen
- [x] Basis API endpoints voor tekst analyse
- [x] Basis API endpoints voor PDF verwerking
- [x] Vereenvoudigde CLI commando's
- [x] Documentatie voor API en CLI
- [ ] Performance optimalisatie voor grote documenten
- [ ] Betere error handling en logging
- [ ] Uitgebreidere test suite

## Toekomstig Project: Taalniveau Analyse
- [ ] Implementeer taalniveau detectie:
  - [ ] Integratie met bestaande tools (bijv. Flesch-Douma)
  - [ ] Analyse van:
    - Zinslengte
    - Woordlengte
    - Woordfrequentie
    - Grammaticale complexiteit
  - [ ] Rapportage van CEFR niveau (A1-C2)
  - [ ] API endpoint voor taalniveau analyse
  - [ ] CLI commando voor taalniveau analyse
  - [ ] Integratie met bestaande tekst analyse flow

## Toekomstig Project: Anonimisatie Methodes
- [ ] Implementeer configureerbare anonimisatie:
  - [ ] Context vervanging (huidige methode)
  - [ ] Maskering (bijv. "XXXX" of "****")
  - [ ] Pseudonimisering (consistente vervanging)
  - [ ] Generalisatie (bijv. leeftijd naar leeftijdsgroep)
  - [ ] Configureerbare placeholder formats
  - [ ] API endpoint voor anonimisatie methode selectie
  - [ ] CLI opties voor anonimisatie methode

## Te Verwijderen Features
- [ ] Complexe UI features (focus op API/CLI)
- [ ] k-anonimiteit (buiten scope)

## Performance Verbeteringen
- [ ] CLI performance verbeteren door model caching
  - Modellen (SpaCy en RobBERT) worden nu elke keer opnieuw geladen
  - Implementeer een daemon/service aanpak zoals in de API
  - Overweeg een "warm" proces dat modellen in geheugen houdt 