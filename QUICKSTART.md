# Quick Start Guide

Get up and running with quranalyze in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install matplotlib
```

That's it! Only one dependency.

## Step 2: Get the Data

```bash
# Clone the quranjson dataset
git clone https://github.com/risan/quran-json.git
```

## Step 3: Run the Example

```bash
# Navigate to quranalyze directory
cd quranalyze

# Run the example script
python examples/basic_usage.py --data-path ../quran-json/source/surah
```

## Step 4: Write Your Own Analysis

Create a file `my_analysis.py`:

```python
from quranalyze import Corpus

# Initialize corpus
corpus = Corpus("./quran-json/source/surah")
corpus.build()

# Get statistics
print(f"Total words: {corpus.total_words()}")
print(f"Total surahs: {corpus.total_surahs()}")
print(f"Total ayahs: {corpus.total_ayahs()}")

# Filter words from Surah 1
surah_1 = corpus.filter_words().by_surah(1).get()
print(f"\nSurah 1 has {len(surah_1)} words")

# Show first 5 words
print("\nFirst 5 words:")
for word in surah_1[:5]:
    print(f"  {word.text} -> {word.buckwalter}")

# Get word counts per surah
word_counts = corpus.word_count_by_surah()
print(f"\nSurah 2 has {word_counts[2]} words")
```

Run it:

```bash
python my_analysis.py
```

## Step 5: Visualize

```python
from quranalyze import Corpus
from quranalyze.visualization.matplotlib_3d import Matplotlib3DVisualizer

# Load corpus
corpus = Corpus("./quran-json/source/surah")
corpus.build()

# Get some words
words = corpus.words[:200]  # First 200 words

# Visualize
viz = Matplotlib3DVisualizer()
viz.visualize_words(words, title="First 200 Words of the Quran")
viz.save("output.png")
viz.show()
```

## Common Use Cases

### Find all occurrences of a word

```python
# Find all instances of "الله"
allah_words = corpus.filter_words().by_text("الله", normalized=True).get()
print(f"Found {len(allah_words)} occurrences")

# Show locations
for word in allah_words[:5]:
    print(f"  Surah {word.surah_number}, Ayah {word.ayah_number}")
```

### Analyze a specific surah

```python
# Get Surah 1
surah = corpus.get_surah(1)
print(f"{surah.name}: {surah.ayah_count} ayahs")

# Get all words in this surah
words = corpus.filter_words().by_surah(1).get()
print(f"Total words: {len(words)}")

# Get unique normalized forms
unique_words = set(w.normalized for w in words)
print(f"Unique words: {len(unique_words)}")
```

### Build a word graph

```python
from quranalyze.graph.graph_builder import GraphBuilder

# Get words from Surah 1
words = corpus.filter_words().by_surah(1).get()

# Build graph
builder = GraphBuilder()
graph = builder.build_from_words(words, use_normalized=True)

print(f"Graph has {graph.node_count()} nodes")
print(f"Graph has {graph.edge_count()} edges")

# Find words connected to a specific word
word = words[0]
neighbors = graph.get_neighbors(word)
print(f"{word.text} is connected to {len(neighbors)} other words")
```

### Export data

```python
from quranalyze.export.snapshot import SnapshotExporter

# Create exporter
exporter = SnapshotExporter(corpus)

# Export full snapshot
exporter.export_full_snapshot("corpus_snapshot.json")

# Export Surah 1 summary
exporter.export_surah_summary(1, "surah_1.json")

# Export filtered words
words = corpus.filter_words().by_surah(1).get()
exporter.export_filtered_words(words, "surah_1_words.json")
```

## Need Help?

- Read [README.md](README.md) for complete documentation
- Check [examples/basic_usage.py](examples/basic_usage.py) for more examples
- See [DEVELOPMENT.md](DEVELOPMENT.md) for advanced usage

## Next Steps

1. Explore filtering capabilities
2. Try different visualization options
3. Build relationship graphs
4. Export your analysis results
5. Consider contributing morphological analysis integration

Happy analyzing! 📊
