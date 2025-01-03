# CLI Reference

## Commando's

### Tekst Analyse

```bash
python -m main analyze "Dit is een test tekst met Jan de Vries"
```

**Opties:**
- `--entities`: Specifieke entiteiten om te detecteren (optioneel)

### Tekst Anonimisatie

```bash
python -m main anonymize "Dit is een test tekst met Jan de Vries"
```

**Opties:**
- `--entities`: Specifieke entiteiten om te anonimiseren (optioneel)

### PDF Verwerking

```bash
# Normale PDF
python -m main anonymize onverwerkt/document.pdf

# Gescande PDF met OCR
python -m main anonymize onverwerkt/scanned_document.pdf --ocr
```

**Opties:**
- `--entities`: Specifieke entiteiten om te anonimiseren (optioneel)
- `--ocr`: Gebruik OCR voor gescande PDFs (optioneel)
- `--output`: Aangepaste output locatie (optioneel, default: `verwerkt/[filename]_anon.pdf`)

## Voorbeelden

### Basis Gebruik

```bash
# Analyseer tekst
python -m main analyze "Jan de Vries woont in Amsterdam"

# Anonimiseer tekst
python -m main anonymize "Jan de Vries woont in Amsterdam"

# Verwerk PDF
python -m main anonymize onverwerkt/document.pdf
```

### Geavanceerd Gebruik

```bash
# Specifieke entiteiten
python -m main anonymize "Jan de Vries woont in Amsterdam" --entities PERSON LOCATION

# Gescande PDF met OCR
python -m main anonymize onverwerkt/scan.pdf --ocr

# Aangepaste output locatie
python -m main anonymize onverwerkt/document.pdf --output custom_output.pdf
```

## Vereisten

Voor OCR functionaliteit:
- Tesseract OCR met Nederlandse taaldata
- Poppler Utils voor PDF verwerking

### Windows Installatie

1. Installeer Tesseract OCR:
   - Download van [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Selecteer Nederlandse taaldata tijdens installatie

2. Installeer Poppler:
   - Download van [poppler releases](http://blog.alivate.com.au/poppler-windows/)
   - Pak uit naar een bekende locatie

3. Stel environment variables in:
   ```bash
   set TESSERACT_CMD="C:\Program Files\Tesseract-OCR\tesseract.exe"
   set POPPLER_PATH="C:\Program Files\poppler-24.02.0\Library\bin"
   ```

### Linux/macOS Installatie

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-nld poppler-utils

# macOS
brew install tesseract tesseract-lang poppler
``` 