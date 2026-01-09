"""
Filter utilities for querying Quranic data.

This module provides filtering functions to query the corpus by various criteria.
"""

from typing import Callable, Optional

from .word import Word
from ..exceptions import FilterError


class WordFilter:
    """
    Filter system for Word objects.
    
    This class provides methods to filter Word objects based on various criteria.
    Filters can be combined using method chaining.
    """
    
    def __init__(self, words: list[Word]) -> None:
        """
        Initialize filter with a list of words.
        
        Args:
            words: List of Word objects to filter
        """
        self.words = words
    
    def by_surah(self, surah_number: int) -> "WordFilter":
        """
        Filter words by surah number.
        
        Args:
            surah_number: The surah number to filter by (1-114)
            
        Returns:
            New WordFilter with filtered words
            
        Raises:
            FilterError: If surah_number is invalid
        """
        if surah_number < 1 or surah_number > 114:
            raise FilterError(f"Invalid surah number: {surah_number}")
        
        filtered = [w for w in self.words if w.surah_number == surah_number]
        return WordFilter(filtered)
    
    def by_ayah(self, surah_number: int, ayah_number: int) -> "WordFilter":
        """
        Filter words by surah and ayah number.
        
        Args:
            surah_number: The surah number (1-114)
            ayah_number: The ayah number within the surah
            
        Returns:
            New WordFilter with filtered words
            
        Raises:
            FilterError: If parameters are invalid
        """
        if surah_number < 1 or surah_number > 114:
            raise FilterError(f"Invalid surah number: {surah_number}")
        if ayah_number < 1:
            raise FilterError(f"Invalid ayah number: {ayah_number}")
        
        filtered = [
            w for w in self.words
            if w.surah_number == surah_number and w.ayah_number == ayah_number
        ]
        return WordFilter(filtered)
    
    def by_text(self, text: str, normalized: bool = False) -> "WordFilter":
        """
        Filter words by exact text match.
        
        Args:
            text: The text to match
            normalized: Whether to match against normalized text (default: False)
            
        Returns:
            New WordFilter with filtered words
        """
        if normalized:
            filtered = [w for w in self.words if w.normalized == text]
        else:
            filtered = [w for w in self.words if w.text == text]
        return WordFilter(filtered)
    
    def by_text_contains(self, substring: str, normalized: bool = False) -> "WordFilter":
        """
        Filter words containing a substring.
        
        Args:
            substring: The substring to search for
            normalized: Whether to search in normalized text (default: False)
            
        Returns:
            New WordFilter with filtered words
        """
        if normalized:
            filtered = [w for w in self.words if substring in w.normalized]
        else:
            filtered = [w for w in self.words if substring in w.text]
        return WordFilter(filtered)
    
    def by_root(self, root: str) -> "WordFilter":
        """
        Filter words by morphological root.
        
        Args:
            root: The root to filter by
            
        Returns:
            New WordFilter with filtered words
        """
        filtered = [w for w in self.words if w.root == root]
        return WordFilter(filtered)
    
    def by_lemma(self, lemma: str) -> "WordFilter":
        """
        Filter words by lemma.
        
        Args:
            lemma: The lemma to filter by
            
        Returns:
            New WordFilter with filtered words
        """
        filtered = [w for w in self.words if w.lemma == lemma]
        return WordFilter(filtered)
    
    def by_custom(self, predicate: Callable[[Word], bool]) -> "WordFilter":
        """
        Filter words using a custom predicate function.
        
        Args:
            predicate: Function that takes a Word and returns bool
            
        Returns:
            New WordFilter with filtered words
            
        Raises:
            FilterError: If predicate execution fails
        """
        try:
            filtered = [w for w in self.words if predicate(w)]
            return WordFilter(filtered)
        except Exception as e:
            raise FilterError(f"Custom filter failed: {e}") from e
    
    def get(self) -> list[Word]:
        """
        Get the current filtered list of words.
        
        Returns:
            List of filtered Word objects
        """
        return self.words
    
    def count(self) -> int:
        """
        Count the number of words in the current filter.
        
        Returns:
            Number of words
        """
        return len(self.words)
    
    def first(self) -> Optional[Word]:
        """
        Get the first word in the current filter.
        
        Returns:
            First Word object or None if empty
        """
        return self.words[0] if self.words else None
    
    def last(self) -> Optional[Word]:
        """
        Get the last word in the current filter.
        
        Returns:
            Last Word object or None if empty
        """
        return self.words[-1] if self.words else None
