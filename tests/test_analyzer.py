import pytest
import time
import psutil
import os
from pathlib import Path
from src.core.analyzer import DutchTextAnalyzer
from pdfminer.pdfdocument import PdfReader

@pytest.fixture
def analyzer():
    return DutchTextAnalyzer()

def test_analyzer_initialization(analyzer):
    """Test if analyzer initializes correctly."""
    assert analyzer is not None
    assert analyzer.default_entities == [
        "PERSON",
        "LOCATION",
        "PHONE_NUMBER",
        "IBAN"
    ]

def test_analyze_text_with_person(analyzer):
    """Test if analyzer can detect person names."""
    text = "Jan de Vries woont in Amsterdam."
    results = analyzer.analyze_text(text)
    
    # Check if we found at least one person
    person_results = [r for r in results if r.entity_type == "PERSON"]
    assert len(person_results) > 0
    assert "Jan de Vries" in text[person_results[0].start:person_results[0].end]

def test_analyze_text_with_location(analyzer):
    """Test if analyzer can detect locations."""
    text = "Jan de Vries woont in Amsterdam."
    results = analyzer.analyze_text(text)
    
    # Check if we found the location
    location_results = [r for r in results if r.entity_type == "LOCATION"]
    assert len(location_results) > 0
    assert "Amsterdam" in text[location_results[0].start:location_results[0].end]

def test_analyze_text_with_phone_number(analyzer):
    """Test if analyzer can detect phone numbers."""
    text = "Mijn telefoonnummer is 06-12345678"
    results = analyzer.analyze_text(text)
    
    # Check if we found the phone number
    phone_results = [r for r in results if r.entity_type == "PHONE_NUMBER"]
    assert len(phone_results) > 0
    assert "06-12345678" in text[phone_results[0].start:phone_results[0].end]

def test_analyze_text_with_iban(analyzer):
    """Test if analyzer can detect IBAN numbers."""
    text = "Mijn rekeningnummer is NL91ABNA0417164300"
    results = analyzer.analyze_text(text)
    
    # Check if we found the IBAN
    iban_results = [r for r in results if r.entity_type == "IBAN"]
    assert len(iban_results) > 0
    assert "NL91ABNA0417164300" in text[iban_results[0].start:iban_results[0].end]

def test_analyze_text_with_custom_entities(analyzer):
    """Test if analyzer works with custom entity list."""
    text = "Jan de Vries woont in Amsterdam."
    results = analyzer.analyze_text(text, entities=["PERSON"])
    
    # Should only find person, not location
    assert all(r.entity_type == "PERSON" for r in results)
    assert not any(r.entity_type == "LOCATION" for r in results)

def test_robbert_recognition():
    """Test RobBERT NER recognition."""
    analyzer = DutchTextAnalyzer()
    
    # Test tekst met verschillende entiteiten
    text = "Minister Rutte sprak gisteren in Den Haag met vertegenwoordigers van Shell over klimaatverandering."
    
    results = analyzer.analyze_text(text)
    
    # Converteer resultaten naar dict voor makkelijke verificatie
    found_entities = {
        text[r.start:r.end]: r.entity_type
        for r in results
    }
    
    # Verificatie van RobBERT resultaten
    assert "Rutte" in found_entities
    assert found_entities["Rutte"] == "PERSON"
    assert "Den Haag" in found_entities
    assert found_entities["Den Haag"] == "LOCATION"
    assert "Shell" in found_entities
    assert found_entities["Shell"] == "ORGANIZATION"

def test_robbert_complex_names():
    """Test RobBERT met complexe Nederlandse namen."""
    analyzer = DutchTextAnalyzer()
    text = "Minister-president Rutte sprak met burgemeester Van der Laan over Amsterdam-Zuid."
    
    results = analyzer.analyze_text(text)
    found_entities = {text[r.start:r.end]: r.entity_type for r in results}
    
    assert "Rutte" in found_entities
    assert found_entities["Rutte"] == "PERSON"
    assert "Van der Laan" in found_entities
    assert found_entities["Van der Laan"] == "PERSON"
    assert "Amsterdam-Zuid" in found_entities
    assert found_entities["Amsterdam-Zuid"] == "LOCATION"

def test_robbert_organizations():
    """Test RobBERT met organisaties in context."""
    analyzer = DutchTextAnalyzer()
    text = "De directeur van Shell Nederland en ABN AMRO Bank tekenden het contract."
    
    results = analyzer.analyze_text(text)
    found_entities = {text[r.start:r.end]: r.entity_type for r in results}
    
    assert "Shell Nederland" in found_entities
    assert found_entities["Shell Nederland"] == "ORGANIZATION"
    assert "ABN AMRO Bank" in found_entities
    assert found_entities["ABN AMRO Bank"] == "ORGANIZATION"

def test_mixed_language():
    """Test met gemengde talen (NL/EN)."""
    analyzer = DutchTextAnalyzer()
    text = "John Smith van Apple Inc. sprak met Pieter de Vries van Shell Nederland."
    
    results = analyzer.analyze_text(text)
    found_entities = {text[r.start:r.end]: r.entity_type for r in results}
    
    assert "John Smith" in found_entities
    assert found_entities["John Smith"] == "PERSON"
    assert "Pieter de Vries" in found_entities
    assert found_entities["Pieter de Vries"] == "PERSON"
    assert "Apple Inc." in found_entities
    assert found_entities["Apple Inc."] == "ORGANIZATION"
    assert "Shell Nederland" in found_entities
    assert found_entities["Shell Nederland"] == "ORGANIZATION"

def test_formal_titles():
    """Test met formele titels en aanhef."""
    analyzer = DutchTextAnalyzer()
    text = "Hoogedelgestrenge heer prof. dr. ir. Van der Berg sprak met mevrouw drs. De Vries."
    
    results = analyzer.analyze_text(text)
    found_entities = {text[r.start:r.end]: r.entity_type for r in results}
    
    assert any("Van der Berg" in entity for entity in found_entities.keys())
    assert any("De Vries" in entity for entity in found_entities.keys())

def test_large_text_performance():
    """Test performance met grote tekst."""
    analyzer = DutchTextAnalyzer()
    # Genereer ~100KB tekst
    base_text = "Jan de Vries woont in Amsterdam. Hij werkt bij Shell. "
    large_text = base_text * 1000
    
    start_time = time.time()
    results = analyzer.analyze_text(large_text)
    processing_time = time.time() - start_time
    
    # Verwerking moet binnen redelijke tijd (10 sec)
    assert processing_time < 10.0
    # Moet entiteiten vinden
    assert len(results) > 0

def test_memory_usage():
    """Test memory gebruik tijdens verwerking."""
    analyzer = DutchTextAnalyzer()
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Verwerk 50 teksten
    text = "Jan de Vries woont in Amsterdam. Hij werkt bij Shell."
    for _ in range(50):
        analyzer.analyze_text(text)
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    # Memory gebruik mag niet significant stijgen (<100MB)
    assert memory_increase < 100

def test_pdf_processing(tmp_path):
    """Test basis PDF verwerking."""
    from src.core.pdf import process_pdf
    
    # Maak test PDF
    test_pdf = tmp_path / "test.pdf"
    output_pdf = tmp_path / "output.pdf"
    
    # TODO: Implementeer PDF creatie en test
    # Voor nu skippen we deze test
    pytest.skip("PDF test nog implementeren")

def test_real_text_files(analyzer):
    """Test met echte voorbeeldteksten uit onverwerkt directory."""
    # Test tekst1.txt
    with open("onverwerkt/tekst1.txt", "r", encoding="utf-8") as f:
        text1 = f.read()
    
    results1 = analyzer.analyze_text(text1)
    found_entities1 = {text1[r.start:r.end]: r.entity_type for r in results1}
    
    # Verificatie tekst1.txt
    assert "Jan de Vries" in found_entities1
    assert found_entities1["Jan de Vries"] == "PERSON"
    assert "Utrecht" in found_entities1
    assert found_entities1["Utrecht"] == "LOCATION"
    # Straatnaam kan gedeeltelijk herkend worden
    assert any("Oude" in entity for entity in found_entities1.keys())
    assert found_entities1["NL91ABNA0417164300"] == "IBAN"
    assert found_entities1["06-12345678"] == "PHONE_NUMBER"
    
    # Test tekst2.txt
    with open("onverwerkt/tekst2.txt", "r", encoding="utf-8") as f:
        text2 = f.read()
    
    results2 = analyzer.analyze_text(text2)
    found_entities2 = {text2[r.start:r.end]: r.entity_type for r in results2}
    
    # Verificatie tekst2.txt
    assert "Sophie van Dijk" in found_entities2
    assert found_entities2["Sophie van Dijk"] == "PERSON"
    assert "Rotterdam" in found_entities2
    assert found_entities2["Rotterdam"] == "LOCATION"
    assert "Erasmusbrug" in found_entities2
    assert found_entities2["Erasmusbrug"] == "LOCATION"
    assert found_entities2["NL91ABNA0987654321"] == "IBAN"
    assert found_entities2["06-98765432"] == "PHONE_NUMBER"
    assert "Maas" in found_entities2
    assert found_entities2["Maas"] == "LOCATION"

def test_real_pdf_files(analyzer):
    """Test met echte PDF bestanden uit onverwerkt directory."""
    from src.core.document import extract_text_from_pdf
    
    # Test alle PDF bestanden
    pdf_files = ["test.pdf", "test2.pdf", "test3.pdf"]
    
    for pdf_file in pdf_files:
        # Lees PDF
        pdf_path = f"onverwerkt/{pdf_file}"
        text = extract_text_from_pdf(pdf_path)
        
        # Analyseer tekst
        results = analyzer.analyze_text(text)
        
        # Basis verificatie
        assert len(results) > 0, f"Geen entiteiten gevonden in {pdf_file}"
        
        # Check of we tenminste één van elk type entiteit hebben
        entity_types = {r.entity_type for r in results}
        assert len(entity_types) >= 2, f"Te weinig verschillende entiteiten in {pdf_file}"
        
        # Print gevonden entiteiten voor debug
        print(f"\nEntiteiten in {pdf_file}:")
        for r in results:
            print(f"{r.entity_type}: {text[r.start:r.end]} (score: {r.score:.2f})")

def test_pdf_text_extraction(tmp_path):
    """Test PDF text extractie voor zowel normale als gescande PDFs."""
    from src.core.document import extract_text_from_pdf
    
    # Test normale PDF
    normal_pdf_path = "onverwerkt/test.pdf"
    text = extract_text_from_pdf(normal_pdf_path)
    assert text.strip(), "Geen tekst geëxtraheerd uit normale PDF"
    
    # Test gescande PDF
    scanned_pdf_path = "onverwerkt/visa_application.pdf"
    text = extract_text_from_pdf(scanned_pdf_path)
    assert text.strip(), "Geen tekst geëxtraheerd uit gescande PDF"
    
    # Verifieer dat OCR wordt gebruikt voor gescande PDFs
    with open(scanned_pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        direct_text = pdf_reader.pages[0].extract_text()
    
    # Als direct_text leeg is maar extract_text_from_pdf wel tekst geeft,
    # dan weten we dat OCR succesvol was
    if not direct_text.strip():
        assert text.strip(), "OCR extractie gefaald voor gescande PDF"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])