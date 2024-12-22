# CLI Handleiding

Deze handleiding beschrijft het gebruik van de command-line interface (CLI) voor het analyseren en anonimiseren van Nederlandse tekst.

## Basis Gebruik

De CLI wordt aangeroepen via:

```bash
python main.py [command] [input]  # Vanuit de root directory
```

## Beschikbare Commando's

Er zijn twee hoofdcommando's beschikbaar:

### 1. Analyze

Het `analyze` commando analyseert tekst en toont gevonden entiteiten:

```bash
python main.py analyze [input]
```

Bijvoorbeeld:
```bash
# Analyseer directe tekst
python main.py analyze "Jan de Vries woont in Amsterdam"

# Analyseer een bestand
python main.py analyze path/naar/bestand.txt

# Analyseer alle .txt bestanden in een directory
python main.py analyze path/naar/directory
```

### 2. Anonymize

Het `anonymize` commando analyseert én anonimiseert de tekst:

```bash
python main.py anonymize [input]
```

Bijvoorbeeld:
```bash
# Anonimiseer directe tekst
python main.py anonymize "Jan de Vries woont in Amsterdam"

# Anonimiseer een bestand
python main.py anonymize path/naar/bestand.txt

# Anonimiseer alle .txt bestanden in een directory
python main.py anonymize path/naar/directory
```

Bij het anonimiseren van bestanden wordt de output opgeslagen in een `verwerkt` directory met de bestandsnaam `[originele_naam]_geanonimiseerd.txt`.

## Input Types

De CLI ondersteunt drie types input:

1. **Directe tekst**: Een tekst string tussen aanhalingstekens
2. **Bestand**: Pad naar een .txt bestand
3. **Directory**: Pad naar een directory (verwerkt alle .txt bestanden)

## Help Informatie

Voor meer informatie over de beschikbare opties:

```bash
python main.py --help           # Algemene help
python main.py analyze --help   # Help voor analyze commando
python main.py anonymize --help # Help voor anonymize commando
```

## Voorbeelden

### Analyse Voorbeeld

```bash
python main.py analyze "Jan de Vries woont in Amsterdam en zijn telefoonnummer is 06-12345678"
```

Output:
```
Analyseresultaten:
Entiteit: PERSON, Tekst: 'Jan de Vries', Score: 0.85
Entiteit: LOCATION, Tekst: 'Amsterdam', Score: 0.90
Entiteit: PHONE_NUMBER, Tekst: '06-12345678', Score: 0.95
```

### Anonimisatie Voorbeeld

```bash
python main.py anonymize "Jan de Vries woont in Amsterdam en zijn telefoonnummer is 06-12345678"
```

Output:
```
Analyseresultaten:
Entiteit: PERSON, Tekst: 'Jan de Vries', Score: 0.85
Entiteit: LOCATION, Tekst: 'Amsterdam', Score: 0.90
Entiteit: PHONE_NUMBER, Tekst: '06-12345678', Score: 0.95

Geanonimiseerde tekst:
[NAAM] woont in [LOCATIE] en zijn telefoonnummer is [TELEFOONNUMMER]
```

## Batch Verwerking

Voor het verwerken van meerdere bestanden:

1. Plaats alle .txt bestanden in een directory
2. Voer het commando uit op de directory:
   ```bash
   python main.py anonymize path/naar/directory
   ```
3. Geanonimiseerde bestanden worden opgeslagen in de `verwerkt` directory