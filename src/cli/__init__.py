"""CLI package for text analysis and anonymization."""
from .cli import main
from .commands import CommandHandler

__all__ = ["main", "CommandHandler"] 