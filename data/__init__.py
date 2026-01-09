"""Data module initialization."""

from .normalizer import normalize_text
from .quranjson_loader import QuranJsonLoader
from .tokenizer import tokenize_ayah

__all__ = [
    "QuranJsonLoader",
    "normalize_text",
    "tokenize_ayah",
]
