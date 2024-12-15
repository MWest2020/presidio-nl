import argparse
from analyzer import analyze_text, anonymize_text

def analyze_command(text):
    """Voer analyse uit."""
    print("\nAnalyseresultaten:")
    analysis_results = analyze_text(text)
    for result in analysis_results:
        print(f"Entiteit: {result.entity_type}, Tekst: '{text[result.start:result.end]}', Score: {result.score:.2f}")

def analyze_and_anonymize_command(text):
    """Combineer analyse en anonimisatie."""
    # Eerst analyseren
    print("\nAnalyseresultaten:")
    analysis_results = analyze_text(text)
    for result in analysis_results:
        print(f"Entiteit: {result.entity_type}, Tekst: '{text[result.start:result.end]}', Score: {result.score:.2f}")

    # Daarna anonimiseren
    print("\nGeanonimiseerde tekst:")
    anonymized_text = anonymize_text(text)
    print(anonymized_text)

def main():
    parser = argparse.ArgumentParser(description="CLI-tool voor analyse en anonimisatie van Nederlandse tekst.")
    subparsers = parser.add_subparsers(dest="command", help="Beschikbare commando's")

    # Subcommando 'analyze' - alleen analyse
    analyze_parser = subparsers.add_parser("analyze", help="Analyseer de tekst")
    analyze_parser.add_argument("text", type=str, nargs='?', help="De tekst om te analyseren")

    # Subcommando 'anonymize' - analyseer en anonimiseer
    anonymize_parser = subparsers.add_parser("anonymize", help="Analyseer en anonimiseer de tekst")
    anonymize_parser.add_argument("text", type=str, nargs='?', help="De tekst om te analyseren en te anonimiseren")

    args = parser.parse_args()

    if args.command == "analyze":
        if args.text:
            analyze_command(args.text)
        else:
            parser.print_help()
    elif args.command == "anonymize":
        if args.text:
            analyze_and_anonymize_command(args.text)
        else:
            parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
