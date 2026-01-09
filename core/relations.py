"""
Relationship modeling for Quranic words.

This module provides functionality to model relationships between words
based on shared linguistic features like roots and lemmas.
"""

from dataclasses import dataclass
from typing import Optional

from ..core.word import Word


@dataclass(frozen=True)
class WordRelation:
    """
    Represents a relationship between two words.
    
    Attributes:
        word1: First word in the relationship
        word2: Second word in the relationship
        relation_type: Type of relationship (e.g., "shared_root", "shared_lemma")
        weight: Strength of the relationship (0.0 to 1.0)
        metadata: Optional additional information about the relationship
    """
    
    word1: Word
    word2: Word
    relation_type: str
    weight: float = 1.0
    metadata: Optional[dict[str, str]] = None
    
    def __post_init__(self) -> None:
        """Validate relation data after initialization."""
        if self.weight < 0.0 or self.weight > 1.0:
            raise ValueError(f"Weight must be between 0.0 and 1.0, got {self.weight}")
        if not self.relation_type:
            raise ValueError("Relation type cannot be empty")
    
    def involves_word(self, word: Word) -> bool:
        """
        Check if this relation involves a specific word.
        
        Args:
            word: The word to check
            
        Returns:
            True if the word is part of this relation
        """
        return self.word1 == word or self.word2 == word
    
    def other_word(self, word: Word) -> Optional[Word]:
        """
        Get the other word in this relation.
        
        Args:
            word: One word in the relation
            
        Returns:
            The other word, or None if given word is not in relation
        """
        if self.word1 == word:
            return self.word2
        elif self.word2 == word:
            return self.word1
        return None
    
    def __str__(self) -> str:
        """Return string representation of the relation."""
        return (
            f"{self.word1.text} <-[{self.relation_type}]-> {self.word2.text} "
            f"(weight: {self.weight:.2f})"
        )


class RelationBuilder:
    """
    Builder for constructing relationships between words.
    
    This class provides methods to identify and create relationships
    based on various linguistic features.
    """
    
    def __init__(self) -> None:
        """Initialize the relation builder."""
        self.relations: list[WordRelation] = []
    
    def add_relation(
        self,
        word1: Word,
        word2: Word,
        relation_type: str,
        weight: float = 1.0,
        metadata: Optional[dict[str, str]] = None,
    ) -> None:
        """
        Add a new relation between two words.
        
        Args:
            word1: First word
            word2: Second word
            relation_type: Type of relationship
            weight: Strength of relationship (default: 1.0)
            metadata: Optional additional information
        """
        relation = WordRelation(
            word1=word1,
            word2=word2,
            relation_type=relation_type,
            weight=weight,
            metadata=metadata,
        )
        self.relations.append(relation)
    
    def build_root_relations(self, words: list[Word], min_weight: float = 1.0) -> None:
        """
        Build relations between words sharing the same root.
        
        Args:
            words: List of words to analyze
            min_weight: Minimum weight for created relations
            
        Note:
            In this foundation version, roots are not available,
            so no relations will be created.
        """
        # Group words by root
        root_groups: dict[str, list[Word]] = {}
        for word in words:
            if word.root:  # Only if root is available
                if word.root not in root_groups:
                    root_groups[word.root] = []
                root_groups[word.root].append(word)
        
        # Create relations within each group
        for root, group_words in root_groups.items():
            for i, word1 in enumerate(group_words):
                for word2 in group_words[i + 1:]:
                    self.add_relation(
                        word1=word1,
                        word2=word2,
                        relation_type="shared_root",
                        weight=min_weight,
                        metadata={"root": root},
                    )
    
    def build_lemma_relations(self, words: list[Word], min_weight: float = 0.5) -> None:
        """
        Build relations between words sharing the same lemma.
        
        Args:
            words: List of words to analyze
            min_weight: Minimum weight for created relations
            
        Note:
            In this foundation version, lemmas are not available,
            so no relations will be created.
        """
        # Group words by lemma
        lemma_groups: dict[str, list[Word]] = {}
        for word in words:
            if word.lemma:  # Only if lemma is available
                if word.lemma not in lemma_groups:
                    lemma_groups[word.lemma] = []
                lemma_groups[word.lemma].append(word)
        
        # Create relations within each group
        for lemma, group_words in lemma_groups.items():
            for i, word1 in enumerate(group_words):
                for word2 in group_words[i + 1:]:
                    self.add_relation(
                        word1=word1,
                        word2=word2,
                        relation_type="shared_lemma",
                        weight=min_weight,
                        metadata={"lemma": lemma},
                    )
    
    def build_normalized_text_relations(self, words: list[Word], weight: float = 0.8) -> None:
        """
        Build relations between words with identical normalized text.
        
        This creates relations based on surface form similarity after normalization.
        
        Args:
            words: List of words to analyze
            weight: Weight for created relations (default: 0.8)
        """
        # Group words by normalized text
        text_groups: dict[str, list[Word]] = {}
        for word in words:
            if word.normalized not in text_groups:
                text_groups[word.normalized] = []
            text_groups[word.normalized].append(word)
        
        # Create relations within each group (only if group size > 1)
        for normalized_text, group_words in text_groups.items():
            if len(group_words) > 1:
                for i, word1 in enumerate(group_words):
                    for word2 in group_words[i + 1:]:
                        self.add_relation(
                            word1=word1,
                            word2=word2,
                            relation_type="identical_normalized",
                            weight=weight,
                            metadata={"normalized_text": normalized_text},
                        )
    
    def get_relations(self) -> list[WordRelation]:
        """
        Get all built relations.
        
        Returns:
            List of WordRelation objects
        """
        return self.relations
    
    def clear(self) -> None:
        """Clear all built relations."""
        self.relations = []
    
    def count(self) -> int:
        """
        Count the number of relations.
        
        Returns:
            Number of relations
        """
        return len(self.relations)
