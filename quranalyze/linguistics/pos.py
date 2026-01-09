"""
Part-of-speech tagging placeholder.

This module provides placeholders for POS tagging capabilities.
POS tagging would require trained models or annotated datasets.
"""

from typing import Optional

from ..core.word import Word


# POS tag types (for future implementation)
POS_TAGS = {
    "NOUN": "Noun",
    "VERB": "Verb",
    "ADJ": "Adjective",
    "ADV": "Adverb",
    "PRON": "Pronoun",
    "DET": "Determiner",
    "ADP": "Adposition",
    "CONJ": "Conjunction",
    "PART": "Particle",
    "NUM": "Numeral",
    "PUNCT": "Punctuation",
    "X": "Other",
}


def tag_word(word: Word) -> Optional[str]:
    """
    Assign a part-of-speech tag to a word.
    
    This is a placeholder function. Actual POS tagging would require:
    - Pre-trained POS tagging model
    - Annotated corpus for training
    - Feature extraction for Arabic morphology
    
    Args:
        word: The Word object to tag
        
    Returns:
        POS tag string, or None if unavailable
        
    Note:
        This foundation version returns None. Future implementations
        could integrate with POS tagging tools like Stanford NLP,
        MADAMIRA, or custom trained models.
    """
    # Placeholder - not implemented
    return None


def tag_ayah(words: list[Word]) -> list[tuple[Word, Optional[str]]]:
    """
    Tag all words in an ayah with POS tags.
    
    This is a placeholder function. Actual tagging would consider:
    - Context of surrounding words
    - Syntactic patterns
    - Morphological features
    
    Args:
        words: List of Word objects from an ayah
        
    Returns:
        List of (Word, tag) tuples
        
    Note:
        This foundation version returns None for all tags.
    """
    return [(word, None) for word in words]


def get_pos_distribution(words: list[Word]) -> dict[str, int]:
    """
    Calculate distribution of POS tags in a word list.
    
    Args:
        words: List of Word objects
        
    Returns:
        Dictionary mapping POS tags to counts
        
    Note:
        This foundation version returns an empty distribution since
        POS tagging is not yet implemented.
    """
    # Placeholder - returns empty in this version
    return {}
