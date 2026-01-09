"""
Basic usage example for the quranalyze framework.

This script demonstrates the fundamental capabilities of the framework:
1. Loading Quranic data from quranjson
2. Building the corpus
3. Computing basic statistics
4. Filtering and querying
5. Simple 3D visualization

Prerequisites:
- Clone the quranjson repository: https://github.com/semarketir/quranjson
- Install matplotlib: pip install matplotlib

Usage:
    python basic_usage.py --data-path /path/to/quranjson/source/surah
"""

import argparse
from pathlib import Path

from quranalyze import Corpus
from quranalyze.visualization.matplotlib_3d import Matplotlib3DVisualizer
from quranalyze.graph.graph_builder import GraphBuilder
from quranalyze.export.snapshot import SnapshotExporter


def main(data_path: str) -> None:
    """
    Main example function.
    
    Args:
        data_path: Path to quranjson surah directory
    """
    print("=" * 60)
    print("quranalyze - Basic Usage Example")
    print("=" * 60)
    print()
    
    # Step 1: Initialize and build corpus
    print("Step 1: Loading Quranic data from quranjson...")
    print(f"Data path: {data_path}")
    
    try:
        corpus = Corpus(data_path)
        corpus.build()
        print("✓ Corpus built successfully")
        print()
    except Exception as e:
        print(f"✗ Failed to build corpus: {e}")
        print()
        print("Make sure you have cloned the quranjson repository:")
        print("  git clone https://github.com/semarketir/quranjson.git")
        print()
        print("Then run this script with the correct path:")
        print("  python basic_usage.py --data-path ./quranjson/source/surah")
        return
    
    # Step 2: Display corpus statistics
    print("Step 2: Corpus Statistics")
    print("-" * 60)
    print(f"Total Surahs:  {corpus.total_surahs()}")
    print(f"Total Ayahs:   {corpus.total_ayahs()}")
    print(f"Total Words:   {corpus.total_words()}")
    print()
    
    # Step 3: Word counts by surah
    print("Step 3: Word Counts by Surah (first 10)")
    print("-" * 60)
    word_counts = corpus.word_count_by_surah()
    for surah_num in range(1, 11):
        surah = corpus.get_surah(surah_num)
        count = word_counts[surah_num]
        print(f"Surah {surah_num:3d} - {surah.name:20s}: {count:5d} words")
    print()
    
    # Step 4: Filter examples
    print("Step 4: Filtering Examples")
    print("-" * 60)
    
    # Get words from Surah 1
    surah_1_words = corpus.filter_words().by_surah(1).get()
    print(f"Words in Surah 1: {len(surah_1_words)}")
    
    # Get first 5 words of Surah 1
    print("\nFirst 5 words of Surah 1:")
    for word in surah_1_words[:5]:
        print(f"  {word.text} (position {word.position}) -> {word.buckwalter}")
    
    # Filter by specific ayah
    ayah_words = corpus.filter_words().by_ayah(1, 1).get()
    print(f"\nWords in Surah 1, Ayah 1: {len(ayah_words)}")
    print()
    
    # Step 5: Graph construction
    print("Step 5: Graph Construction")
    print("-" * 60)
    
    # Build graph for Surah 1 based on normalized text
    builder = GraphBuilder()
    graph = builder.build_from_words(
        surah_1_words,
        use_roots=False,      # Not available yet
        use_lemmas=False,     # Not available yet
        use_normalized=True,  # Available
    )
    print(f"Graph nodes (words): {graph.node_count()}")
    print(f"Graph edges (relationships): {graph.edge_count()}")
    print()
    
    # Step 6: Export snapshot
    print("Step 6: Export Snapshot")
    print("-" * 60)
    
    exporter = SnapshotExporter(corpus)
    snapshot_path = "corpus_snapshot.json"
    
    try:
        exporter.export_full_snapshot(
            snapshot_path,
            include_all_words=False  # Set to True for full export (large file)
        )
        print(f"✓ Snapshot exported to: {snapshot_path}")
        print()
    except Exception as e:
        print(f"✗ Failed to export snapshot: {e}")
        print()
    
    # Step 7: Visualization
    print("Step 7: 3D Visualization")
    print("-" * 60)
    print("Creating 3D scatter plot of first 100 words...")
    
    try:
        viz = Matplotlib3DVisualizer(
            figure_size=(14, 10),
            point_size=40,
            alpha=0.7,
        )
        
        # Visualize first 100 words
        sample_words = corpus.words[:100]
        viz.visualize_words(
            sample_words,
            title="3D Distribution of First 100 Words in the Quran"
        )
        
        # Save figure
        output_path = "word_distribution_3d.png"
        viz.save(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Visualization saved to: {output_path}")
        
        # Show interactive plot
        print("Displaying interactive 3D plot...")
        print("(Close the plot window to continue)")
        viz.show()
        
        viz.close()
        print()
    except Exception as e:
        print(f"✗ Visualization failed: {e}")
        print("Make sure matplotlib is installed: pip install matplotlib")
        print()
    
    # Summary
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("- Explore different filtering options")
    print("- Build graphs with different relationship types")
    print("- Export and analyze specific surahs")
    print("- Integrate morphological analysis tools (future)")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Basic usage example for quranalyze framework"
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default="./quranjson/source/surah",
        help="Path to quranjson surah directory (default: ./quranjson/source/surah)"
    )
    
    args = parser.parse_args()
    main(args.data_path)
