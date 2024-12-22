#!/usr/bin/env python3
"""
Command-line interface voor Nederlandse tekst analyse en anonimisatie.
"""

from src.cli.main import CLI

def main():
    """Entry point voor de command-line interface."""
    cli = CLI()
    return cli.main()

if __name__ == "__main__":
    main() 