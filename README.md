# quranalyze

A research-grade Python framework for observational analysis of the Quran using the [quranjson](https://github.com/risan/quran-json) dataset.

## Overview

`quranalyze` is designed for serious, transparent, reproducible analysis of Quranic text. It prioritizes:

- **Observational analysis only** - No interpretation, no claims, no conclusions
- **Single canonical source** - quranjson dataset as the only data source
- **Transparent assumptions** - All defaults are explicit and documented
- **Reproducible results** - Export and snapshot capabilities
- **Type safety** - Full type hints throughout
- **Extensibility** - Clean architecture for future enhancements

## Features

### Core Capabilities
- Load and parse quranjson dataset
- Represent Quran as structured data (Surahs, Ayahs, Words)
- Tokenize Arabic text deterministically
- Normalize Arabic text (diacritics, character variations)
- Buckwalter transliteration
- Filter and query by surah, ayah, text, root, lemma
- Build relationship graphs between words
- 3D visualization with matplotlib
- Export snapshots for reproducibility

### Foundation Placeholders
The following features are included as placeholders for future implementation:
- Morphological analysis (root, lemma extraction)
- Part-of-speech tagging
- Advanced graph clustering
- Audio synthesis

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd quranalyze

# Install dependencies
pip install matplotlib  # Only external dependency

# Clone the quranjson dataset
git clone https://github.com/risan/quran-json.git
```

## Quick Start

```python
from quranalyze import Corpus
from quranalyze.visualization.matplotlib_3d import Matplotlib3DVisualizer

# Load and build corpus
corpus = Corpus("./quran-json/source/surah")
corpus.build()

# Basic statistics
print(f"Total words: {corpus.total_words()}")
print(f"Total ayahs: {corpus.total_ayahs()}")

# Filter words
surah_1_words = corpus.filter_words().by_surah(1).get()
print(f"Words in Surah 1: {len(surah_1_words)}")

# Visualize
viz = Matplotlib3DVisualizer()
viz.visualize_words(surah_1_words[:100], title="First 100 words of Surah 1")
viz.show()
```

See [examples/basic_usage.py](examples/basic_usage.py) for a complete example.

## Directory Structure

```
quranalyze/
├── core/               # Core data structures
│   ├── corpus.py      # Main corpus class
│   ├── surah.py       # Surah representation
│   ├── ayah.py        # Ayah representation
│   ├── word.py        # Word representation
│   ├── relations.py   # Word relationships
│   └── filters.py     # Query filters
│
├── data/              # Data loading and processing
│   ├── quranjson_loader.py  # Dataset loader
│   ├── normalizer.py         # Text normalization
│   └── tokenizer.py          # Tokenization
│
├── linguistics/       # Linguistic analysis
│   ├── buckwalter.py  # Transliteration
│   ├── morphology.py  # Morphology (placeholder)
│   └── pos.py         # POS tagging (placeholder)
│
├── graph/             # Graph construction
│   ├── graph_builder.py  # Graph builder
│   └── clustering.py     # Clustering (placeholder)
│
├── visualization/     # Visualization tools
│   ├── base.py           # Base interface
│   └── matplotlib_3d.py  # 3D matplotlib viz
│
├── audio/             # Audio synthesis (placeholder)
│   └── synthesis.py
│
├── export/            # Export capabilities
│   └── snapshot.py
│
├── examples/          # Usage examples
│   └── basic_usage.py
│
├── config.py          # Configuration constants
├── exceptions.py      # Custom exceptions
└── __init__.py        # Package initialization
```

## Design Principles

### 1. Single Data Source
The framework uses **only** the quranjson dataset. No user-supplied text, no external corpora, no web requests.

### 2. Observational Only
This is a data analysis tool, not an interpretation tool. It provides:
- Counts and statistics
- Text relationships
- Structural patterns

It does **not** provide:
- Religious interpretations
- Thematic analysis
- Theological conclusions

### 3. Transparent Assumptions
All assumptions are explicit in [config.py](config.py):
- Normalization rules
- Tokenization delimiters
- Graph edge weights
- Visualization defaults

### 4. Reproducibility
Export functionality ensures analyses can be:
- Saved with metadata
- Shared with collaborators
- Verified independently

### 5. Extensibility
Clean architecture allows integration of:
- External morphological analyzers
- Machine learning models
- Additional visualization methods
- Custom analysis pipelines

## Usage Examples

### Filtering

```python
# By surah
words = corpus.filter_words().by_surah(1).get()

# By ayah
words = corpus.filter_words().by_ayah(1, 1).get()

# By text
words = corpus.filter_words().by_text("الله", normalized=True).get()

# Chain filters
words = corpus.filter_words().by_surah(2).by_text_contains("رحم", normalized=True).get()

# Custom filter
words = corpus.filter_words().by_custom(lambda w: w.position == 0).get()
```

### Graph Construction

```python
from quranalyze.graph.graph_builder import GraphBuilder

# Build graph from words
builder = GraphBuilder()
graph = builder.build_from_words(
    words,
    use_normalized=True,  # Connect words with identical normalized text
)

print(f"Nodes: {graph.node_count()}")
print(f"Edges: {graph.edge_count()}")

# Get neighbors
neighbors = graph.get_neighbors(words[0])
```

### Export

```python
from quranalyze.export.snapshot import SnapshotExporter

exporter = SnapshotExporter(corpus)

# Full snapshot
exporter.export_full_snapshot("snapshot.json", include_all_words=True)

# Surah summary
exporter.export_surah_summary(1, "surah_1_summary.json")

# Filtered words
filtered = corpus.filter_words().by_surah(1).get()
exporter.export_filtered_words(filtered, "surah_1_words.json")
```

## Requirements

- Python 3.10+
- matplotlib (for visualization)
- quranjson dataset (cloned locally)

## Limitations

This is a **foundation version**. The following features are planned but not implemented:

- Morphological root extraction (requires external tools like AraMorph, MADAMIRA)
- Lemmatization (requires dictionary/morphological analyzer)
- Part-of-speech tagging (requires trained models)
- Advanced graph clustering (requires networkx or similar)
- Audio synthesis (requires Arabic TTS engine)

## Contributing

Contributions should maintain the framework's core principles:
- No interpretation or claims
- Transparent assumptions
- Type hints and docstrings for all code
- No hidden defaults

## License

MIT

## Acknowledgments

- Data source: [quranjson](https://github.com/risan/quran-json) by Risan Bagja Pradana
- Buckwalter transliteration scheme
- Arabic text processing conventions

## Citation

If you use this framework in research, please cite both the framework and the quranjson dataset.
