"""
Graph construction for word relationships.

This module provides functionality to build graph structures from
word relationships for network analysis and visualization.
"""

from typing import Any, Optional

from ..core.relations import RelationBuilder, WordRelation
from ..core.word import Word
from ..exceptions import GraphBuildError


class WordGraph:
    """
    Graph representation of word relationships.
    
    This class represents words as nodes and relationships as edges,
    suitable for network analysis and visualization.
    
    Attributes:
        nodes: Dictionary mapping word to node data
        edges: List of edge tuples (word1, word2, weight, relation_type)
    """
    
    def __init__(self) -> None:
        """Initialize an empty graph."""
        self.nodes: dict[Word, dict[str, Any]] = {}
        self.edges: list[tuple[Word, Word, float, str]] = []
    
    def add_node(self, word: Word, **attributes: Any) -> None:
        """
        Add a word as a node in the graph.
        
        Args:
            word: The Word object to add as a node
            **attributes: Additional attributes for the node
        """
        if word not in self.nodes:
            self.nodes[word] = attributes
    
    def add_edge(
        self,
        word1: Word,
        word2: Word,
        weight: float = 1.0,
        relation_type: str = "unknown",
    ) -> None:
        """
        Add an edge between two words.
        
        Args:
            word1: First word
            word2: Second word
            weight: Edge weight (default: 1.0)
            relation_type: Type of relationship
        """
        # Ensure nodes exist
        self.add_node(word1)
        self.add_node(word2)
        
        # Add edge
        self.edges.append((word1, word2, weight, relation_type))
    
    def get_neighbors(self, word: Word) -> list[Word]:
        """
        Get all words connected to the given word.
        
        Args:
            word: The word to find neighbors for
            
        Returns:
            List of neighboring words
        """
        neighbors = []
        for word1, word2, _, _ in self.edges:
            if word1 == word:
                neighbors.append(word2)
            elif word2 == word:
                neighbors.append(word1)
        return neighbors
    
    def get_edges_for_word(self, word: Word) -> list[tuple[Word, Word, float, str]]:
        """
        Get all edges involving a specific word.
        
        Args:
            word: The word to find edges for
            
        Returns:
            List of edge tuples
        """
        return [edge for edge in self.edges if word in (edge[0], edge[1])]
    
    def node_count(self) -> int:
        """
        Get the number of nodes in the graph.
        
        Returns:
            Number of nodes
        """
        return len(self.nodes)
    
    def edge_count(self) -> int:
        """
        Get the number of edges in the graph.
        
        Returns:
            Number of edges
        """
        return len(self.edges)
    
    def degree(self, word: Word) -> int:
        """
        Get the degree (number of connections) of a word.
        
        Args:
            word: The word to calculate degree for
            
        Returns:
            Degree of the word
        """
        return len(self.get_neighbors(word))
    
    def subgraph(self, words: list[Word]) -> "WordGraph":
        """
        Create a subgraph containing only specified words.
        
        Args:
            words: List of words to include in subgraph
            
        Returns:
            New WordGraph containing only specified words and their edges
        """
        word_set = set(words)
        subgraph = WordGraph()
        
        # Add nodes
        for word in words:
            if word in self.nodes:
                subgraph.add_node(word, **self.nodes[word])
        
        # Add edges that connect words in the subgraph
        for word1, word2, weight, relation_type in self.edges:
            if word1 in word_set and word2 in word_set:
                subgraph.add_edge(word1, word2, weight, relation_type)
        
        return subgraph
    
    def __repr__(self) -> str:
        """Return string representation of the graph."""
        return f"WordGraph(nodes={self.node_count()}, edges={self.edge_count()})"


class GraphBuilder:
    """
    Builder for constructing WordGraph from relationships.
    
    This class takes word relationships and constructs a graph structure
    suitable for analysis and visualization.
    """
    
    def __init__(self) -> None:
        """Initialize the graph builder."""
        self.graph = WordGraph()
    
    def build_from_relations(self, relations: list[WordRelation]) -> WordGraph:
        """
        Build a graph from a list of word relations.
        
        Args:
            relations: List of WordRelation objects
            
        Returns:
            Constructed WordGraph
            
        Raises:
            GraphBuildError: If graph construction fails
        """
        try:
            self.graph = WordGraph()
            
            for relation in relations:
                self.graph.add_edge(
                    word1=relation.word1,
                    word2=relation.word2,
                    weight=relation.weight,
                    relation_type=relation.relation_type,
                )
            
            return self.graph
        except Exception as e:
            raise GraphBuildError(f"Failed to build graph: {e}") from e
    
    def build_from_words(
        self,
        words: list[Word],
        use_roots: bool = True,
        use_lemmas: bool = True,
        use_normalized: bool = True,
    ) -> WordGraph:
        """
        Build a graph from a list of words by discovering relationships.
        
        Args:
            words: List of Word objects
            use_roots: Whether to create root-based relations
            use_lemmas: Whether to create lemma-based relations
            use_normalized: Whether to create normalized text relations
            
        Returns:
            Constructed WordGraph
            
        Raises:
            GraphBuildError: If graph construction fails
        """
        try:
            # Build relations
            relation_builder = RelationBuilder()
            
            if use_roots:
                relation_builder.build_root_relations(words)
            if use_lemmas:
                relation_builder.build_lemma_relations(words)
            if use_normalized:
                relation_builder.build_normalized_text_relations(words)
            
            # Build graph from relations
            return self.build_from_relations(relation_builder.get_relations())
        except Exception as e:
            raise GraphBuildError(f"Failed to build graph from words: {e}") from e
    
    def get_graph(self) -> WordGraph:
        """
        Get the current graph.
        
        Returns:
            The constructed WordGraph
        """
        return self.graph
