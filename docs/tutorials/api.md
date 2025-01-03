# API Tutorial

Deze tutorial legt stap voor stap uit hoe je de API kunt gebruiken om documenten te anonimiseren.

## Inhoudsopgave
1. [Voorbereiding](#voorbereiding)
2. [Tekst Anonimiseren](#tekst-anonimiseren)
3. [PDF Bestanden Verwerken](#pdf-bestanden-verwerken)
4. [Gescande PDFs Verwerken](#gescande-pdfs-verwerken)
5. [Veelgestelde Vragen](#veelgestelde-vragen)

## Voorbereiding

De API draait standaard op `http://localhost:8000`. Zorg dat de server actief is met:

```bash
docker run -p 8000:8000 presidio-nl
```

Om de voorbeelden te volgen heb je nodig:
- Een terminal (bijv. PowerShell of Command Prompt op Windows)
- cURL (standaard aanwezig op Linux/macOS, [download voor Windows](https://curl.se/windows/))
- Een teksteditor voor het opslaan van de geanonimiseerde PDFs

## Tekst Anonimiseren

### Voorbeeld 1: Simpele tekst

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/text" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"Jan de Vries woont in Amsterdam\"}"
```

Je krijgt een response zoals:
```json
{
    "original_text": "Jan de Vries woont in Amsterdam",
    "anonymized_text": "<PERSON> woont in <LOCATION>",
    "entities_found": [
        {
            "entity_type": "PERSON",
            "text": "Jan de Vries",
            "score": 0.95
        },
        {
            "entity_type": "LOCATION",
            "text": "Amsterdam",
            "score": 0.92
        }
    ]
}
```

### Voorbeeld 2: Specifieke entiteiten

Als je alleen bepaalde gegevens wilt anonimiseren:

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/text" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"Jan de Vries woont in Amsterdam\", \"entities\": [\"PERSON\"]}"
```

Nu wordt alleen de naam geanonimiseerd:
```json
{
    "anonymized_text": "<PERSON> woont in Amsterdam"
}
```

## PDF Bestanden Verwerken

### Voorbeeld 3: PDF Document

Om een PDF te verwerken:

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/pdf" ^
  -F "file=@C:\Users\JandeVries\Documents\document.pdf" ^
  -o geanonimiseerd.pdf
```

Let op:
- Vervang het pad (`C:\Users\...`) met het pad naar jouw PDF
- De `-o geanonimiseerd.pdf` zorgt dat het resultaat wordt opgeslagen

### Voorbeeld 4: PDF met Specifieke Entiteiten

Als je alleen bepaalde gegevens in de PDF wilt anonimiseren:

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/pdf?entities=PERSON,LOCATION" ^
  -F "file=@document.pdf" ^
  -o geanonimiseerd.pdf
```

## Gescande PDFs Verwerken

Voor gescande documenten moet je OCR (tekstherkenning) activeren:

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/pdf?use_ocr=true" ^
  -F "file=@gescand_document.pdf" ^
  -o geanonimiseerd.pdf
```

De OCR zal:
1. De gescande tekst herkennen
2. PII (persoonlijke informatie) detecteren
3. Deze informatie anonimiseren
4. Een nieuwe PDF genereren

## Veelgestelde Vragen

### Welke gegevens worden herkend?
- PERSON: Namen van personen
- LOCATION: Plaatsnamen, adressen
- ORGANIZATION: Bedrijven, instanties
- PHONE_NUMBER: Telefoonnummers
- EMAIL: E-mailadressen
- IBAN: Bankrekeningnummers

### Wat als er geen gegevens worden gevonden?
Dan krijg je een bericht dat er geen PII is gevonden en blijft het document ongewijzigd.

### Hoe weet ik of de OCR goed heeft gewerkt?
De API geeft in de response aan hoeveel woorden zijn herkend en welke gegevens zijn gevonden.

### Kan ik zien welke gegevens zijn geanonimiseerd?
Ja, de API geeft een lijst van gevonden entiteiten met hun type en betrouwbaarheidsscore.

### Wat betekenen de scores?
- 0.9-1.0: Zeer betrouwbaar
- 0.7-0.9: Waarschijnlijk correct
- <0.7: Mogelijk incorrect

### Hoe kan ik het resultaat controleren?
Open de geanonimiseerde PDF en controleer of:
1. Alle gevoelige informatie is vervangen
2. De layout behouden is gebleven
3. De tekst nog leesbaar is 