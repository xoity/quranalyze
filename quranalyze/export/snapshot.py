"""
Export functionality for analysis snapshots.

This module provides functionality to export corpus state and analysis
results for reproducibility and sharing.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..config import EXPORT_FORMAT_VERSION
from ..core.corpus import Corpus
from ..core.word import Word
from ..exceptions import QuranalyzeError


class SnapshotExporter:
    """
    Exporter for creating snapshots of corpus state and analysis.
    
    This class handles exporting corpus data, word lists, and analysis
    results in a structured format for reproducibility.
    """
    
    def __init__(self, corpus: Corpus) -> None:
        """
        Initialize the snapshot exporter.
        
        Args:
            corpus: The Corpus to export from
        """
        self.corpus = corpus
    
    def export_metadata(self) -> dict[str, Any]:
        """
        Export corpus metadata.
        
        Returns:
            Dictionary containing corpus metadata
        """
        return {
            "format_version": EXPORT_FORMAT_VERSION,
            "export_timestamp": datetime.now().isoformat(),
            "total_surahs": self.corpus.total_surahs(),
            "total_ayahs": self.corpus.total_ayahs(),
            "total_words": self.corpus.total_words(),
        }
    
    def export_word_list(
        self,
        words: list[Word],
        include_text: bool = True,
        include_normalized: bool = True,
        include_buckwalter: bool = True,
        include_location: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Export a list of words to structured format.
        
        Args:
            words: List of words to export
            include_text: Include original text
            include_normalized: Include normalized text
            include_buckwalter: Include Buckwalter transliteration
            include_location: Include location information
            
        Returns:
            List of dictionaries representing words
        """
        exported = []
        
        for word in words:
            word_data: dict[str, Any] = {}
            
            if include_location:
                word_data["surah"] = word.surah_number
                word_data["ayah"] = word.ayah_number
                word_data["position"] = word.position
            
            if include_text:
                word_data["text"] = word.text
            
            if include_normalized:
                word_data["normalized"] = word.normalized
            
            if include_buckwalter:
                word_data["buckwalter"] = word.buckwalter
            
            if word.root:
                word_data["root"] = word.root
            
            if word.lemma:
                word_data["lemma"] = word.lemma
            
            exported.append(word_data)
        
        return exported
    
    def export_full_snapshot(
        self,
        output_path: str,
        include_all_words: bool = False,
    ) -> None:
        """
        Export a complete snapshot to JSON file.
        
        Args:
            output_path: Path to save the snapshot JSON
            include_all_words: Whether to include all words (can be large)
            
        Raises:
            QuranalyzeError: If export fails
        """
        try:
            snapshot = {
                "metadata": self.export_metadata(),
                "word_counts_by_surah": self.corpus.word_count_by_surah(),
            }
            
            if include_all_words:
                snapshot["words"] = self.export_word_list(self.corpus.words)
            
            # Write to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            raise QuranalyzeError(f"Failed to export snapshot: {e}") from e
    
    def export_surah_summary(self, surah_number: int, output_path: str) -> None:
        """
        Export summary information for a specific surah.
        
        Args:
            surah_number: The surah number to export
            output_path: Path to save the summary JSON
            
        Raises:
            QuranalyzeError: If export fails
        """
        try:
            surah = self.corpus.get_surah(surah_number)
            if not surah:
                raise QuranalyzeError(f"Surah {surah_number} not found")
            
            # Get words for this surah
            surah_words = self.corpus.filter_words().by_surah(surah_number).get()
            
            summary = {
                "surah_number": surah.number,
                "surah_name": surah.name,
                "english_name": surah.english_name,
                "revelation_type": surah.revelation_type,
                "ayah_count": surah.ayah_count,
                "word_count": len(surah_words),
                "words": self.export_word_list(surah_words),
            }
            
            # Write to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            raise QuranalyzeError(f"Failed to export surah summary: {e}") from e
    
    def export_filtered_words(
        self,
        words: list[Word],
        output_path: str,
        description: Optional[str] = None,
    ) -> None:
        """
        Export a filtered list of words.
        
        Args:
            words: List of words to export
            output_path: Path to save the export JSON
            description: Optional description of the filter
            
        Raises:
            QuranalyzeError: If export fails
        """
        try:
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "word_count": len(words),
                    "description": description,
                },
                "words": self.export_word_list(words),
            }
            
            # Write to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            raise QuranalyzeError(f"Failed to export filtered words: {e}") from e
