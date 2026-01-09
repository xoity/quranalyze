"""
Text tokenization utilities for Arabic text.

This module provides functions to tokenize Arabic text into words
using deterministic rules.
"""

from typing import Final

from ..config import WORD_DELIMITER
from ..exceptions import TokenizationError


# Characters to strip from word boundaries
BOUNDARY_CHARS: Final[str] = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~؟،"


def tokenize_ayah(ayah_text: str, delimiter: str = WORD_DELIMITER) -> list[str]:
    """
    Tokenize an ayah text into individual words.
    
    This function uses a simple whitespace-based tokenization approach.
    It splits text by the specified delimiter and strips boundary characters.
    
    Args:
        ayah_text: The ayah text to tokenize
        delimiter: The delimiter to use for splitting (default: space)
        
    Returns:
        List of tokenized words in order
        
    Raises:
        TokenizationError: If tokenization fails
    """
    if not ayah_text:
        return []
    
    try:
        # Split by delimiter
        tokens = ayah_text.split(delimiter)
        
        # Strip boundary characters and filter empty tokens
        words = []
        for token in tokens:
            word = token.strip(BOUNDARY_CHARS)
            if word:  # Only keep non-empty tokens
                words.append(word)
        
        return words
    except Exception as e:
        raise TokenizationError(f"Failed to tokenize ayah: {e}") from e


def tokenize_with_positions(ayah_text: str, delimiter: str = WORD_DELIMITER) -> list[tuple[str, int]]:
    """
    Tokenize an ayah text and return words with their positions.
    
    Args:
        ayah_text: The ayah text to tokenize
        delimiter: The delimiter to use for splitting (default: space)
        
    Returns:
        List of (word, position) tuples
        
    Raises:
        TokenizationError: If tokenization fails
    """
    try:
        words = tokenize_ayah(ayah_text, delimiter)
        return [(word, i) for i, word in enumerate(words)]
    except Exception as e:
        raise TokenizationError(f"Failed to tokenize with positions: {e}") from e


def count_words(text: str, delimiter: str = WORD_DELIMITER) -> int:
    """
    Count the number of words in a text.
    
    Args:
        text: The text to count words in
        delimiter: The delimiter to use for splitting (default: space)
        
    Returns:
        Number of words
        
    Raises:
        TokenizationError: If counting fails
    """
    try:
        return len(tokenize_ayah(text, delimiter))
    except Exception as e:
        raise TokenizationError(f"Failed to count words: {e}") from e
