"""
Surah representation for the quranalyze framework.

This module defines the Surah dataclass that represents a complete chapter
from the Quranic text.
"""

from dataclasses import dataclass
from typing import Optional

from .ayah import Ayah


@dataclass(frozen=True)
class Surah:
    """
    Represents a single surah (chapter) from the Quran.
    
    Attributes:
        number: The surah number (1-114)
        name: Arabic name of the surah
        ayahs: Tuple of Ayah objects in this surah
        english_name: Optional English name
        revelation_type: Optional revelation type (Meccan/Medinan)
    """
    
    number: int
    name: str
    ayahs: tuple[Ayah, ...]
    english_name: Optional[str] = None
    revelation_type: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate surah data after initialization."""
        if self.number < 1 or self.number > 114:
            raise ValueError(f"Invalid surah number: {self.number}")
        if not self.name:
            raise ValueError("Surah name cannot be empty")
        if not self.ayahs:
            raise ValueError("Surah must contain at least one ayah")
        
        # Validate that all ayahs belong to this surah
        for ayah in self.ayahs:
            if ayah.surah_number != self.number:
                raise ValueError(
                    f"Ayah surah_number {ayah.surah_number} does not match "
                    f"surah number {self.number}"
                )
    
    @property
    def ayah_count(self) -> int:
        """Return the number of ayahs in this surah."""
        return len(self.ayahs)
    
    def get_ayah(self, ayah_number: int) -> Optional[Ayah]:
        """
        Get a specific ayah by its number.
        
        Args:
            ayah_number: The ayah number to retrieve
            
        Returns:
            The Ayah object if found, None otherwise
        """
        for ayah in self.ayahs:
            if ayah.ayah_number == ayah_number:
                return ayah
        return None
    
    def total_words(self) -> int:
        """
        Return the total number of words in this surah.
        
        Note: This is a simple count based on whitespace splitting.
        For accurate word tokenization, use the tokenizer module.
        
        Returns:
            Total number of words across all ayahs
        """
        return sum(ayah.word_count() for ayah in self.ayahs)
    
    def __str__(self) -> str:
        """Return string representation of the surah."""
        return f"Surah {self.number}: {self.name} ({self.ayah_count} ayahs)"
    
    def __repr__(self) -> str:
        """Return detailed representation of the surah."""
        return (
            f"Surah(number={self.number}, name='{self.name}', "
            f"ayah_count={self.ayah_count})"
        )
