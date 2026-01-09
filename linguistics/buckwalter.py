"""
Buckwalter transliteration for Arabic text.

This module provides bidirectional transliteration between Arabic script
and ASCII-based Buckwalter transliteration scheme.
"""

from typing import Final

from ..exceptions import TransliterationError


# Buckwalter transliteration mapping (Arabic -> Buckwalter)
ARABIC_TO_BUCKWALTER_MAP: Final[dict[str, str]] = {
    # Letters
    "\u0621": "'",   # Hamza
    "\u0622": "|",   # Alef with madda
    "\u0623": ">",   # Alef with hamza above
    "\u0624": "&",   # Waw with hamza
    "\u0625": "<",   # Alef with hamza below
    "\u0626": "}",   # Yeh with hamza
    "\u0627": "A",   # Alef
    "\u0628": "b",   # Beh
    "\u0629": "p",   # Teh marbuta
    "\u062A": "t",   # Teh
    "\u062B": "v",   # Theh
    "\u062C": "j",   # Jeem
    "\u062D": "H",   # Hah
    "\u062E": "x",   # Khah
    "\u062F": "d",   # Dal
    "\u0630": "*",   # Thal
    "\u0631": "r",   # Reh
    "\u0632": "z",   # Zain
    "\u0633": "s",   # Seen
    "\u0634": "$",   # Sheen
    "\u0635": "S",   # Sad
    "\u0636": "D",   # Dad
    "\u0637": "T",   # Tah
    "\u0638": "Z",   # Zah
    "\u0639": "E",   # Ain
    "\u063A": "g",   # Ghain
    "\u0640": "_",   # Tatweel
    "\u0641": "f",   # Feh
    "\u0642": "q",   # Qaf
    "\u0643": "k",   # Kaf
    "\u0644": "l",   # Lam
    "\u0645": "m",   # Meem
    "\u0646": "n",   # Noon
    "\u0647": "h",   # Heh
    "\u0648": "w",   # Waw
    "\u0649": "Y",   # Alef maksura
    "\u064A": "y",   # Yeh
    
    # Diacritics
    "\u064B": "F",   # Fathatan
    "\u064C": "N",   # Dammatan
    "\u064D": "K",   # Kasratan
    "\u064E": "a",   # Fatha
    "\u064F": "u",   # Damma
    "\u0650": "i",   # Kasra
    "\u0651": "~",   # Shadda
    "\u0652": "o",   # Sukun
    "\u0653": "^",   # Maddah
    "\u0654": "#",   # Hamza above
    "\u0670": "`",   # Superscript alef
    
    # Additional characters
    "\u0671": "{",   # Alef wasla
}

# Reverse mapping (Buckwalter -> Arabic)
BUCKWALTER_TO_ARABIC_MAP: Final[dict[str, str]] = {
    v: k for k, v in ARABIC_TO_BUCKWALTER_MAP.items()
}


def arabic_to_buckwalter(text: str) -> str:
    """
    Convert Arabic text to Buckwalter transliteration.
    
    Args:
        text: Arabic text to transliterate
        
    Returns:
        Buckwalter transliteration
        
    Raises:
        TransliterationError: If transliteration fails
    """
    if not text:
        return text
    
    try:
        result = []
        for char in text:
            if char in ARABIC_TO_BUCKWALTER_MAP:
                result.append(ARABIC_TO_BUCKWALTER_MAP[char])
            else:
                # Keep non-Arabic characters as-is
                result.append(char)
        return "".join(result)
    except Exception as e:
        raise TransliterationError(f"Failed to convert to Buckwalter: {e}") from e


def buckwalter_to_arabic(text: str) -> str:
    """
    Convert Buckwalter transliteration to Arabic text.
    
    Args:
        text: Buckwalter transliteration
        
    Returns:
        Arabic text
        
    Raises:
        TransliterationError: If transliteration fails
    """
    if not text:
        return text
    
    try:
        result = []
        for char in text:
            if char in BUCKWALTER_TO_ARABIC_MAP:
                result.append(BUCKWALTER_TO_ARABIC_MAP[char])
            else:
                # Keep non-Buckwalter characters as-is
                result.append(char)
        return "".join(result)
    except Exception as e:
        raise TransliterationError(f"Failed to convert from Buckwalter: {e}") from e


def is_arabic_char(char: str) -> bool:
    """
    Check if a character is an Arabic character.
    
    Args:
        char: Single character to check
        
    Returns:
        True if the character is Arabic, False otherwise
    """
    return char in ARABIC_TO_BUCKWALTER_MAP


def is_buckwalter_char(char: str) -> bool:
    """
    Check if a character is a Buckwalter transliteration character.
    
    Args:
        char: Single character to check
        
    Returns:
        True if the character is Buckwalter, False otherwise
    """
    return char in BUCKWALTER_TO_ARABIC_MAP
