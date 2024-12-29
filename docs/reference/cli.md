# CLI Reference

Gedetailleerde documentatie van alle command-line opties en functionaliteit.

## Basis Gebruik

```bash
python main.py <command> [options] <text>
```

## Commands

### analyze
Analyseer tekst voor entiteiten (personen, locaties, etc.).

```bash
python main.py analyze "Jan de Vries woont in Amsterdam"
```

### anonymize
Anonimiseer tekst door gevonden entiteiten te vervangen.

```bash
python main.py anonymize "Jan de Vries woont in Amsterdam"
```

## Algemene Opties

### --format
Specificeer het output formaat.

```bash
--format {text|json}  Output formaat (standaard: text)
```

Voorbeeld JSON output:
```json
{
  "results": [
    {
      "entity_type": "PERSON",
      "text": "Jan de Vries",
      "start": 0,
      "end": 11,
      "score": 0.95
    }
  ]
}
```

### --entities
Specificeer welke entiteiten gedetecteerd moeten worden.

```bash
--entities PERSON LOCATION  # Alleen personen en locaties detecteren
```

Ondersteunde entiteiten:
- `PERSON`: Namen van personen
- `LOCATION`: Geografische locaties
- `PHONE_NUMBER`: Telefoonnummers
- `IBAN`: IBAN rekeningnummers

## Bestandsverwerking

### --input-file
Verwerk een tekstbestand in plaats van command-line input.

```bash
python main.py analyze --input-file input.txt
```

### --output-file
Schrijf de resultaten naar een bestand.

```bash
python main.py anonymize --input-file input.txt --output-file output.txt
```

## Voorbeelden

1. **Basis analyse:**
   ```bash
   python main.py analyze "Jan de Vries woont in Amsterdam"
   ```

2. **Specifieke entiteiten:**
   ```bash
   python main.py analyze --entities PERSON LOCATION "Jan de Vries woont in Amsterdam"
   ```

3. **JSON output:**
   ```bash
   python main.py analyze --format json "Jan de Vries woont in Amsterdam"
   ```

4. **Bestandsverwerking:**
   ```bash
   # Analyseer bestand
   python main.py analyze --input-file input.txt --output-file analysis.json --format json

   # Anonimiseer bestand
   python main.py anonymize --input-file input.txt --output-file anonymous.txt
   ```

5. **Combinatie van opties:**
   ```bash
   python main.py anonymize \
     --entities PERSON LOCATION \
     --format json \
     --input-file input.txt \
     --output-file output.json
   ```

## Exit Codes

- 0: Succesvol
- 1: Error (zie error message voor details)

## Foutafhandeling

De CLI geeft duidelijke foutmeldingen voor veel voorkomende problemen:

1. **Bestand niet gevonden:**
   ```
   Error: Bestand niet gevonden: input.txt
   ```

2. **Ongeldige entiteiten:**
   ```
   Error: Unsupported entities: EMAIL, IP
   ```

3. **Lege input:**
   ```
   Error: Text cannot be empty
   ``` 