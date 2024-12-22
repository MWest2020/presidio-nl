# TODO List

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

## Taalniveau Analyse
- [ ] Implementeer taalniveau detectie:
  - [ ] Integratie met bestaande tools (bijv. Flesch-Douma)
  - [ ] Analyse van:
    - Zinslengte
    - Woordlengte
    - Woordfrequentie
    - Grammaticale complexiteit
  - [ ] Rapportage van CEFR niveau (A1-C2)

## Document Formaat Ondersteuning
- [ ] PDF ondersteuning:
  - [ ] PDF tekst extractie
  - [ ] Behoud van layout en formatting
  - [ ] Genereren van geanonimiseerde PDF
  - [ ] OCR ondersteuning voor gescande documenten

- [ ] DOCX ondersteuning:
  - [ ] DOCX tekst extractie
  - [ ] Behoud van formatting (bold, italic, etc.)
  - [ ] Genereren van geanonimiseerde DOCX
  - [ ] Behoud van headers, footers en andere document elementen

## Gebruikersinterface
- [ ] Ontwikkel UI voor anonimisatie visualisatie:
  - [ ] Web-based interface
  - [ ] Highlight van gedetecteerde entiteiten
  - [ ] Preview van anonimisatie resultaat
  - [ ] Mogelijkheid om entiteiten handmatig toe te voegen/verwijderen
  - [ ] Exporteren naar verschillende formaten

## Anonimisatie Opties
- [ ] Implementeer verschillende anonimisatie methodes:
  - [ ] Maskering (bijv. "XXXX" of "****")
  - [ ] Pseudonimisering (consistente vervanging)
  - [ ] Generalisatie (bijv. leeftijd naar leeftijdsgroep)
  - [ ] Randomisatie
  - [ ] k-anonimiteit ondersteuning
  - [ ] Configureerbare placeholder formats

## Toekomstige Verbeteringen
- [ ] Performance optimalisatie voor grote documenten
- [ ] Batch processing verbeteren
- [ ] API uitbreiden met nieuwe functionaliteit
- [ ] Betere error handling en logging
- [ ] Uitgebreidere test suite
- [ ] Documentatie verbeteren 