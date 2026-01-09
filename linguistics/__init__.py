"""Linguistics module initialization."""

from .buckwalter import arabic_to_buckwalter, buckwalter_to_arabic
from .morphology import analyze_morphology, extract_lemma, extract_root
from .pos import tag_word

__all__ = [
    "arabic_to_buckwalter",
    "buckwalter_to_arabic",
    "extract_root",
    "extract_lemma",
    "analyze_morphology",
    "tag_word",
]
