# CLI Documentatie

## Basis Commando's

### 1. Tekst Analyse

```bash
# Directe tekst
python -m main analyze "Jan de Vries woont in Amsterdam"

# Bestand
python -m main analyze bestand.txt

# Specifieke entiteiten
python -m main analyze "Jan de Vries woont in Amsterdam" --entities PERSON LOCATION
```

### 2. Tekst Anonimisatie

```bash
# Directe tekst
python -m main anonymize "Jan de Vries woont in Amsterdam"

# Bestand
python -m main anonymize bestand.txt

# Specifieke entiteiten
python -m main anonymize "Jan de Vries woont in Amsterdam" --entities PERSON LOCATION
```

## Output Formaten

### Text (Standaard)
```bash
python -m main analyze "Jan de Vries woont in Amsterdam"
```
Output:
```
Gevonden entiteiten:
----------------------------------------
Type: PERSON
Text: Jan de Vries
Score: 0.98
----------------------------------------
Type: LOCATION
Text: Amsterdam
Score: 0.95
----------------------------------------
```

### JSON
```bash
python -m main analyze "Jan de Vries woont in Amsterdam" --format json
```
Output:
```json
{
  "results": [
    {
      "entity_type": "PERSON",
      "text": "Jan de Vries",
      "start": 0,
      "end": 12,
      "score": 0.98
    },
    {
      "entity_type": "LOCATION",
      "text": "Amsterdam",
      "start": 22,
      "end": 31,
      "score": 0.95
    }
  ]
}
```

## Ondersteunde Entiteiten

- `PERSON`: Namen van personen
- `LOCATION`: Locaties, adressen, plaatsnamen
- `PHONE_NUMBER`: Telefoonnummers
- `IBAN`: Nederlandse bankrekeningnummers
- `EMAIL`: Email adressen
- `ORGANIZATION`: Organisaties en bedrijven

## Bestandsverwerking

### Tekst Bestanden
- Automatische encoding detectie (UTF-8)
- Output in dezelfde directory als input
- Suffix `_anon` voor geanonimiseerde bestanden

### Batch Verwerking
Voor meerdere bestanden, gebruik een directory:
```bash
python -m main anonymize /pad/naar/directory
```

## Exit Codes

- `0`: Succes
- `1`: Error (details in stderr)

## Voorbeelden

1. **Analyseer een brief**
```bash
python -m main analyze brief.txt
```

2. **Anonimiseer met specifieke entiteiten**
```bash
python -m main anonymize brief.txt --entities PERSON IBAN PHONE_NUMBER
```

3. **JSON output naar bestand**
```bash
python -m main analyze brief.txt --format json > analyse.json
```

## Opmerkingen

1. **Performance**
   - Eerste run laadt modellen (~30s)
   - Volgende runs zijn sneller
   - Overweeg de API voor betere performance

2. **Beperkingen**
   - Geen PDF ondersteuning in CLI
   - Gebruik API voor PDF verwerking
   - Geen streaming voor grote bestanden 