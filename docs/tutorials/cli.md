# CLI Tutorial

Deze tutorial leidt je stap voor stap door het gebruik van de Presidio-NL command-line interface.

## Voorbereiding

1. Installeer de vereiste packages:
   ```bash
   pip install -r requirements/base.txt
   ```

2. Test de installatie:
   ```bash
   python main.py analyze "Dit is een test"
   ```

## Basis Gebruik

### 1. Tekst Analyse

Laten we beginnen met het analyseren van een eenvoudige tekst:

```bash
python main.py analyze "Jan de Vries woont in Amsterdam"
```

Je zou output moeten zien zoals:
```
Gevonden entiteiten:
----------------------------------------
Type: PERSON
Text: Jan de Vries
Positie: 0-11
Score: 0.95
----------------------------------------
Type: LOCATION
Text: Amsterdam
Positie: 22-31
Score: 0.98
----------------------------------------
```

### 2. Tekst Anonimiseren

Nu gaan we dezelfde tekst anonimiseren:

```bash
python main.py anonymize "Jan de Vries woont in Amsterdam"
```

Output:
```
Originele tekst:
Jan de Vries woont in Amsterdam

Geanonimiseerde tekst:
[NAAM] woont in [LOCATIE]
```

## Geavanceerd Gebruik

### 1. Specifieke Entiteiten

Je kunt specificeren welke entiteiten je wilt detecteren:

```bash
python main.py analyze --entities PERSON LOCATION "Jan de Vries heeft 06-12345678"
```

Dit zal alleen personen en locaties detecteren, het telefoonnummer wordt genegeerd.

### 2. JSON Output

Voor programmatische verwerking, gebruik JSON output:

```bash
python main.py analyze --format json "Jan de Vries woont in Amsterdam"
```

### 3. Bestandsverwerking

1. Maak een tekstbestand `input.txt`:
   ```text
   Jan de Vries woont in Amsterdam.
   Hij heeft telefoonnummer 06-12345678.
   Zijn IBAN is NL91ABNA0417164300.
   ```

2. Analyseer het bestand:
   ```bash
   python main.py analyze --input-file input.txt --output-file analysis.json --format json
   ```

3. Anonimiseer het bestand:
   ```bash
   python main.py anonymize --input-file input.txt --output-file anonymous.txt
   ```

## Best Practices

1. **Gebruik JSON voor automatisering**
   ```bash
   python main.py analyze --format json | jq .
   ```

2. **Batch verwerking**
   ```bash
   # Verwerk alle .txt bestanden in een directory
   for f in *.txt; do
     python main.py anonymize --input-file "$f" --output-file "anon_$f"
   done
   ```

3. **Foutafhandeling**
   ```bash
   # Controleer exit code
   python main.py analyze "test" || echo "Error occurred"
   ```

## Volgende Stappen

- Bekijk de [CLI Reference](../reference/cli.md) voor alle opties
- Leer over de [API](api.md) voor server-based gebruik
- Zie de [Installation Guide](../guides/installation.md) voor deployment opties 