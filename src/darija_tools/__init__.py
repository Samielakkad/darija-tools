"""darija-tools: small, honest NLP utilities for Moroccan Darija."""
from .arabizi import to_arabic, to_arabizi
from .normalize import normalize

__version__ = "0.2.0"
__all__ = ["__version__", "normalize", "to_arabic", "to_arabizi"]
