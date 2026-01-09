"""
quranalyze - A research-grade framework for Quranic text analysis.

This framework provides tools for observational analysis of the Quran
using the quranjson dataset as the canonical data source.

Main components:
- core: Data structures (Corpus, Surah, Ayah, Word) and filtering
- data: Loading, normalization, and tokenization
- linguistics: Buckwalter transliteration, morphology, POS tagging
- graph: Relationship modeling and graph construction
- visualization: 2D and 3D visualization tools
- audio: Audio synthesis (placeholder)
- export: Snapshot and export functionality

Usage:
    from quranalyze import Corpus
    
    corpus = Corpus("path/to/quran-json/source/surah")
    corpus.build()
    
    print(f"Total words: {corpus.total_words()}")
    
    # Filter by surah
    surah_1_words = corpus.filter_words().by_surah(1).get()
    
    # Visualize
    from quranalyze.visualization.matplotlib_3d import Matplotlib3DVisualizer
    
    viz = Matplotlib3DVisualizer()
    viz.visualize_words(surah_1_words[:100], title="First 100 words of Surah 1")
    viz.show()
"""

__version__ = "0.1.0"
__author__ = "quranalyze contributors"
__license__ = "MIT"

# Core exports
from .core.ayah import Ayah
from .core.corpus import Corpus
from .core.filters import WordFilter
from .core.relations import RelationBuilder, WordRelation
from .core.surah import Surah
from .core.word import Word

# Data exports
from .data.normalizer import normalize_text
from .data.quranjson_loader import QuranJsonLoader
from .data.tokenizer import tokenize_ayah

# Exception exports
from .exceptions import (
    DataLoadError,
    DataValidationError,
    FilterError,
    GraphBuildError,
    NormalizationError,
    QuranalyzeError,
    TokenizationError,
    TransliterationError,
    VisualizationError,
)

# Graph exports
from .graph.clustering import cluster_by_surah
from .graph.graph_builder import GraphBuilder, WordGraph

# Linguistics exports
from .linguistics.buckwalter import arabic_to_buckwalter, buckwalter_to_arabic

__all__ = [
    # Version
    "__version__",
    # Core
    "Corpus",
    "Surah",
    "Ayah",
    "Word",
    "WordFilter",
    "WordRelation",
    "RelationBuilder",
    # Data
    "QuranJsonLoader",
    "normalize_text",
    "tokenize_ayah",
    # Exceptions
    "QuranalyzeError",
    "DataLoadError",
    "DataValidationError",
    "FilterError",
    "GraphBuildError",
    "NormalizationError",
    "TokenizationError",
    "TransliterationError",
    "VisualizationError",
    # Graph
    "WordGraph",
    "GraphBuilder",
    "cluster_by_surah",
    # Linguistics
    "arabic_to_buckwalter",
    "buckwalter_to_arabic",
]
