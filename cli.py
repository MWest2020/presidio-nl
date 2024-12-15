import argparse
from analyzer import analyze_text, anonymize_text

def analyze_command(text):
    """Voer analyse uit."""
    print("\nAnalyseresultaten:")
    analysis_results = analyze_text(text)
    for result in analysis_results:
        print(f"Entiteit: {result.entity_type}, Tekst: '{text[result.start:result.end]}', Score: {result.score:.2f}")

def anonymize_command(text):
    """Voer anonimisatie uit."""
    print("\nGeanonimiseerde tekst:")
    anonymized_text = anonymize_text(text)
    print(anonymized_text)

def main():
    parser = argparse.ArgumentParser(description="CLI-tool voor analyse en anonimisatie van Nederlandse tekst.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommando 'analyze'
    analyze_parser = subparsers.add_parser("analyze", help="Analyseer een tekst")
    analyze_parser.add_argument("text", type=str, help="De tekst om te analyseren")

    # Subcommando 'anonymize'
    anonymize_parser = subparsers.add_parser("anonymize", help="Anonimiseer een tekst")
    anonymize_parser.add_argument("text", type=str, help="De tekst om te anonimiseren")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args.text)
    elif args.command == "anonymize":
        anonymize_command(args.text)

if __name__ == "__main__":
    main()
