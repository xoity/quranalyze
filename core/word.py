"""
Word representation for the quranalyze framework.

This module defines the Word dataclass that represents a single word
from the Quranic text with all associated metadata.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Word:
    """
    Represents a single word from the Quran.
    
    Attributes:
        surah_number: The surah number (1-114)
        ayah_number: The ayah number within the surah
        position: Position of the word within the ayah (0-indexed)
        text: Original Arabic text
        normalized: Normalized Arabic text (without diacritics, normalized forms)
        buckwalter: Buckwalter transliteration of the text
        root: Optional morphological root (None if unavailable)
        lemma: Optional lemma form (None if unavailable)
    """
    
    surah_number: int
    ayah_number: int
    position: int
    text: str
    normalized: str
    buckwalter: str
    root: Optional[str] = None
    lemma: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate word data after initialization."""
        if self.surah_number < 1 or self.surah_number > 114:
            raise ValueError(f"Invalid surah_number: {self.surah_number}")
        if self.ayah_number < 1:
            raise ValueError(f"Invalid ayah_number: {self.ayah_number}")
        if self.position < 0:
            raise ValueError(f"Invalid position: {self.position}")
        if not self.text:
            raise ValueError("Word text cannot be empty")
        if not self.normalized:
            raise ValueError("Normalized text cannot be empty")
        if not self.buckwalter:
            raise ValueError("Buckwalter transliteration cannot be empty")
    
    @property
    def location(self) -> tuple[int, int, int]:
        """
        Return the complete location of this word.
        
        Returns:
            Tuple of (surah_number, ayah_number, position)
        """
        return (self.surah_number, self.ayah_number, self.position)
    
    def __str__(self) -> str:
        """Return string representation of the word."""
        return f"{self.text} ({self.surah_number}:{self.ayah_number}:{self.position})"
    
    def __repr__(self) -> str:
        """Return detailed representation of the word."""
        return (
            f"Word(surah={self.surah_number}, ayah={self.ayah_number}, "
            f"pos={self.position}, text='{self.text}', "
            f"normalized='{self.normalized}', buckwalter='{self.buckwalter}')"
        )
