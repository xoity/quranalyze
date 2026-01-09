"""
Text normalization utilities for Arabic text.

This module provides functions to normalize Arabic text by handling
diacritics, character variations, and other text preprocessing needs.
"""

from typing import Final

from ..exceptions import NormalizationError


# Arabic character definitions
ARABIC_DIACRITICS: Final[str] = (
    "\u064B"  # Fathatan
    "\u064C"  # Dammatan
    "\u064D"  # Kasratan
    "\u064E"  # Fatha
    "\u064F"  # Damma
    "\u0650"  # Kasra
    "\u0651"  # Shadda
    "\u0652"  # Sukun
    "\u0653"  # Maddah
    "\u0654"  # Hamza above
    "\u0655"  # Hamza below
    "\u0656"  # Subscript alef
    "\u0657"  # Inverted damma
    "\u0658"  # Mark noon ghunna
    "\u0670"  # Superscript alef
)

# Hamza variations
HAMZA_FORMS: Final[dict[str, str]] = {
    "\u0623": "\u0627",  # Alef with hamza above -> Alef
    "\u0625": "\u0627",  # Alef with hamza below -> Alef
    "\u0622": "\u0627",  # Alef with madda -> Alef
    "\u0624": "\u0648",  # Waw with hamza -> Waw
    "\u0626": "\u064A",  # Yeh with hamza -> Yeh
}

# Alef variations
ALEF_FORMS: Final[dict[str, str]] = {
    "\u0623": "\u0627",  # Alef with hamza above -> Alef
    "\u0625": "\u0627",  # Alef with hamza below -> Alef
    "\u0622": "\u0627",  # Alef with madda -> Alef
    "\u0671": "\u0627",  # Alef wasla -> Alef
}

# Taa marbuta variation
TAA_MARBUTA: Final[str] = "\u0629"
TAA: Final[str] = "\u0647"  # Heh


def remove_diacritics(text: str) -> str:
    """
    Remove all Arabic diacritical marks from text.
    
    Args:
        text: Arabic text potentially containing diacritics
        
    Returns:
        Text with all diacritics removed
        
    Raises:
        NormalizationError: If text processing fails
    """
    try:
        for diacritic in ARABIC_DIACRITICS:
            text = text.replace(diacritic, "")
        return text
    except Exception as e:
        raise NormalizationError(f"Failed to remove diacritics: {e}") from e


def normalize_hamza(text: str) -> str:
    """
    Normalize all hamza variations to their base forms.
    
    Args:
        text: Arabic text with hamza variations
        
    Returns:
        Text with normalized hamza forms
        
    Raises:
        NormalizationError: If text processing fails
    """
    try:
        for original, normalized in HAMZA_FORMS.items():
            text = text.replace(original, normalized)
        return text
    except Exception as e:
        raise NormalizationError(f"Failed to normalize hamza: {e}") from e


def normalize_alef(text: str) -> str:
    """
    Normalize all alef variations to base alef.
    
    Args:
        text: Arabic text with alef variations
        
    Returns:
        Text with normalized alef forms
        
    Raises:
        NormalizationError: If text processing fails
    """
    try:
        for original, normalized in ALEF_FORMS.items():
            text = text.replace(original, normalized)
        return text
    except Exception as e:
        raise NormalizationError(f"Failed to normalize alef: {e}") from e


def normalize_taa_marbuta(text: str) -> str:
    """
    Normalize taa marbuta to regular heh.
    
    Args:
        text: Arabic text potentially containing taa marbuta
        
    Returns:
        Text with taa marbuta normalized to heh
        
    Raises:
        NormalizationError: If text processing fails
    """
    try:
        return text.replace(TAA_MARBUTA, TAA)
    except Exception as e:
        raise NormalizationError(f"Failed to normalize taa marbuta: {e}") from e


def normalize_text(
    text: str,
    remove_diacritics_flag: bool = True,
    normalize_hamza_flag: bool = True,
    normalize_alef_flag: bool = True,
    normalize_taa_marbuta_flag: bool = True,
) -> str:
    """
    Apply full normalization pipeline to Arabic text.
    
    This function applies various normalization operations in sequence
    to standardize Arabic text for analysis.
    
    Args:
        text: Original Arabic text
        remove_diacritics_flag: Whether to remove diacritical marks
        normalize_hamza_flag: Whether to normalize hamza variations
        normalize_alef_flag: Whether to normalize alef variations
        normalize_taa_marbuta_flag: Whether to normalize taa marbuta
        
    Returns:
        Fully normalized text
        
    Raises:
        NormalizationError: If any normalization step fails
    """
    if not text:
        return text
    
    try:
        # Remove diacritics first
        if remove_diacritics_flag:
            text = remove_diacritics(text)
        
        # Normalize character forms
        if normalize_hamza_flag:
            text = normalize_hamza(text)
        if normalize_alef_flag:
            text = normalize_alef(text)
        if normalize_taa_marbuta_flag:
            text = normalize_taa_marbuta(text)
        
        return text
    except Exception as e:
        raise NormalizationError(f"Failed to normalize text: {e}") from e
