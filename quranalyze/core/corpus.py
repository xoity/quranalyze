"""
Corpus representation for the quranalyze framework.

This module provides the main Corpus class that represents the complete
Quranic text with all analysis capabilities.
"""

from typing import Optional

from .ayah import Ayah
from .filters import WordFilter
from .surah import Surah
from .word import Word
from ..data.normalizer import normalize_text
from ..data.quranjson_loader import QuranJsonLoader
from ..data.tokenizer import tokenize_ayah
from ..exceptions import QuranalyzeError
from ..linguistics.buckwalter import arabic_to_buckwalter


class Corpus:
    """
    Main corpus class representing the complete Quranic text.
    
    This class loads data from quranjson, tokenizes it into words,
    and provides comprehensive querying and analysis capabilities.
    
    Attributes:
        surahs: Tuple of all Surah objects
        words: List of all Word objects in the corpus
    """
    
    def __init__(self, data_path: str) -> None:
        """
        Initialize the corpus by loading data from quranjson.
        
        Args:
            data_path: Path to the quranjson dataset directory
            
        Raises:
            QuranalyzeError: If corpus initialization fails
        """
        self._loader = QuranJsonLoader(data_path)
        self._surahs: Optional[tuple[Surah, ...]] = None
        self._words: Optional[list[Word]] = None
    
    @property
    def surahs(self) -> tuple[Surah, ...]:
        """Get all surahs in the corpus."""
        if self._surahs is None:
            raise QuranalyzeError("Corpus not built. Call build() first.")
        return self._surahs
    
    @property
    def words(self) -> list[Word]:
        """Get all words in the corpus."""
        if self._words is None:
            raise QuranalyzeError("Corpus not built. Call build() first.")
        return self._words
    
    def build(self) -> None:
        """
        Build the corpus by loading and processing all data.
        
        This method:
        1. Loads all surahs from quranjson
        2. Tokenizes all ayahs into words
        3. Normalizes and transliterates each word
        4. Constructs the complete word list
        
        Raises:
            QuranalyzeError: If building fails
        """
        try:
            # Load all surahs
            surahs = self._loader.load_all_surahs()
            self._surahs = tuple(surahs)
            
            # Build word list
            words = []
            for surah in surahs:
                for ayah in surah.ayahs:
                    ayah_words = self._process_ayah(ayah)
                    words.extend(ayah_words)
            
            self._words = words
        except Exception as e:
            raise QuranalyzeError(f"Failed to build corpus: {e}") from e
    
    def _process_ayah(self, ayah: Ayah) -> list[Word]:
        """
        Process an ayah into Word objects.
        
        Args:
            ayah: The Ayah to process
            
        Returns:
            List of Word objects from this ayah
        """
        tokens = tokenize_ayah(ayah.text)
        words = []
        
        for position, text in enumerate(tokens):
            # Normalize text
            normalized = normalize_text(text)
            
            # Generate Buckwalter transliteration
            buckwalter = arabic_to_buckwalter(text)
            
            # Create Word object
            word = Word(
                surah_number=ayah.surah_number,
                ayah_number=ayah.ayah_number,
                position=position,
                text=text,
                normalized=normalized,
                buckwalter=buckwalter,
                root=None,  # Not available yet
                lemma=None,  # Not available yet
            )
            words.append(word)
        
        return words
    
    def get_surah(self, surah_number: int) -> Optional[Surah]:
        """
        Get a specific surah by number.
        
        Args:
            surah_number: The surah number (1-114)
            
        Returns:
            Surah object if found, None otherwise
        """
        for surah in self.surahs:
            if surah.number == surah_number:
                return surah
        return None
    
    def get_ayah(self, surah_number: int, ayah_number: int) -> Optional[Ayah]:
        """
        Get a specific ayah.
        
        Args:
            surah_number: The surah number (1-114)
            ayah_number: The ayah number within the surah
            
        Returns:
            Ayah object if found, None otherwise
        """
        surah = self.get_surah(surah_number)
        if surah:
            return surah.get_ayah(ayah_number)
        return None
    
    def filter_words(self) -> WordFilter:
        """
        Create a new word filter for querying.
        
        Returns:
            WordFilter initialized with all corpus words
        """
        return WordFilter(self.words)
    
    def total_words(self) -> int:
        """
        Get the total number of words in the corpus.
        
        Returns:
            Total word count
        """
        return len(self.words)
    
    def total_surahs(self) -> int:
        """
        Get the total number of surahs.
        
        Returns:
            Total surah count (should always be 114)
        """
        return len(self.surahs)
    
    def total_ayahs(self) -> int:
        """
        Get the total number of ayahs in the corpus.
        
        Returns:
            Total ayah count
        """
        return sum(surah.ayah_count for surah in self.surahs)
    
    def word_count_by_surah(self) -> dict[int, int]:
        """
        Get word counts for each surah.
        
        Returns:
            Dictionary mapping surah number to word count
        """
        counts = {}
        for surah in self.surahs:
            surah_words = self.filter_words().by_surah(surah.number).get()
            counts[surah.number] = len(surah_words)
        return counts
    
    def __repr__(self) -> str:
        """Return detailed representation of the corpus."""
        if self._surahs is None:
            return "Corpus(unbuilt)"
        return (
            f"Corpus(surahs={len(self.surahs)}, "
            f"ayahs={self.total_ayahs()}, "
            f"words={self.total_words()})"
        )
