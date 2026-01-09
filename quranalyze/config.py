"""
Configuration settings for the quranalyze framework.

This module contains all configuration constants and settings used
throughout the framework. All assumptions are made explicit here.
"""

from typing import Final


# Quran structure constants
TOTAL_SURAHS: Final[int] = 114
"""Total number of surahs in the Quran."""

# Data source configuration
DEFAULT_QURANJSON_PATH: Final[str] = "./quranjson/source/surah"
"""Default path to quranjson dataset directory containing surah JSON files."""

# Expected JSON structure keys (quranjson format)
SURAH_NUMBER_KEY: Final[str] = "index"
SURAH_NAME_KEY: Final[str] = "name"
VERSE_KEY: Final[str] = "verse"  # Dictionary of verse_N: text
COUNT_KEY: Final[str] = "count"  # Number of verses

# Normalization settings
NORMALIZE_HAMZA: Final[bool] = True
"""Whether to normalize hamza variations."""

NORMALIZE_ALEF: Final[bool] = True
"""Whether to normalize alef variations."""

NORMALIZE_TAA_MARBUTA: Final[bool] = True
"""Whether to normalize taa marbuta."""

REMOVE_DIACRITICS: Final[bool] = True
"""Whether to remove diacritical marks (harakat)."""

# Tokenization settings
WORD_DELIMITER: Final[str] = " "
"""Delimiter used to split ayah text into words."""

# Visualization defaults
DEFAULT_FIGURE_SIZE: Final[tuple[int, int]] = (12, 8)
"""Default figure size for matplotlib plots."""

DEFAULT_DPI: Final[int] = 100
"""Default DPI for matplotlib plots."""

DEFAULT_POINT_SIZE: Final[int] = 20
"""Default point size for scatter plots."""

DEFAULT_ALPHA: Final[float] = 0.6
"""Default alpha transparency for plot points."""

# Graph construction
MIN_SHARED_ROOT_WEIGHT: Final[float] = 1.0
"""Minimum edge weight for shared root relationships."""

MIN_SHARED_LEMMA_WEIGHT: Final[float] = 0.5
"""Minimum edge weight for shared lemma relationships."""

# Export settings
EXPORT_FORMAT_VERSION: Final[str] = "1.0.0"
"""Version identifier for exported snapshots."""
