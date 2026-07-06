"""darija-tools: small, honest NLP utilities for Moroccan Darija."""
from .arabizi import to_arabic
from .normalize import normalize

__version__ = "0.1.0"
__all__ = ["normalize", "to_arabic", "__version__"]
