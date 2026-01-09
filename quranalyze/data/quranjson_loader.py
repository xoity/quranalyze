"""
QuranJSON dataset loader.

This module provides functionality to load Quranic data from the quranjson
GitHub dataset, which is treated as the canonical data source.
"""

import json
from pathlib import Path
from typing import Any, Optional

from ..config import (
    AYAH_NUMBER_KEY,
    AYAH_TEXT_KEY,
    AYAHS_KEY,
    DEFAULT_QURANJSON_PATH,
    SURAH_NAME_KEY,
    SURAH_NUMBER_KEY,
    TOTAL_SURAHS,
)
from ..core.ayah import Ayah
from ..core.surah import Surah
from ..exceptions import DataLoadError, DataValidationError


class QuranJsonLoader:
    """
    Loader for the quranjson dataset.
    
    This class handles loading and validation of Quran data from JSON files
    structured by surah. Each surah is expected to be in a separate JSON file
    with a specific structure.
    
    Attributes:
        data_path: Path to the directory containing surah JSON files
    """
    
    def __init__(self, data_path: str = DEFAULT_QURANJSON_PATH) -> None:
        """
        Initialize the loader with a data path.
        
        Args:
            data_path: Path to the quranjson surah directory
            
        Raises:
            DataLoadError: If the data path does not exist
        """
        self.data_path = Path(data_path)
        if not self.data_path.exists():
            raise DataLoadError(f"Data path does not exist: {data_path}")
        if not self.data_path.is_dir():
            raise DataLoadError(f"Data path is not a directory: {data_path}")
    
    def _validate_surah_data(self, data: dict[str, Any], surah_number: int) -> None:
        """
        Validate the structure of loaded surah data.
        
        Args:
            data: The loaded JSON data
            surah_number: Expected surah number
            
        Raises:
            DataValidationError: If data structure is invalid
        """
        # Check required keys
        if SURAH_NUMBER_KEY not in data:
            raise DataValidationError(f"Missing key: {SURAH_NUMBER_KEY}")
        if SURAH_NAME_KEY not in data:
            raise DataValidationError(f"Missing key: {SURAH_NAME_KEY}")
        if AYAHS_KEY not in data:
            raise DataValidationError(f"Missing key: {AYAHS_KEY}")
        
        # Validate surah number
        if data[SURAH_NUMBER_KEY] != surah_number:
            raise DataValidationError(
                f"Surah number mismatch: expected {surah_number}, "
                f"got {data[SURAH_NUMBER_KEY]}"
            )
        
        # Validate ayahs structure
        if not isinstance(data[AYAHS_KEY], list):
            raise DataValidationError("Ayahs must be a list")
        if not data[AYAHS_KEY]:
            raise DataValidationError("Surah must contain at least one ayah")
        
        # Validate each ayah
        for i, ayah_data in enumerate(data[AYAHS_KEY]):
            if not isinstance(ayah_data, dict):
                raise DataValidationError(f"Ayah {i} is not a dictionary")
            if AYAH_NUMBER_KEY not in ayah_data:
                raise DataValidationError(f"Ayah {i} missing key: {AYAH_NUMBER_KEY}")
            if AYAH_TEXT_KEY not in ayah_data:
                raise DataValidationError(f"Ayah {i} missing key: {AYAH_TEXT_KEY}")
    
    def load_surah(self, surah_number: int) -> Surah:
        """
        Load a single surah from the dataset.
        
        Args:
            surah_number: The surah number to load (1-114)
            
        Returns:
            Surah object with all ayahs
            
        Raises:
            DataLoadError: If file cannot be read
            DataValidationError: If data structure is invalid
        """
        if surah_number < 1 or surah_number > TOTAL_SURAHS:
            raise DataLoadError(f"Invalid surah number: {surah_number}")
        
        # Construct file path (files are named surah_1.json, surah_2.json, etc.)
        file_path = self.data_path / f"surah_{surah_number}.json"
        
        if not file_path.exists():
            raise DataLoadError(f"Surah file not found: {file_path}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Invalid JSON in {file_path}: {e}") from e
        except Exception as e:
            raise DataLoadError(f"Failed to read {file_path}: {e}") from e
        
        # Validate data structure
        self._validate_surah_data(data, surah_number)
        
        # Extract ayahs
        ayahs = []
        for ayah_data in data[AYAHS_KEY]:
            ayah = Ayah(
                surah_number=surah_number,
                ayah_number=ayah_data[AYAH_NUMBER_KEY],
                text=ayah_data[AYAH_TEXT_KEY],
            )
            ayahs.append(ayah)
        
        # Create and return surah
        return Surah(
            number=surah_number,
            name=data[SURAH_NAME_KEY],
            ayahs=tuple(ayahs),
            english_name=data.get("englishName"),
            revelation_type=data.get("revelationType"),
        )
    
    def load_all_surahs(self, start: int = 1, end: Optional[int] = None) -> list[Surah]:
        """
        Load multiple surahs from the dataset.
        
        Args:
            start: First surah number to load (default: 1)
            end: Last surah number to load (default: 114)
            
        Returns:
            List of Surah objects in order
            
        Raises:
            DataLoadError: If any file cannot be read
            DataValidationError: If any data structure is invalid
        """
        if end is None:
            end = TOTAL_SURAHS
        
        if start < 1 or start > TOTAL_SURAHS:
            raise DataLoadError(f"Invalid start surah number: {start}")
        if end < 1 or end > TOTAL_SURAHS:
            raise DataLoadError(f"Invalid end surah number: {end}")
        if start > end:
            raise DataLoadError(f"Start ({start}) must be <= end ({end})")
        
        surahs = []
        for surah_number in range(start, end + 1):
            surah = self.load_surah(surah_number)
            surahs.append(surah)
        
        return surahs
    
    def verify_dataset(self) -> dict[str, Any]:
        """
        Verify the integrity of the entire dataset.
        
        Returns:
            Dictionary with verification results including:
            - total_surahs: Number of surahs found
            - missing_surahs: List of missing surah numbers
            - invalid_surahs: List of surahs with invalid data
            - total_ayahs: Total number of ayahs across all surahs
            
        """
        results = {
            "total_surahs": 0,
            "missing_surahs": [],
            "invalid_surahs": [],
            "total_ayahs": 0,
        }
        
        for surah_number in range(1, TOTAL_SURAHS + 1):
            file_path = self.data_path / f"surah_{surah_number}.json"
            
            if not file_path.exists():
                results["missing_surahs"].append(surah_number)
                continue
            
            try:
                surah = self.load_surah(surah_number)
                results["total_surahs"] += 1
                results["total_ayahs"] += surah.ayah_count
            except (DataLoadError, DataValidationError) as e:
                results["invalid_surahs"].append((surah_number, str(e)))
        
        return results
