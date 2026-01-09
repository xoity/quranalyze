"""
Ayah representation for the quranalyze framework.

This module defines the Ayah dataclass that represents a single verse
from the Quranic text.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Ayah:
    """
    Represents a single ayah (verse) from the Quran.
    
    Attributes:
        surah_number: The surah number (1-114)
        ayah_number: The ayah number within the surah
        text: Original Arabic text of the ayah
        number_in_quran: Optional global ayah number across entire Quran
    """
    
    surah_number: int
    ayah_number: int
    text: str
    number_in_quran: Optional[int] = None
    
    def __post_init__(self) -> None:
        """Validate ayah data after initialization."""
        if self.surah_number < 1 or self.surah_number > 114:
            raise ValueError(f"Invalid surah_number: {self.surah_number}")
        if self.ayah_number < 1:
            raise ValueError(f"Invalid ayah_number: {self.ayah_number}")
        if not self.text:
            raise ValueError("Ayah text cannot be empty")
        if self.number_in_quran is not None and self.number_in_quran < 1:
            raise ValueError(f"Invalid number_in_quran: {self.number_in_quran}")
    
    @property
    def location(self) -> tuple[int, int]:
        """
        Return the location of this ayah.
        
        Returns:
            Tuple of (surah_number, ayah_number)
        """
        return (self.surah_number, self.ayah_number)
    
    def word_count(self) -> int:
        """
        Return the number of words in this ayah.
        
        Note: This is a simple word count based on whitespace splitting.
        For accurate word tokenization, use the tokenizer module.
        
        Returns:
            Number of words (space-delimited)
        """
        return len(self.text.split())
    
    def __str__(self) -> str:
        """Return string representation of the ayah."""
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Ayah {self.surah_number}:{self.ayah_number} - {preview}"
    
    def __repr__(self) -> str:
        """Return detailed representation of the ayah."""
        return (
            f"Ayah(surah={self.surah_number}, ayah={self.ayah_number}, "
            f"text='{self.text[:30]}...', number_in_quran={self.number_in_quran})"
        )
