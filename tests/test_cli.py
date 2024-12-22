import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.cli.main import CLI

@pytest.fixture
def cli():
    return CLI()

@pytest.fixture
def mock_text_file(tmp_path):
    """Create a temporary text file for testing."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Jan de Vries woont in Amsterdam.", encoding='utf-8')
    return test_file

@pytest.fixture
def mock_directory(tmp_path):
    """Create a temporary directory with test files."""
    # Create test files
    (tmp_path / "test1.txt").write_text("Text 1", encoding='utf-8')
    (tmp_path / "test2.txt").write_text("Text 2", encoding='utf-8')
    (tmp_path / "not_a_text.doc").write_text("Not a text file", encoding='utf-8')
    return tmp_path

def test_cli_initialization(cli):
    """Test if CLI initializes correctly."""
    assert cli is not None
    assert cli.analyzer is not None
    assert cli.anonymizer is not None

def test_analyze_text(cli, capsys):
    """Test analyzing text directly."""
    text = "Jan de Vries woont in Amsterdam."
    cli.analyze_text(text)
    
    captured = capsys.readouterr()
    assert "Analyseresultaten:" in captured.out
    assert "Jan de Vries" in captured.out
    assert "Amsterdam" in captured.out

def test_anonymize_text(cli, capsys, tmp_path):
    """Test anonymizing text."""
    text = "Jan de Vries woont in Amsterdam."
    output_path = tmp_path / "output.txt"
    
    cli.anonymize_text(text, output_path)
    
    # Check console output
    captured = capsys.readouterr()
    assert "Analyseresultaten:" in captured.out
    assert "Geanonimiseerde tekst:" in captured.out
    
    # Check file output if path was provided
    if output_path.exists():
        content = output_path.read_text(encoding='utf-8')
        assert "[NAAM]" in content
        assert "[LOCATIE]" in content
        assert "Jan de Vries" not in content
        assert "Amsterdam" not in content

def test_process_file(cli, mock_text_file, capsys):
    """Test processing a single file."""
    cli.process_file(mock_text_file, "analyze")
    
    captured = capsys.readouterr()
    assert "Analyseresultaten:" in captured.out
    assert "Jan de Vries" in captured.out
    assert "Amsterdam" in captured.out

def test_process_directory(cli, mock_directory, capsys):
    """Test processing a directory."""
    cli.process_directory(mock_directory, "analyze")
    
    captured = capsys.readouterr()
    assert "Analyseresultaten:" in captured.out
    assert "test1.txt" in captured.out
    assert "test2.txt" in captured.out

def test_process_directory_no_txt_files(cli, tmp_path, capsys):
    """Test processing a directory with no txt files."""
    cli.process_directory(tmp_path, "analyze")
    
    captured = capsys.readouterr()
    assert "Geen .txt-bestanden gevonden" in captured.out

@patch('argparse.ArgumentParser.parse_args')
def test_main_with_file(mock_args, cli, mock_text_file):
    """Test main function with file input."""
    mock_args.return_value = MagicMock(
        command="analyze",
        path=str(mock_text_file)
    )
    
    result = cli.main()
    assert result == 0

@patch('argparse.ArgumentParser.parse_args')
def test_main_with_directory(mock_args, cli, mock_directory):
    """Test main function with directory input."""
    mock_args.return_value = MagicMock(
        command="analyze",
        path=str(mock_directory)
    )
    
    result = cli.main()
    assert result == 0

@patch('argparse.ArgumentParser.parse_args')
def test_main_with_direct_text(mock_args, cli):
    """Test main function with direct text input."""
    mock_args.return_value = MagicMock(
        command="analyze",
        path="Jan de Vries woont in Amsterdam."
    )
    
    result = cli.main()
    assert result == 0 